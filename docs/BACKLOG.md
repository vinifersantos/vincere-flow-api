# Backlog estruturado

As issues abaixo serão criadas automaticamente por `scripts/publish_github.py`.

## M0 - Fundação e arquitetura

Base técnica, convenções, configuração local e decisões que sustentam o restante do produto.

### VF-001 - chore: inicializar a API Vincere Flow com Spring Boot

Criar a base executável da API Java que receberá os módulos do Vincere Flow.

**Labels:** type:chore, area:foundation, priority:P0

**Dependências:** nenhuma

**Critérios de aceite:**

- [ ] Projeto Maven criado com Java 21 e Spring Boot.
- [ ] Package base definido como `io.github.vinifersantos.vincereflow`.
- [ ] Dependências iniciais limitadas a Web, Validation, Data JPA, PostgreSQL, Flyway e Actuator.
- [ ] Aplicação inicia localmente e o teste de contexto passa.
- [ ] Nenhum segredo ou arquivo de IDE é versionado.

### VF-002 - chore: definir arquitetura modular e convenções do repositório

Definir uma estrutura simples, coerente e evolutiva para evitar um projeto organizado por improviso.

**Labels:** type:chore, area:foundation, priority:P0

**Dependências:** VF-001

**Critérios de aceite:**

- [ ] Arquitetura registrada como monólito modular organizado por domínio.
- [ ] Módulos previstos: `produto`, `estoque`, `venda`, `financeiro`, `indicador` e `shared`.
- [ ] Convenções de nomes, commits, branches e pull requests documentadas.
- [ ] Regras de dependência entre módulos registradas em `docs/ARCHITECTURE.md`.
- [ ] Decisões arquiteturais iniciais registradas em ADR.

### VF-003 - infra: configurar PostgreSQL local com Docker Compose

Disponibilizar um banco PostgreSQL reproduzível para desenvolvimento local.

**Labels:** type:infra, area:foundation, priority:P0, good first issue

**Dependências:** VF-001

**Critérios de aceite:**

- [ ] Arquivo `compose.yaml` inicia uma instância PostgreSQL suportada.
- [ ] Banco, usuário e senha locais são configurados por variáveis de ambiente com valores de desenvolvimento.
- [ ] Volume nomeado preserva os dados entre reinicializações.
- [ ] Health check confirma quando o banco está pronto.
- [ ] README documenta os comandos para iniciar, parar e remover o ambiente.

### VF-004 - config: separar perfis local, test e prod

Separar configurações por ambiente sem acoplar segredos ao código.

**Labels:** type:chore, area:foundation, priority:P0

**Dependências:** VF-001, VF-003

**Critérios de aceite:**

- [ ] Perfis `local`, `test` e `prod` possuem responsabilidades claras.
- [ ] Credenciais de produção são lidas apenas de variáveis de ambiente.
- [ ] Perfil de teste não depende do banco de desenvolvimento.
- [ ] Configuração falha de forma explícita quando variáveis obrigatórias estão ausentes.
- [ ] Arquivos `.env` reais permanecem fora do Git.

### VF-005 - db: configurar Flyway e migration de baseline

Controlar a evolução do esquema do banco por migrations versionadas.

**Labels:** type:infra, area:foundation, priority:P0

**Dependências:** VF-003, VF-004

**Critérios de aceite:**

- [ ] Flyway executa automaticamente na inicialização.
- [ ] Hibernate opera com `ddl-auto=validate` fora dos testes isolados.
- [ ] Migration de baseline cria extensões ou estruturas compartilhadas estritamente necessárias.
- [ ] Convenção de nomes `Vn__descricao.sql` está documentada.
- [ ] Aplicar a mesma migration duas vezes não produz alterações indevidas.

### VF-006 - api: padronizar validação e tratamento global de erros

Garantir respostas previsíveis para entradas inválidas e falhas de regra de negócio.

