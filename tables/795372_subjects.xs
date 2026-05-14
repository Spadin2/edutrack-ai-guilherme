// Subjects table for EduTrack AI
table subjects {
  auth = false

  schema {
    int id {
      description = "Unique identifier for the subject"
    }

    timestamp created_at?=now {
      description = "Timestamp when the subject was created"
      visibility = "private"
    }

    timestamp timestamp updated_at {
      description = "Timestamp when the subject was last updated"
    }

    text name filters=trim {
      description = "Name of the subject (discipline/matter)"
      required = true
    }

    text description? filters=trim {
      description = "Detailed description of the subject"
    }

    text color? filters=trim {
      description = "Hex color code for the subject (e.g., #FF5733)"
    }

    int user_id {
      table = "user"
      description = "ID of the user who owns this subject"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "name", op: "asc"}]}
  ]
}