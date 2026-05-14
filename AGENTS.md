# AGENTS.md

## Regras do OpenSpec

- Sempre seguir o fluxo Spec-Driven Development (SDD)
- Criar mudanças dentro de `openspec/changes/`
- Toda mudança deve conter:
  - `proposal.md`
  - `specs/spec.md`
  - `tasks.md`

## Estrutura obrigatória

### proposal.md
Deve conter:
- # Change:
- ## Why:
- ## What Changes:
- ## Impact:

### spec.md
Deve conter:
- ### Requirement:
- #### Scenario:

### tasks.md
- Todas as tarefas devem estar em inglês
- Apenas tarefas solicitadas pelo usuário
- Não adicionar frontend, testes ou APIs sem solicitação

## Responsabilidade da IA

A IA pode:
- Criar/editar arquivos `.xs`
- Criar proposal.md
- Criar spec.md
- Criar tasks.md

A IA NÃO pode:
- Fazer deploy
- Fazer push automático para Xano
- Fazer sync automático
- Executar `push_all_changes_to_xano`

## Fluxo OpenSpec

1. `/opsx:new`
2. `/opsx:continue`
3. `/opsx:apply`
4. `/opsx:archive`

## Padrões XanoScript

- Arquivos `.xs` devem ser criados na pasta correta
- Seguir sintaxe válida do XanoScript
- Validar índices e schemas antes do push