        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def create_tables(self) -> None:
        """Create the notes table if it is missing."""
        # PRIMARY KEY gives each row an ID.
        # NOT NULL prevents missing values in these columns.
        # CHECK prevents a title that contains only spaces.
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                    body TEXT NOT NULL DEFAULT ''
                )
                """
            )

    @staticmethod
    def _validate_text(title: str, body: str) -> tuple[str, str]:
        """Check the input and remove extra spaces around the title."""
        if not isinstance(title, str) or not isinstance(body, str):
            raise TypeError("The title and body must be text.")

        title = title.strip()
        if not title:
            raise ValueError("Please enter a title.")

        return title, body

    def add_note(self, title: str, body: str = "") -> int:
        """Save a new note and return its ID."""
        title, body = self._validate_text(title, body)

        with self._connection() as connection:
            # Pass values separately instead of joining them into the SQL text.
            cursor = connection.execute(
                "INSERT INTO notes (title, body) VALUES (?, ?)",
                (title, body),
            )
            note_id = int(cursor.lastrowid)

        return note_id

    def get_note(self, note_id: int) -> dict | None:
        """Return one note as a dictionary, or None if the ID is not found."""
        with self._connection() as connection:
            row = connection.execute(
                "SELECT id, title, body FROM notes WHERE id = ?",
                (note_id,),
            ).fetchone()

        return dict(row) if row is not None else None

    def get_all_notes(self) -> list[dict]:
        """Return all notes as dictionaries, with larger IDs first."""
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT id, title, body FROM notes ORDER BY id DESC"
            ).fetchall()

        return [dict(row) for row in rows]

    def update_note(self, note_id: int, title: str, body: str = "") -> bool:
        """Update a note and return True, or False if its ID is not found."""
        title, body = self._validate_text(title, body)

        with self._connection() as connection:
            cursor = connection.execute(
                "UPDATE notes SET title = ?, body = ? WHERE id = ?",
                (title, body, note_id),
            )
            updated = cursor.rowcount > 0

        return updated

    def delete_note(self, note_id: int) -> bool:
        """Delete one note and return True, or False if its ID is not found."""
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM notes WHERE id = ?",
                (note_id,),
            )
            deleted = cursor.rowcount > 0

        return deleted


def main() -> None:
    """Demonstrate the four basic database actions using a separate demo file."""
    db = Database(DEMO_DATABASE_PATH)
    print(f"Demo database: {db.path}")

    # CREATE: Insert a new record and remember only its ID.
    note_id = db.add_note("Example note", "This record was saved locally.")
    print(f"\nCreated note {note_id}.")

    # READ: Retrieve the saved record.
    print("Saved record:", db.get_note(note_id))

    # UPDATE: Change this demonstration's new record.
    db.update_note(note_id, "Updated example", "The database saved this change.")
    print("Updated record:", db.get_note(note_id))

    # DELETE: Remove only the record created during this demonstration.
    print("Deleted demo record:", db.delete_note(note_id))
    print("Read after deletion:", db.get_note(note_id))
    print("\nDemo finished. Other records were left unchanged.")


if __name__ == "__main__":
    main()

