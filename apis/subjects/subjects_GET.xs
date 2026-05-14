// List all subjects belonging to the authenticated user
query "subjects" verb=GET {
  api_group = "Subjects"
  auth = ""

  input {
  }

  stack {
    db.query "subjects" {
      where = $db.subjects.user_id == $auth.id
      sort = {subjects.name: "asc"}
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
}
