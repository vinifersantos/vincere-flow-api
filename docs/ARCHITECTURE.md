# Arquitetura inicial

## Decisão principal

O Vincere Flow começará como um **monólito modular**. Uma aplicação, um banco e limites claros entre domínios.

Essa escolha reduz complexidade operacional enquanto permite praticar organização, transações, testes e deploy profissional.

## Módulos

```text
produto     -> cadastro e atributos comerciais
estoque     -> saldo e movimentações
venda       -> venda, itens, cancelamento e regras
financeiro  -> receitas, despesas, estornos e caixa
indicador   -> leituras agregadas para gestão
shared      -> erros, auditoria e componentes transversais pequenos
```

## Regras arquiteturais

1. Controllers trabalham com DTOs, nunca com entidades JPA diretamente.
2. Regras de negócio ficam em serviços ou objetos de domínio, não em controllers.
3. Venda, baixa de estoque e geração financeira formam uma transação atômica.
4. Dinheiro usa `BigDecimal`; datas usam `java.time`.
5. Movimentações e cancelamentos preservam histórico.
6. Migrations são versionadas com Flyway e nunca reescritas depois de aplicadas.
7. Segredos entram por configuração externa.
8. API inicia versionada em `/api/v1`.

## Arquitetura de execução

```text
Cliente HTTP
    -> Azure App Service / Spring Boot
    -> Azure Database for PostgreSQL
    -> Application Insights

GitHub
    -> GitHub Actions CI/CD
    -> Azure App Service
```

## Decisões adiadas

- Interface web.
- Múltiplas lojas e multi-tenant.
- Integração bancária.
- Emissão fiscal.
- Microsserviços, mensageria e Kubernetes.
