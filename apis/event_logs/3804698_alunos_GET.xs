// Query all Alunos records
query alunos verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $alunos
  }

  response = $alunos
}