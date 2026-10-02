import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from note.decorators import handle_exceptions, log_execution
from note.logger import logger
from note.models import Note


class NoteManager:
    def __init__(self, filepath: str = "notes.json") -> None:
        self.filepath = Path(filepath)
        loaded = self._load_notes()
        self.notes: list[Note] = loaded if loaded is not None else []

    @handle_exceptions
    @log_execution
    def _load_notes(self) -> list[Note]:
        if not self.filepath.exists():
            return []

        with open(self.filepath, encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON format in {self.filepath}")
                return []

        if not isinstance(data, list):
            return []

        return [Note.from_dict(item) for item in data if isinstance(item, dict)]

    @handle_exceptions
    @log_execution
    def _save_notes(self) -> bool:
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(
                [note.to_dict() for note in self.notes],
                file,
                indent=4,
                ensure_ascii=False,
            )
        logger.info(f"Successfully saved {len(self.notes)} notes to {self.filepath}")
        return True

    @handle_exceptions
    @log_execution
    def create_note(self, title: str, content: str) -> Note:
        new_note = Note(title=title, content=content)
        self.notes.append(new_note)
        self._save_notes()
        logger.info(f"Created new note: Note(id={new_note.id}, title='{title}')")
        return new_note

    @handle_exceptions
    @log_execution
    def get_all_notes(self) -> list[Note]:
        return list(self.notes)

    @handle_exceptions
    @log_execution
    def get_note_by_id(self, note_id: str | UUID) -> Note | None:
        target_id = str(note_id).strip()
        for note in self.notes:
            if str(note.id) == target_id:
                return note
        return None

    @handle_exceptions
    @log_execution
    def update_note(
        self,
        note_id: str | UUID,
        title: str | None = None,
        content: str | None = None,
    ) -> bool:
        note = self.get_note_by_id(note_id)
        if not note:
            return False

        if title is not None and title.strip():
            note.title = title
        if content is not None and content.strip():
            note.content = content
        note.updated_at = datetime.now(timezone.utc)
        self._save_notes()
        logger.info(f"Updated note with ID: {note.id}")
        return True

    @handle_exceptions
    @log_execution
    def delete_note(self, note_id: str | UUID) -> bool:
        note = self.get_note_by_id(note_id)
        if not note:
            return False

        self.notes.remove(note)
        self._save_notes()
        logger.info(f"Deleted note with ID: {note.id}")
        return True

    @handle_exceptions
    @log_execution
    def search_notes(self, query: str) -> list[Note]:
        cleaned_query = query.strip().lower()
        if not cleaned_query:
            return []
        return [
            note
            for note in self.notes
            if cleaned_query in note.title.lower()
            or cleaned_query in note.content.lower()
        ]