# Database Schema

This project uses a SQLite database to store user information and Kanban board data.

## Tables

### `users`

Stores user credentials.

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key |
| `username` | TEXT | Unique username |
| `password` | TEXT | Bcrypt hashed password |

### `boards`

Stores the Kanban board data for each user.

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key |
| `user_id` | INTEGER | Foreign Key referencing `users(id)` |
| `data` | TEXT | JSON representation of `BoardData` |
| `updated_at` | DATETIME | Timestamp of the last update |

## JSON Data Structure

The `data` column in the `boards` table stores a JSON object with the following structure (matching `frontend/src/lib/kanban.ts`):

```json
{
  "columns": [
    {
      "id": "string",
      "title": "string",
      "cardIds": ["string"]
    }
  ],
  "cards": {
    "card-id": {
      "id": "string",
      "title": "string",
      "details": "string"
    }
  }
}
```

## Implementation Notes

- The database file will be named `kanban.db` and located in the project root (or as configured in the backend).
- The backend will use `sqlite3` (or an async wrapper) to interact with the database.
- Upon first login, if no board exists for the user, a default board will be created using `initialData`.
