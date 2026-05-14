// Update an existing subject owned by the authenticated user
query "subjects/{subject_id}" verb=PATCH {
  api_group = "Subjects"
  auth = ""

  input {
    int subject_id {
      description = "Subject ID"
    }

    text name? filters=trim {
      description = "Updated subject name"
    }

    text description? filters=trim {
      description = "Updated subject description"
    }

    text color? filters=trim {
      description = "Updated subject color code"
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
          value = "You are not authorized to update this subject."
        }
      }
    }

    var $payload {
      value = {
        name       : $input.name  || $subject.name
        description: $input.description || $subject.description
        color      : $input.color || $subject.color
        updated_at : now
      }
    }

    db.patch "subjects" {
      field_name  = "id"
      field_value = $input.subject_id
      data        = $payload
    } as $updated_subject
  }

  response = $updated_subject
}
