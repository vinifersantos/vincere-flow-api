# ADR 0001 - Adotar monólito modular

## Status

Aceito.

## Contexto

O projeto é desenvolvido inicialmente por uma pessoa e precisa ensinar Java, Spring Boot, banco, testes e Azure sem introduzir complexidade distribuída prematura.

## Decisão

Usar uma aplicação Spring Boot organizada por domínio, com um PostgreSQL e transações locais.

## Consequências

### Positivas

- Desenvolvimento e depuração mais simples.
- Transação consistente entre venda, estoque e financeiro.
- Menor custo no Azure educacional.
- Deploy e observabilidade centralizados.

### Negativas

- Exige disciplina para preservar limites entre módulos.
- Escalabilidade independente por módulo não existe no início.

A separação em serviços só será reavaliada quando houver necessidade mensurável.
