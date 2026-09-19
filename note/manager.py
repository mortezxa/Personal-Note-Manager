import os
import json
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from note.decorators import handle_exceptions, log_execution
from note.models import Note

class NoteManager:
    def __init__(self, filepath: str = "notes.json"):
        self.filepath = Path(filepath)
        self.notes = self._load_notes()

    @handle_exceptions
    @log_execution
    def _load_notes(self) -> List[Note]:
        if not os.path.exists(self.filepath):
            return []

        with open(self.filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []

            loaded_notes = []
            for item in data:
                # تبدیل تاریخ‌های رشته‌ای به آبجکت datetime
                if isinstance(item.get('created_at'), str):
                    item['created_at'] = datetime.fromisoformat(item['created_at'])
                if isinstance(item.get('last_modified_at'), str):
                    item['last_modified_at'] = datetime.fromisoformat(item['last_modified_at'])
                
                # اطمینان از اینکه ID حتماً UUID است
                if isinstance(item.get('id'), str):
                    item['id'] = UUID(item['id'])
                
                loaded_notes.append(Note(**item))
            return loaded_notes

    @handle_exceptions
    @log_execution
    def _save_notes(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as file:
            # موقع ذخیره، UUID رو به رشته تبدیل کن تا JSON خراب نشه
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
        # تبدیل رشته به UUID برای مقایسه دقیق
        target_uuid = UUID(note_id)
        for note in self.notes:
            if note.id == target_uuid:
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
    def update_note(self, note_id: str, title: Optional[str] = None, content: Optional[str] = None) -> bool:
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
