# Specification: add-subjects

## Requirement

### Create Subject Management System

O sistema deve permitir que usuários autenticados gerenciem disciplinas (matérias) associadas à sua conta.

#### Scenario 1: Create a new subject

- **Given** que o usuário está autenticado
- **When** o usuário envia uma requisição POST para criar uma disciplina com nome válido
- **Then** uma nova disciplina deve ser criada no banco de dados
- **And** a resposta deve retornar os dados da disciplina criada
- **And** o campo `user_id` deve ser automaticamente associado ao usuário autenticado

#### Scenario 2: List all subjects for a user

- **Given** que o usuário está autenticado
- **When** o usuário envia uma requisição GET para listar suas disciplinas
- **Then** todas as disciplinas do usuário devem ser retornadas
- **And** a lista deve estar ordenada por nome

#### Scenario 3: Get a single subject

- **Given** que o usuário está autenticado
- **When** o usuário envia uma requisição GET para buscar uma disciplina específica
- **And** a disciplina pertence ao usuário
- **Then** os dados da disciplina devem ser retornados

#### Scenario 4: Update a subject

- **Given** que o usuário está autenticado
- **When** o usuário envia uma requisição PATCH para atualizar uma disciplina
- **And** a disciplina pertence ao usuário
- **Then** a disciplina deve ser atualizada com os novos dados
- **And** a resposta deve retornar os dados atualizados

#### Scenario 5: Delete a subject

- **Given** que o usuário está autenticado
- **When** o usuário envia uma requisição DELETE para excluir uma disciplina
- **And** a disciplina pertence ao usuário
- **Then** a disciplina deve ser removida do banco de dados
- **And** a resposta deve confirmar a exclusão

#### Scenario 6: Validation - Empty name

- **Given** que o usuário está autenticado
- **When** o usuário tenta criar uma disciplina com nome vazio
- **Then** um erro de validação deve ser retornado
- **And** a disciplina não deve ser criada

#### Scenario 7: Validation - Unauthorized access

- **Given** que o usuário está autenticado
- **When** o usuário tenta acessar uma disciplina de outro usuário
- **Then** um erro de acesso não autorizado deve ser retornado

## Data Model

### Subject Table

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | int/uuid | yes | Primary key |
| name | string | yes | Subject name (max 100 chars) |
| description | string | no | Optional description (max 500 chars) |
| color | string | no | Hex color code for UI (e.g., "#FF5733") |
| user_id | int/uuid | yes | Foreign key to users table |
| created_at | datetime | yes | Auto-generated timestamp |
| updated_at | datetime | yes | Auto-generated timestamp |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/subjects | Create a new subject |
| GET | /api/subjects | List all subjects for user |
| GET | /api/subjects/{id} | Get a single subject |
| PATCH | /api/subjects/{id} | Update a subject |
| DELETE | /api/subjects/{id} | Delete a subject |