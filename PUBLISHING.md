# Publicar no GitHub

O pacote inclui um script idempotente que cria ou sincroniza:

- repositório público `vincere-flow-api`;
- descrição e tópicos;
- labels;
- seis milestones;
- 39 issues com critérios de aceite e dependências;
- commit inicial e push para a branch `main`.

## Pré-requisitos

1. Instale Git e GitHub CLI.
2. Autentique a CLI:

```bash
gh auth login
```

3. Na raiz do projeto, execute:

```bash
python3 scripts/publish_github.py
```

Por padrão, o script usa o usuário autenticado e cria um repositório público.

Opções:

```bash
python3 scripts/publish_github.py --private
python3 scripts/publish_github.py --owner outro-owner
python3 scripts/publish_github.py --skip-issues
```

O script pode ser executado novamente: ele reutiliza o repositório, atualiza labels e milestones e evita duplicar issues pelo título.
