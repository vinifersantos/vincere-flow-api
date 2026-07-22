# Contribuição

## Fluxo de trabalho

1. Escolha uma issue sem dependências abertas.
2. Crie uma branch curta, por exemplo `feat/VF-009-produtos`.
3. Faça commits pequenos usando Conventional Commits.
4. Execute build e testes.
5. Abra um pull request ligado à issue.

## Commits

```text
feat: adiciona cadastro de produto
fix: impede estoque negativo
refactor: separa calculo de margem
test: cobre cancelamento de venda
docs: atualiza fluxo do MVP
chore: configura Flyway
```

## Regras

- Não altere migrations já publicadas.
- Não versione segredos.
- Não exponha entidades JPA diretamente na API.
- Toda regra P0 deve possuir teste automatizado.
- Uma issue deve produzir uma mudança pequena e revisável.