**Labels:** type:feature, area:foundation, priority:P0

**Dependências:** VF-001

**Critérios de aceite:**

- [ ] DTOs de entrada usam Bean Validation.
- [ ] Exceções de negócio são mapeadas por `@RestControllerAdvice`.
- [ ] Resposta de erro possui código, mensagem, timestamp, path e detalhes de campos quando aplicável.
- [ ] Status HTTP distingue validação, recurso ausente, conflito e erro interno.
- [ ] Stack traces e dados sensíveis não são expostos ao cliente.

### VF-007 - docs: registrar visão do produto e escopo do MVP

Transformar a ideia do produto em um escopo verificável e protegido contra expansão descontrolada.

**Labels:** type:docs, area:foundation, priority:P1, good first issue

**Dependências:** VF-002

**Critérios de aceite:**

- [ ] Problema, público-alvo e proposta de valor estão documentados.
- [ ] Fluxo principal do MVP liga produto, estoque, venda e financeiro.
- [ ] Funcionalidades fora do MVP estão explicitamente listadas.
- [ ] Critérios de sucesso da versão 1.0 estão definidos.
- [ ] Nome, tagline e convenções da marca Vincere Flow estão registrados.

## M1 - Catálogo e estoque

Cadastro de produtos, saldo de estoque e trilha auditável de movimentações.

### VF-008 - feat(produtos): modelar produto e persistência

Criar o modelo de produto que sustenta estoque, vendas e indicadores.

**Labels:** type:feature, area:products, priority:P0

**Dependências:** VF-002, VF-005

**Critérios de aceite:**

- [ ] Produto possui id, referência, nome, marca, categoria, custo, preço de venda, estoque mínimo, status e auditoria.
- [ ] Valores monetários usam `BigDecimal` com escala definida.
- [ ] Referência do produto é única e normalizada.
- [ ] Migration cria tabela, índices, constraints e checks necessários.
- [ ] Repository possui teste de persistência para unicidade e campos obrigatórios.

### VF-009 - feat(produtos): implementar cadastro e manutenção de produtos

Permitir criar, consultar, atualizar e ativar ou inativar produtos com regras consistentes.

**Labels:** type:feature, area:products, priority:P0

**Dependências:** VF-006, VF-008

**Critérios de aceite:**

- [ ] `POST /api/v1/produtos` cadastra um produto válido.
- [ ] `GET /api/v1/produtos/{id}` retorna o produto ou 404.
- [ ] `PUT /api/v1/produtos/{id}` atualiza apenas campos permitidos.
- [ ] Ativação e inativação não apagam histórico.
- [ ] Referência duplicada retorna conflito com mensagem clara.
- [ ] Controllers não expõem entidades JPA diretamente.

### VF-010 - feat(produtos): implementar busca, filtros e paginação

Permitir localizar produtos com eficiência sem retornar o catálogo inteiro.

**Labels:** type:feature, area:products, priority:P1

**Dependências:** VF-009

**Critérios de aceite:**

- [ ] `GET /api/v1/produtos` suporta paginação e ordenação.
- [ ] Filtros cobrem referência, nome, marca, categoria e status.
- [ ] Parâmetros inválidos retornam erro de validação.
- [ ] Resposta informa página, tamanho, total de elementos e total de páginas.
- [ ] Consultas relevantes utilizam índices compatíveis com os filtros.

### VF-011 - feat(estoque): modelar saldo e movimentações

Representar o estoque como saldo controlado e trilha imutável de movimentações.

**Labels:** type:feature, area:stock, priority:P0

**Dependências:** VF-005, VF-008

**Critérios de aceite:**

- [ ] Movimentação registra produto, tipo, quantidade, data, origem, observação e auditoria.
- [ ] Tipos iniciais incluem entrada, venda, ajuste, devolução, perda e estorno.
- [ ] Quantidade de uma movimentação é sempre positiva; o tipo define o efeito no saldo.
- [ ] Saldo não pode ficar negativo.
- [ ] Migration cria constraints e índices para produto e data.

