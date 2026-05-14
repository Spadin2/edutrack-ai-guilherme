# Change: add-subjects

## Why:
O sistema EduTrack AI precisa gerenciar disciplinas (matérias) que os usuários podem criar e associar às suas tarefas. Atualmente, não existe uma forma de organizar disciplinas no sistema, o que limita a organização do conteúdo educacional.

## What:
Criar a funcionalidade de disciplinas (subjects) no sistema, permitindo que usuários criem, editem, listem e excluam disciplinas. Cada disciplina deve ter um nome, descrição opcional, cor para identificação visual, e associação com o usuário.

## Impact:
- Nova tabela `subjects` no banco de dados
- APIs REST para CRUD de disciplinas
- Integração com tarefas existentes (cada tarefa pode ter uma disciplina associada)
- Interface de usuário para gerenciamento de disciplinas