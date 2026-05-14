// Create a new subject for the authenticated user
query "subjects" verb=POST {
  api_group = "Subjects"
  auth = ""

  input {
    text name filters=trim {
      description = "Subject name"
      required = true
    }

    text description? filters=trim {
      description = "Optional subject description"
    }

    text color? filters=trim {
      description = "Optional color code for the subject, e.g. #FF5733"
    }
  }

  stack {
    db.add "subjects" {
      data = {
        name       : $input.name
        description: $input.description
        color      : $input.color
        user_id    : $auth.id
        updated_at : now
      }
    } as $new_subject
  }

  response = $new_subject
}