### VF-012 - feat(estoque): registrar entradas e ajustes

Permitir aumentar ou corrigir o saldo com rastreabilidade e validação.

**Labels:** type:feature, area:stock, priority:P0

**Dependências:** VF-006, VF-011

**Critérios de aceite:**

- [ ] `POST /api/v1/estoque/movimentacoes` aceita entrada e ajuste autorizado.
- [ ] Operação atualiza saldo e grava movimentação na mesma transação.
- [ ] Produto inexistente ou inativo impede a movimentação.
- [ ] Ajustes exigem motivo textual.
- [ ] Falha em qualquer etapa reverte toda a operação.

### VF-013 - feat(estoque): consultar saldo e histórico

Dar visibilidade ao saldo atual e à origem de cada alteração de estoque.

**Labels:** type:feature, area:stock, priority:P1

**Dependências:** VF-012

**Critérios de aceite:**

- [ ] Endpoint retorna saldo atual por produto.
- [ ] Histórico suporta filtros por produto, tipo e intervalo de datas.
- [ ] Resultados são paginados e ordenados do mais recente para o mais antigo.
- [ ] Cada registro identifica a origem de negócio quando existir.
- [ ] Consulta não permite alteração de movimentações já gravadas.

### VF-014 - feat(estoque): listar produtos abaixo do estoque mínimo

Sinalizar produtos que precisam de reposição.

**Labels:** type:feature, area:stock, priority:P1, good first issue

**Dependências:** VF-009, VF-013

**Critérios de aceite:**

- [ ] Endpoint lista apenas produtos ativos cujo saldo é menor ou igual ao estoque mínimo.
- [ ] Resposta inclui saldo, estoque mínimo e quantidade sugerida para reposição.
- [ ] Consulta suporta paginação e ordenação por criticidade.
- [ ] Cenários sem produtos críticos retornam lista vazia, não erro.

## M2 - Vendas

Venda transacional com múltiplos itens, validações, consultas, cancelamento e proteção contra concorrência.

### VF-015 - feat(vendas): modelar venda e itens

Criar o agregado de venda com valores históricos independentes de alterações futuras no produto.

**Labels:** type:feature, area:sales, priority:P0

**Dependências:** VF-005, VF-008

**Critérios de aceite:**

- [ ] Venda possui número, data, status, subtotal, desconto, total e auditoria.
- [ ] Item registra produto, quantidade, preço unitário, custo unitário e total do item.
- [ ] Preço e custo são copiados para o item no momento da venda.
- [ ] Venda possui ao menos um item e não aceita quantidades nulas ou negativas.
- [ ] Migration garante integridade referencial e precisão monetária.

### VF-016 - feat(vendas): registrar venda com múltiplos itens

Executar o fluxo central do produto: concluir uma venda e baixar o estoque de forma atômica.

**Labels:** type:feature, area:sales, priority:P0

**Dependências:** VF-006, VF-009, VF-011, VF-015

**Critérios de aceite:**

- [ ] `POST /api/v1/vendas` aceita um ou mais itens.
- [ ] Produtos e quantidades são validados antes de qualquer gravação.
- [ ] Venda, itens, saldos e movimentações são persistidos na mesma transação.
- [ ] Totais são calculados no servidor, não confiados ao cliente.
- [ ] Resposta retorna identificação da venda, itens e totais consolidados.
- [ ] Falha em um item reverte toda a venda.

### VF-017 - feat(vendas): validar estoque, preços e descontos

Concentrar e testar as regras que impedem vendas inconsistentes ou economicamente inválidas.

**Labels:** type:feature, area:sales, priority:P0

**Dependências:** VF-016

**Critérios de aceite:**

