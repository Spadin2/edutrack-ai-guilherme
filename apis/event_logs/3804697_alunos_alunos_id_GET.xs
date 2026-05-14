// Get Alunos record
query "alunos/{alunos_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int alunos_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.alunos_id
    } as $alunos
  
    precondition ($alunos != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $alunos
}