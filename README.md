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

## Executando localmente

### Pré-requisitos

- **Java 21 LTS**
- **IntelliJ IDEA Ultimate** (recomendado)

> **Atenção (Configuração do Java no Terminal):** Se o terminal Windows (PowerShell/CMD) estiver configurado por padrão com uma versão do Java anterior (como Java 8), defina a variável `JAVA_HOME` apontando para o JDK 21 (por exemplo, a JDK bundled do IntelliJ IDEA em `C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.3\jbr`) antes de executar os comandos do Maven Wrapper:
>
> **PowerShell:**
> ```powershell
> $env:JAVA_HOME="C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.3\jbr"
> $env:Path="$env:JAVA_HOME\bin;$env:Path"
> ```
>
> **CMD:**
> ```cmd
> set JAVA_HOME=C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.3\jbr
> set PATH=%JAVA_HOME%\bin;%PATH%
> ```

### Como executar

1. Abra o projeto no **IntelliJ IDEA Ultimate** (o Maven carregará o projeto automaticamente utilizando a JDK 21).
2. Execute a aplicação diretamente pela classe principal `VincereFlowApplication` (`src/main/java/io/github/vinifersantos/vincereflow/VincereFlowApplication.java`).
3. Ou execute a aplicação utilizando o **Maven Wrapper**:

```powershell
.\mvnw.cmd spring-boot:run
```

> **Nota:** O banco de dados PostgreSQL será configurado em uma issue posterior (Issue #3/#4). Atualmente, a autoconfiguração de banco está desabilitada temporariamente para permitir a execução e validação da fundação técnica da API.

### Execução de testes

Para executar os testes automatizados da aplicação:

```powershell
.\mvnw.cmd test
```

Para compilar, testar e empacotar a aplicação com validação completa:

```powershell
.\mvnw.cmd clean verify
```

### Endereços locais

- Aplicação: `http://localhost:8080`
- Endpoint de saúde: `http://localhost:8080/actuator/health`


## Nome

**Vincere Flow** une a marca **Vincere** à ideia de fluxo: cada venda movimenta estoque, caixa e indicadores. O nome permite evoluir o produto sem limitá-lo a um único módulo.

## Licença

Distribuído sob a licença MIT. Consulte [`LICENSE`](LICENSE).