- [ ] Venda de produto inativo ou sem estoque suficiente é recusada.
- [ ] Itens duplicados são consolidados ou recusados por regra documentada.
- [ ] Desconto não pode tornar o total negativo.
- [ ] Limite de desconto possui regra explícita e configurável.
- [ ] Arredondamento monetário usa estratégia única e documentada.
- [ ] Mensagens de erro identificam o item que causou a rejeição.

### VF-018 - feat(vendas): consultar vendas e seus detalhes

Permitir auditoria e análise das vendas registradas.

**Labels:** type:feature, area:sales, priority:P1

**Dependências:** VF-016, VF-017

**Critérios de aceite:**

- [ ] Listagem suporta período, status e paginação.
- [ ] Detalhe retorna itens, totais, custos históricos e margem bruta.
- [ ] Consultas evitam N+1 e carregamento desnecessário.
- [ ] Intervalos de data inválidos retornam erro de validação.
- [ ] Venda inexistente retorna 404.

### VF-019 - feat(vendas): cancelar venda e estornar estoque

Permitir cancelamento sem apagar histórico e devolver os itens ao estoque.

**Labels:** type:feature, area:sales, priority:P0

**Dependências:** VF-016, VF-017

**Critérios de aceite:**

- [ ] Venda concluída pode ser cancelada uma única vez.
- [ ] Cancelamento altera status e registra data, motivo e responsável.
- [ ] Cada item gera movimentação de estorno no estoque.
- [ ] Operação é atômica e idempotente.
- [ ] Venda cancelada permanece consultável e não pode ser editada.

### VF-020 - feat(estoque): proteger saldo contra vendas concorrentes

Evitar estoque negativo quando duas vendas tentam consumir o mesmo saldo simultaneamente.

**Labels:** type:feature, area:stock, priority:P1

**Dependências:** VF-016

**Critérios de aceite:**

- [ ] Estratégia de concorrência é documentada e implementada.
- [ ] Conflitos retornam erro tratável sem corromper o saldo.
- [ ] Teste reproduz duas transações concorrentes sobre o mesmo produto.
- [ ] Saldo final e movimentações permanecem consistentes.
- [ ] Mecanismo escolhido não bloqueia todo o catálogo desnecessariamente.

## M3 - Financeiro e indicadores

Receitas, despesas, integração com vendas, fluxo de caixa e indicadores comerciais.

### VF-021 - feat(financeiro): modelar categorias e lançamentos

Criar a base financeira para receitas, despesas, pagamentos e estornos.

**Labels:** type:feature, area:finance, priority:P0

**Dependências:** VF-005, VF-002

**Critérios de aceite:**

- [ ] Categoria possui nome, tipo permitido, status e auditoria.
- [ ] Lançamento possui tipo, origem, descrição, categoria, valor, competência, vencimento, pagamento e status.
- [ ] Valores usam `BigDecimal` e devem ser positivos.
- [ ] Origem identifica lançamento manual, venda ou estorno.
- [ ] Migration cria constraints e índices para período, tipo e status.

### VF-022 - feat(financeiro): registrar receitas e despesas manuais

Permitir controlar entradas e saídas não originadas automaticamente por vendas.

**Labels:** type:feature, area:finance, priority:P0

**Dependências:** VF-006, VF-021

**Critérios de aceite:**

- [ ] Endpoint cadastra receita ou despesa com categoria compatível.
- [ ] Status inicial segue regra baseada em vencimento e data de pagamento.
- [ ] Lançamentos podem ser consultados, atualizados dentro das regras e cancelados sem exclusão física.
- [ ] Categorias inativas não podem ser usadas em novos lançamentos.
- [ ] Validação impede datas e valores incoerentes.

### VF-023 - feat(financeiro): integrar lançamentos ao ciclo da venda

Gerar receita automaticamente na venda e estorno financeiro no cancelamento.

**Labels:** type:feature, area:finance, priority:P0

**Dependências:** VF-019, VF-021

**Critérios de aceite:**

