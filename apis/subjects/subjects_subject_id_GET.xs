// Retrieve a specific subject owned by the authenticated user
query "subjects/{subject_id}" verb=GET {
  api_group = "Subjects"
  auth = ""

  input {
    int subject_id {
      description = "Subject ID"
    }
  }

  stack {
    db.get "subjects" {
      field_name  = "id"
      field_value = $input.subject_id
    } as $subject

    conditional {
      if ($subject == null) {
        throw {
          name  = "notfound"
          value = "Subject not found."
        }
      }

      if ($subject.user_id != $auth.id) {
        throw {
          name  = "accessdenied"
          value = "You are not authorized to access this subject."
        }
      }
    }
  }

  response = $subject
}
