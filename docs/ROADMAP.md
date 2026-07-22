# Roadmap

O roadmap prioriza um fluxo vertical funcional antes de recursos avançados.

## M0 - Fundação e arquitetura

Base técnica, convenções, configuração local e decisões que sustentam o restante do produto.

- [ ] `VF-001` chore: inicializar a API Vincere Flow com Spring Boot
- [ ] `VF-002` chore: definir arquitetura modular e convenções do repositório
- [ ] `VF-003` infra: configurar PostgreSQL local com Docker Compose
- [ ] `VF-004` config: separar perfis local, test e prod
- [ ] `VF-005` db: configurar Flyway e migration de baseline
- [ ] `VF-006` api: padronizar validação e tratamento global de erros
- [ ] `VF-007` docs: registrar visão do produto e escopo do MVP

## M1 - Catálogo e estoque

Cadastro de produtos, saldo de estoque e trilha auditável de movimentações.

- [ ] `VF-008` feat(produtos): modelar produto e persistência
- [ ] `VF-009` feat(produtos): implementar cadastro e manutenção de produtos
- [ ] `VF-010` feat(produtos): implementar busca, filtros e paginação
- [ ] `VF-011` feat(estoque): modelar saldo e movimentações
- [ ] `VF-012` feat(estoque): registrar entradas e ajustes
- [ ] `VF-013` feat(estoque): consultar saldo e histórico
- [ ] `VF-014` feat(estoque): listar produtos abaixo do estoque mínimo

## M2 - Vendas

Venda transacional com múltiplos itens, validações, consultas, cancelamento e proteção contra concorrência.

- [ ] `VF-015` feat(vendas): modelar venda e itens
- [ ] `VF-016` feat(vendas): registrar venda com múltiplos itens
- [ ] `VF-017` feat(vendas): validar estoque, preços e descontos
- [ ] `VF-018` feat(vendas): consultar vendas e seus detalhes
- [ ] `VF-019` feat(vendas): cancelar venda e estornar estoque
- [ ] `VF-020` feat(estoque): proteger saldo contra vendas concorrentes

## M3 - Financeiro e indicadores

Receitas, despesas, integração com vendas, fluxo de caixa e indicadores comerciais.

- [ ] `VF-021` feat(financeiro): modelar categorias e lançamentos
- [ ] `VF-022` feat(financeiro): registrar receitas e despesas manuais
- [ ] `VF-023` feat(financeiro): integrar lançamentos ao ciclo da venda
- [ ] `VF-024` feat(financeiro): consultar fluxo de caixa por período
- [ ] `VF-025` feat(indicadores): disponibilizar resumo comercial

## M4 - Qualidade e segurança

Testes, documentação da API, observabilidade, integração contínua e controle de acesso.

- [ ] `VF-026` test: configurar testes de integração com Testcontainers
- [ ] `VF-027` test: cobrir regras críticas com testes automatizados
- [ ] `VF-028` docs: documentar a API com OpenAPI e Swagger UI
- [ ] `VF-029` ops: adicionar health checks e logs estruturados
- [ ] `VF-030` ci: executar build e testes no GitHub Actions
- [ ] `VF-031` security: implementar autenticação e autorização por perfis
- [ ] `VF-032` security: revisar validação, segredos e exposição de dados

## M5 - Azure e lançamento

Publicação no Azure, entrega contínua, monitoramento, apresentação de portfólio e versão 1.0.0.

- [ ] `VF-033` cloud: provisionar PostgreSQL no Azure
- [ ] `VF-034` cloud: publicar a API no Azure App Service
- [ ] `VF-035` cloud: configurar ambiente e segredos de produção
- [ ] `VF-036` cd: automatizar deploy no Azure com GitHub Actions
- [ ] `VF-037` ops: integrar Application Insights e alertas de custo
- [ ] `VF-038` docs: preparar apresentação de portfólio e dados de demonstração
- [ ] `VF-039` release: publicar Vincere Flow API v1.0.0

## Definição de pronto da versão 1.0

- Fluxo produto -> estoque -> venda -> financeiro funciona de ponta a ponta.
- Regras P0 possuem testes automatizados.
- API está documentada e protegida por autenticação.
- CI/CD publica uma versão rastreável no Azure.
- Monitoramento e alertas de custo estão ativos.
- README permite que outra pessoa compreenda e execute o projeto.