- [ ] Venda concluída gera lançamento financeiro vinculado e com valor idêntico ao total.
- [ ] Reprocessamento da mesma venda não duplica receita.
- [ ] Cancelamento gera estorno ou cancela a receita conforme regra documentada.
- [ ] Venda, estoque e financeiro permanecem consistentes na mesma transação.
- [ ] Origem permite navegar do lançamento para a venda relacionada.

### VF-024 - feat(financeiro): consultar fluxo de caixa por período

Apresentar entradas, saídas e saldo financeiro em um intervalo informado.

**Labels:** type:feature, area:finance, priority:P1

**Dependências:** VF-022, VF-023

**Critérios de aceite:**

- [ ] Endpoint aceita data inicial, data final e filtros de status.
- [ ] Resposta informa saldo inicial, receitas, despesas, saldo do período e saldo final.
- [ ] Critério de caixa ou competência está explicitamente definido.
- [ ] Lançamentos cancelados e estornos seguem regra documentada.
- [ ] Cálculos possuem testes com valores e datas limítrofes.

### VF-025 - feat(indicadores): disponibilizar resumo comercial

Converter os dados operacionais em indicadores de gestão comercial.

**Labels:** type:feature, area:analytics, priority:P1

**Dependências:** VF-018, VF-024

**Critérios de aceite:**

- [ ] Resumo por período informa faturamento, despesas, saldo, lucro bruto e margem bruta.
- [ ] Calcula quantidade vendida, ticket médio, preço médio e produtos mais vendidos.
- [ ] Vendas canceladas não contaminam os indicadores.
- [ ] Fórmulas e arredondamentos estão documentados.
- [ ] Consultas possuem limite temporal e desempenho aceitável para o MVP.

## M4 - Qualidade e segurança

Testes, documentação da API, observabilidade, integração contínua e controle de acesso.

### VF-026 - test: configurar testes de integração com Testcontainers

Executar testes contra PostgreSQL real e reproduzível, reduzindo diferenças entre teste e produção.

**Labels:** type:test, area:quality, priority:P0

**Dependências:** VF-004, VF-005

**Critérios de aceite:**

- [ ] Testcontainers inicia PostgreSQL automaticamente na suíte de integração.
- [ ] Flyway aplica migrations no container de teste.
- [ ] Testes não dependem do Docker Compose de desenvolvimento.
- [ ] Dados são isolados entre testes.
- [ ] Comando Maven executa testes unitários e de integração de forma previsível.

### VF-027 - test: cobrir regras críticas com testes automatizados

Proteger o fluxo central contra regressões de estoque, venda e financeiro.

**Labels:** type:test, area:quality, priority:P0

**Dependências:** VF-009, VF-012, VF-016, VF-019, VF-023, VF-026

**Critérios de aceite:**

- [ ] Testes cobrem cadastro duplicado, estoque insuficiente, cálculos, transação, cancelamento e idempotência.
- [ ] Testes de integração verificam banco, migrations e endpoints principais.
- [ ] Cenários felizes e falhas relevantes estão nomeados pelo comportamento esperado.
- [ ] Cobertura não depende apenas de percentual; regras P0 possuem testes explícitos.
- [ ] Suíte completa passa em ambiente limpo.

### VF-028 - docs: documentar a API com OpenAPI e Swagger UI

Tornar os contratos da API compreensíveis e testáveis sem leitura do código-fonte.

**Labels:** type:docs, area:quality, priority:P1

**Dependências:** VF-009, VF-013, VF-018, VF-024, VF-025

**Critérios de aceite:**

- [ ] OpenAPI descreve endpoints, parâmetros, DTOs, status e erros.
- [ ] Swagger UI fica disponível no ambiente autorizado.
- [ ] Exemplos representam o domínio real do Vincere Flow.
- [ ] Campos obrigatórios, formatos e limites são documentados.
- [ ] Contrato gerado está alinhado aos testes de integração.

