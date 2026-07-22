#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args, *, check=True, capture=True, input_text=None):
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        input=input_text,
        capture_output=capture,
        check=False,
    )
    if check and result.returncode != 0:
        command = ' '.join(args)
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f'Command failed: {command}\n{message}')
    return result


def gh_json(args, *, method=None, payload=None, paginate=False):
    command = ['gh', 'api']
    if method:
        command.extend(['--method', method])
    if paginate:
        command.append('--paginate')
    command.extend(args)
    input_text = None
    if payload is not None:
        command.extend(['--input', '-'])
        input_text = json.dumps(payload)
    result = run(command, input_text=input_text)
    output = result.stdout.strip()
    if not output:
        return None
    if paginate:
        decoder = json.JSONDecoder()
        index = 0
        values = []
        while index < len(output):
            while index < len(output) and output[index].isspace():
                index += 1
            if index >= len(output):
                break
            value, index = decoder.raw_decode(output, index)
            if isinstance(value, list):
                values.extend(value)
            else:
                values.append(value)
        return values
    return json.loads(output)


def read_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding='utf-8'))


def ensure_prerequisites():
    if shutil.which('gh') is None:
        raise RuntimeError('GitHub CLI not found. Install it from https://cli.github.com and run gh auth login.')
    if shutil.which('git') is None:
        raise RuntimeError('Git not found.')
    run(['gh', 'auth', 'status'])


def ensure_local_repository(profile):
    if not (ROOT / '.git').exists():
        run(['git', 'init', '-b', 'main'])

    name = run(['git', 'config', '--get', 'user.name'], check=False).stdout.strip()
    email = run(['git', 'config', '--get', 'user.email'], check=False).stdout.strip()
    if not name:
        run(['git', 'config', 'user.name', profile.get('name') or profile['login']])
    if not email:
        user_id = profile['id']
        login = profile['login']
        run(['git', 'config', 'user.email', f'{user_id}+{login}@users.noreply.github.com'])

    run(['git', 'add', '.'])
    has_head = run(['git', 'rev-parse', '--verify', 'HEAD'], check=False).returncode == 0
    staged = run(['git', 'diff', '--cached', '--quiet'], check=False).returncode != 0
    if not has_head:
        run(['git', 'commit', '-m', 'chore: initialize Vincere Flow repository'])
    elif staged:
        run(['git', 'commit', '-m', 'chore: synchronize repository planning files'])


def repository_exists(repo_full_name):
    result = run(['gh', 'repo', 'view', repo_full_name], check=False)
    return result.returncode == 0


def ensure_remote(repo_meta, owner, private, skip_push):
    repo_name = repo_meta['name']
    repo_full_name = f'{owner}/{repo_name}'
    exists = repository_exists(repo_full_name)

    if not exists:
        visibility_flag = '--private' if private else '--public'
        command = [
            'gh', 'repo', 'create', repo_full_name,
            visibility_flag,
            '--description', repo_meta['description'],
            '--source', '.',
            '--remote', 'origin',
        ]
        if not skip_push:
            command.append('--push')
        run(command)
    else:
        remotes = run(['git', 'remote'], check=False).stdout.split()
        if 'origin' not in remotes:
            run(['git', 'remote', 'add', 'origin', f'https://github.com/{repo_full_name}.git'])
        if not skip_push:
            run(['git', 'push', '-u', 'origin', 'main'])

    gh_json(
        [f'repos/{repo_full_name}'],
        method='PATCH',
        payload={
            'description': repo_meta['description'],
            'has_issues': True,
            'has_projects': True,
            'has_wiki': False,
        },
    )
    gh_json(
        [f'repos/{repo_full_name}/topics'],
        method='PUT',
        payload={'names': repo_meta['topics']},
    )
    return repo_full_name


def ensure_labels(repo_full_name, labels):
    for label in labels:
        result = run(
            [
                'gh', 'label', 'create', label['name'],
                '--repo', repo_full_name,
                '--color', label['color'],
                '--description', label['description'],
                '--force',
            ],
            check=False,
        )
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"Could not create label {label['name']}: {message}")


