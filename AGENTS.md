# AGENTS.md — Vincere Flow API

Diretriz primária para agentes autônomos e assistentes de IA operando no repositório **Vincere Flow API**.
Os procedimentos universais de engenharia de software (Code-First, Grill-Me, arquitetura, testes, dados e governança) são providos pela Skill Master global `senior-software-engineer` (`C:\Users\vinic\.gemini\config\skills\senior-software-engineer\SKILL.md`).

---

## 1. Identidade e Domínio do Sistema

- **Propósito:** Gestão comercial integrada de produtos, entradas/saídas de estoque, vendas com múltiplos itens e conciliação financeira de fluxo de caixa para pequenos negócios.
- **Arquitetura:** Monólito modular organizado por pacotes de domínio em `io.github.vinifersantos.vincereflow` (`produto`, `estoque`, `venda`, `financeiro`, `indicador`, `shared`).
- **Documentação de Referência:** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) e [`README.md`](README.md).

---

## 2. Stack Tecnológica e Invariantes

- **Runtime & Framework:** Java 21, Spring Boot 3.x, Spring Data JPA, Spring Web e Spring Validation.
- **Banco de Dados & Migrações:** PostgreSQL versionado com **Flyway** em `src/main/resources/db/migration/`. Nunca edite migrações já aplicadas.
- **Testes & Qualidade:** JUnit 5, Mockito e Testcontainers para testes de integração com banco real.
- **Infraestrutura:** Docker Compose local e Azure (App Service, Azure Database for PostgreSQL).

---

## 3. Comandos de Validação e Build

Execução via Maven Wrapper:
```bash
./mvnw clean compile        # Compilação e checagem de contratos
./mvnw test                 # Execução da suíte de testes unitários (JUnit)
./mvnw verify               # Verificação completa e testes de integração
```

---

## 4. Governança e Regras de Contribuição

- Proibido commit direto na branch `main`. Toda alteração deve ocorrer via branch dedicada (`feat/`, `fix/`, `chore/`, `docs/`) com Pull Request no GitHub.
- Mensagens de commit seguindo Conventional Commits.
- Segredos, credenciais de banco ou chaves de nuvem nunca devem ser versionados.