### VF-029 - ops: adicionar health checks e logs estruturados

Dar visibilidade sobre saúde, falhas e operações importantes da aplicação.

**Labels:** type:infra, area:quality, priority:P1

**Dependências:** VF-004, VF-006

**Critérios de aceite:**

- [ ] Actuator expõe apenas endpoints necessários.
- [ ] Health check diferencia aplicação ativa de aplicação pronta para receber tráfego.
- [ ] Logs incluem correlation id, nível, evento e contexto sem dados sensíveis.
- [ ] Vendas e cancelamentos registram eventos auditáveis.
- [ ] Falhas inesperadas possuem log com contexto suficiente para diagnóstico.

### VF-030 - ci: executar build e testes no GitHub Actions

Bloquear integrações que não compilam ou quebram testes.

**Labels:** type:infra, area:quality, priority:P0

**Dependências:** VF-026, VF-027

**Critérios de aceite:**

- [ ] Workflow executa em pull requests e pushes para `main`.
- [ ] Pipeline configura Java 21, cache Maven, build e testes.
- [ ] Falhas interrompem o workflow com logs claros.
- [ ] Artefato JAR pode ser publicado pelo workflow quando o build passa.
- [ ] README exibe o status do CI.

### VF-031 - security: implementar autenticação e autorização por perfis

Restringir operações da API a usuários autenticados e perfis autorizados.

**Labels:** type:security, area:security, priority:P1

**Dependências:** VF-009, VF-018, VF-022

**Critérios de aceite:**

- [ ] Usuário possui credencial com hash forte, status e perfil.
- [ ] Login emite token com expiração e claims mínimas.
- [ ] Perfis iniciais: administrador, gerente e operador.
- [ ] Operações sensíveis de ajuste, cancelamento e gestão de usuários exigem permissão adequada.
- [ ] Endpoints públicos ficam explicitamente listados.
- [ ] Testes cobrem 401, 403 e acessos permitidos.

### VF-032 - security: revisar validação, segredos e exposição de dados

Executar uma revisão defensiva antes da publicação na internet.

**Labels:** type:security, area:security, priority:P1

**Dependências:** VF-004, VF-029, VF-031

**Critérios de aceite:**

- [ ] Nenhum segredo, token ou credencial está versionado ou aparece em logs.
- [ ] DTOs evitam mass assignment e exposição de campos internos.
- [ ] Entradas possuem limites de tamanho e formato.
- [ ] Dependências passam por verificação de vulnerabilidades conhecida.
- [ ] CORS, headers e documentação pública seguem configuração intencional.
- [ ] Achados e mitigações ficam registrados.

## M5 - Azure e lançamento

Publicação no Azure, entrega contínua, monitoramento, apresentação de portfólio e versão 1.0.0.

### VF-033 - cloud: provisionar PostgreSQL no Azure

Criar o banco gerenciado de produção com custo e acesso controlados.

**Labels:** type:infra, area:azure, priority:P1

**Dependências:** VF-005

**Critérios de aceite:**

- [ ] Azure Database for PostgreSQL Flexible Server é criado no resource group do projeto.
- [ ] Região e camada são compatíveis com o crédito educacional.
- [ ] Acesso de rede é restrito ao necessário.
- [ ] Usuário da aplicação não possui privilégios administrativos desnecessários.
- [ ] Backup, retenção e procedimento de remoção estão documentados.
- [ ] Flyway consegue aplicar migrations em ambiente controlado.

### VF-034 - cloud: publicar a API no Azure App Service

Executar o JAR do Vincere Flow em um serviço gerenciado do Azure.

**Labels:** type:infra, area:azure, priority:P1

**Dependências:** VF-030, VF-033

**Critérios de aceite:**

