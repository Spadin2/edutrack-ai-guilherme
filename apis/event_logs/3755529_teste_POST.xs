// Add teste record
query teste verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = "teste"
    }
  }

  stack {
    db.add teste {
      data = {created_at: "now"}
    } as $teste
  }

  response = $teste
}