def ensure_milestones(repo_full_name, milestones):
    existing = gh_json([f'repos/{repo_full_name}/milestones?state=all&per_page=100'], paginate=True) or []
    by_title = {item['title']: item for item in existing}
    result = {}
    for milestone in milestones:
        current = by_title.get(milestone['title'])
        payload = {
            'title': milestone['title'],
            'description': milestone['description'],
            'state': 'open',
        }
        if current:
            updated = gh_json(
                [f"repos/{repo_full_name}/milestones/{current['number']}"],
                method='PATCH',
                payload=payload,
            )
        else:
            updated = gh_json(
                [f'repos/{repo_full_name}/milestones'],
                method='POST',
                payload=payload,
            )
        result[milestone['title']] = updated['number']
    return result


def render_issue_body(item, issue_numbers):
    lines = [
        f"<!-- backlog-id: {item['id']} -->",
        '## Objetivo',
        '',
        item['objective'],
        '',
        '## Critérios de aceite',
        '',
    ]
    lines.extend([f"- [ ] {criterion}" for criterion in item['acceptance']])
    lines.extend(['', '## Dependências', ''])
    if item['depends_on']:
        for dependency_id in item['depends_on']:
            number = issue_numbers.get(dependency_id)
            if number:
                lines.append(f'- [ ] #{number} (`{dependency_id}`)')
            else:
                lines.append(f'- [ ] `{dependency_id}`')
    else:
        lines.append('- Nenhuma.')
    if item.get('notes'):
        lines.extend(['', '## Observações', ''])
        lines.extend([f'- {note}' for note in item['notes']])
    lines.extend([
        '',
        '## Definição de pronto',
        '',
        '- [ ] Implementação revisada.',
        '- [ ] Testes relevantes passam.',
        '- [ ] Documentação foi atualizada quando necessário.',
        '- [ ] Nenhum segredo ou dado sensível foi incluído.',
    ])
    return '\n'.join(lines) + '\n'


def existing_issues(repo_full_name):
    items = gh_json([f'repos/{repo_full_name}/issues?state=all&per_page=100'], paginate=True) or []
    result = {}
    for item in items:
        if 'pull_request' not in item:
            result[item['title']] = item
    return result


def synchronize_issues(repo_full_name, issues, milestone_numbers, login):
    existing = existing_issues(repo_full_name)
    issue_numbers = {}

    for item in issues:
        current = existing.get(item['title'])
        if current:
            issue_numbers[item['id']] = current['number']
            continue

        body = render_issue_body(item, issue_numbers)
        payload = {
            'title': item['title'],
            'body': body,
            'labels': item['labels'],
            'milestone': milestone_numbers[item['milestone']],
            'assignees': [login],
        }
        created = gh_json([f'repos/{repo_full_name}/issues'], method='POST', payload=payload)
        issue_numbers[item['id']] = created['number']
        print(f"Created #{created['number']}: {item['title']}")

    existing = existing_issues(repo_full_name)
    for item in issues:
        current = existing[item['title']]
        body = render_issue_body(item, issue_numbers)
        payload = {
            'title': item['title'],
            'body': body,
            'labels': item['labels'],
            'milestone': milestone_numbers[item['milestone']],
            'assignees': [login],
            'state': 'open',
        }
        gh_json(
            [f"repos/{repo_full_name}/issues/{current['number']}"],
            method='PATCH',
            payload=payload,
        )

    return issue_numbers


def main():
    parser = argparse.ArgumentParser(description='Create and synchronize the Vincere Flow GitHub repository.')
    parser.add_argument('--owner', help='GitHub owner. Defaults to the authenticated user.')
    parser.add_argument('--private', action='store_true', help='Create a private repository instead of public.')
    parser.add_argument('--skip-push', action='store_true', help='Do not push the local files.')
    parser.add_argument('--skip-issues', action='store_true', help='Do not create labels, milestones and issues.')
    args = parser.parse_args()

    ensure_prerequisites()
    profile = gh_json(['user'])
    owner = args.owner or profile['login']

    repo_meta = read_json('github/repository.json')
    labels = read_json('github/labels.json')
    milestones = read_json('github/milestones.json')
    issues = read_json('github/issues.json')

    ensure_local_repository(profile)
    repo_full_name = ensure_remote(repo_meta, owner, args.private, args.skip_push)

    if not args.skip_issues:
        ensure_labels(repo_full_name, labels)
        milestone_numbers = ensure_milestones(repo_full_name, milestones)
        issue_numbers = synchronize_issues(repo_full_name, issues, milestone_numbers, profile['login'])
        print(f'Synchronized {len(issue_numbers)} issues.')

    print(f'Repository ready: https://github.com/{repo_full_name}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
