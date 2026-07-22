# Vincere Flow API

> Gestão integrada de estoque, vendas e financeiro para transformar movimento operacional em decisão.

![Status](https://img.shields.io/badge/status-planejamento-blue)
![Java](https://img.shields.io/badge/Java-21-orange)
![Architecture](https://img.shields.io/badge/arquitetura-monolito%20modular-6f42c1)

## Visão

O **Vincere Flow** é um sistema de gestão comercial criado para integrar quatro pontos que normalmente ficam separados em pequenos negócios: produtos, estoque, vendas e financeiro.

O fluxo principal do MVP é:

```text
Cadastrar produto
    -> registrar entrada de estoque
    -> concluir venda
    -> baixar estoque
    -> gerar receita
    -> consultar caixa, lucro e margem
```

## Escopo da API

- Catálogo e manutenção de produtos.
- Entradas, ajustes, saídas e histórico de estoque.
- Vendas com múltiplos itens, cancelamento e estorno.
- Receitas, despesas e fluxo de caixa.
- Indicadores comerciais e financeiros.
- Autenticação, autorização e auditoria.
- Deploy automatizado e monitoramento no Azure.

## Arquitetura planejada

O projeto será um **monólito modular**, organizado por domínio:

```text
io.github.vinifersantos.vincereflow
|-- produto
|-- estoque
|-- venda
|-- financeiro
|-- indicador
`-- shared
```

Detalhes e decisões: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Stack planejada

- Java 21
- Spring Boot e Maven
- Spring Web, Validation e Data JPA
- PostgreSQL e Flyway
- JUnit, Mockito e Testcontainers
- OpenAPI/Swagger
- Docker Compose
- GitHub Actions
- Azure App Service, Azure Database for PostgreSQL e Application Insights

## Roadmap

O trabalho está dividido em seis marcos, da fundação ao lançamento. Consulte:

- [`docs/ROADMAP.md`](docs/ROADMAP.md)
- [`docs/BACKLOG.md`](docs/BACKLOG.md)
- [Issues do projeto](../../issues)

## Nome

**Vincere Flow** une a marca **Vincere** à ideia de fluxo: cada venda movimenta estoque, caixa e indicadores. O nome permite evoluir o produto sem limitá-lo a um único módulo.

## Licença

Distribuído sob a licença MIT. Consulte [`LICENSE`](LICENSE).