- [ ] App Service Linux usa runtime Java 21 compatível.
- [ ] Aplicação inicia com perfil `prod` e conecta ao PostgreSQL do Azure.
- [ ] Health check do App Service aponta para endpoint apropriado.
- [ ] HTTPS é obrigatório.
- [ ] Plano escolhido respeita o orçamento do Azure educacional.
- [ ] Procedimento de deploy manual e rollback está documentado.

### VF-035 - cloud: configurar ambiente e segredos de produção

Configurar produção sem incorporar segredos ao repositório ou ao artefato.

**Labels:** type:security, area:azure, priority:P0

**Dependências:** VF-032, VF-033, VF-034

**Critérios de aceite:**

- [ ] URL, usuário e senha do banco são fornecidos por configurações protegidas.
- [ ] Chave de assinatura e demais segredos possuem rotação documentada.
- [ ] Logs não imprimem valores de configuração sensíveis.
- [ ] Configuração de produção usa menor privilégio.
- [ ] Checklist confirma que nenhum segredo chegou ao histórico Git.

### VF-036 - cd: automatizar deploy no Azure com GitHub Actions

Publicar automaticamente uma versão validada após integração na branch principal.

**Labels:** type:infra, area:azure, priority:P1

**Dependências:** VF-030, VF-034, VF-035

**Critérios de aceite:**

- [ ] Workflow de deploy depende do sucesso do CI.
- [ ] Autenticação com Azure evita credenciais permanentes quando possível.
- [ ] Deploy identifica commit e versão publicados.
- [ ] Falha não substitui uma versão saudável silenciosamente.
- [ ] Procedimento de rollback é testado e documentado.
- [ ] Secrets do GitHub contêm somente o indispensável.

### VF-037 - ops: integrar Application Insights e alertas de custo

Monitorar disponibilidade, erros e consumo do crédito Azure.

**Labels:** type:infra, area:azure, priority:P1

**Dependências:** VF-034, VF-035

**Critérios de aceite:**

- [ ] Application Insights recebe telemetria da aplicação.
- [ ] Dashboard exibe requisições, latência, falhas e dependência do banco.
- [ ] Alertas cobrem indisponibilidade e taxa anormal de erros.
- [ ] Budget do Azure possui alertas progressivos antes do esgotamento do crédito.
- [ ] Dados sensíveis não aparecem na telemetria.
- [ ] Runbook explica como diagnosticar falha de aplicação ou banco.

### VF-038 - docs: preparar apresentação de portfólio e dados de demonstração

Apresentar o projeto de forma verificável para recrutadores e avaliadores técnicos.

**Labels:** type:docs, area:azure, priority:P2

**Dependências:** VF-025, VF-028, VF-037

**Critérios de aceite:**

- [ ] README explica problema, arquitetura, stack, regras e como executar.
- [ ] Diagrama mostra API, PostgreSQL, GitHub Actions e Azure.
- [ ] Coleção HTTP ou Postman demonstra o fluxo principal.
- [ ] Dados sintéticos permitem executar uma demonstração sem informações reais.
- [ ] Capturas ou GIF mostram cadastro, entrada, venda, financeiro e indicadores.
- [ ] Limitações e próximos passos são declarados honestamente.

### VF-039 - release: publicar Vincere Flow API v1.0.0

Formalizar a primeira versão utilizável e demonstrável do produto.

**Labels:** type:chore, area:azure, priority:P2

**Dependências:** VF-027, VF-028, VF-030, VF-031, VF-032, VF-036, VF-037, VF-038

**Critérios de aceite:**

- [ ] Todas as issues P0 e P1 da versão estão concluídas ou justificadamente removidas do escopo.
- [ ] CI e deploy passam a partir de uma tag imutável.
- [ ] Release notes descrevem capacidades, limitações e correções.
- [ ] Banco possui backup ou procedimento de restauração validado.
- [ ] Smoke test confirma os fluxos de produto, estoque, venda, financeiro e indicadores.
- [ ] Tag `v1.0.0` e GitHub Release são publicados.

