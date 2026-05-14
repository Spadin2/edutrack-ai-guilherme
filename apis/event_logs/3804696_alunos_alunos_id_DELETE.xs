// Delete Alunos record.
query "alunos/{alunos_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int alunos_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.alunos_id
    }
  }

  response = null
}