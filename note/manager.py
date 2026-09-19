import json
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional

from note.decorators import handle_exceptions, log_execution
from note.models import Note
from datetime import datetime


class NoteManager:
    def __init__(self, filepath: str = "notes.json"):
        # تبدیل مسیر به یک آبجکت Path برای کارکرد راحت‌تر
        self.filepath = Path(filepath)
        self.notes = self._load_notes()

    @handle_exceptions
    @log_execution
    def _load_notes(self) -> List[Note]:
        # اگر فایل وجود نداشت، لیست خالی برگردون
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r") as file:
            data = json.load(file)
            # تبدیل داده‌های دیکشنری به آبجکت‌های Note
            return [Note(**item) for item in data]

    @handle_exceptions
    @log_execution
    def _save_notes(self) -> None:
        # استفاده از self.filepath برای ذخیره‌سازی
        with open(self.filepath, "w") as file:
            json.dump([asdict(note) for note in self.notes], file, indent=4, default=str)

    @handle_exceptions
    @log_execution
    def create_note(self, title: str, content: str) -> Note:
        new_note = Note(title=title, content=content)
        self.notes.append(new_note)
        self._save_notes()
        return new_note

    @handle_exceptions
    @log_execution
    def get_all_notes(self) -> List[Note]:
        return self.notes

    @handle_exceptions
    @log_execution
    def get_note_by_id(self, note_id: str) -> Optional[Note]:
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    @handle_exceptions
    @log_execution
    def delete_note(self, note_id: str) -> bool:
        note = self.get_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self._save_notes()
            return True
        return False

    @handle_exceptions
    @log_execution
    def update_note(self, note_id: str,
                    title: Optional[str] = None,
                    content: Optional[str] = None) -> bool:
        note = self.get_note_by_id(note_id)
        if note:
            if title is not None:
                note.title = title
            if content is not None:
                note.content = content
            
            note.last_modified_at = datetime.now()
            
            self._save_notes()
            return True
        return False

