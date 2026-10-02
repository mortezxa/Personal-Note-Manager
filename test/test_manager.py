from pathlib import Path
from uuid import uuid4

import pytest

from note.decorators import handle_exceptions, log_execution
from note.manager import NoteManager
from note.models import Note


@pytest.fixture
def temp_manager(tmp_path: Path) -> NoteManager:
    test_file = tmp_path / "test_notes.json"
    return NoteManager(filepath=str(test_file))


def test_note_model_conversion() -> None:
    uid = uuid4()
    note = Note(
        id=uid,  # type: ignore[arg-type]
        title="Model Test",
        content="Body",
        created_at="2025-06-01T12:00:00",  # type: ignore[arg-type]
        updated_at="2025-06-01T12:30:00",  # type: ignore[arg-type]
    )
    assert isinstance(note.id, str)
    data = note.to_dict()
    assert data["title"] == "Model Test"
    restored = Note.from_dict(data)
    assert restored.id == note.id
    assert restored.title == "Model Test"


def test_create_and_list_notes(temp_manager: NoteManager) -> None:
    note = temp_manager.create_note("Test Title", "Test Content")
    assert note.title == "Test Title"
    assert note.content == "Test Content"
    notes = temp_manager.get_all_notes()
    assert len(notes) == 1
    assert notes[0].id == note.id


def test_get_note_by_id(temp_manager: NoteManager) -> None:
    created = temp_manager.create_note("Title", "Content")
    found = temp_manager.get_note_by_id(created.id)
    assert found is not None
    assert found.title == "Title"

    missing = temp_manager.get_note_by_id("non-existent-id")
    assert missing is None


def test_update_note(temp_manager: NoteManager) -> None:
    note = temp_manager.create_note("Old Title", "Old Content")
    old_updated_at = note.updated_at

    success = temp_manager.update_note(
        note.id, title="New Title", content="New Content"
    )
    assert success is True

    updated = temp_manager.get_note_by_id(note.id)
    assert updated is not None
    assert updated.title == "New Title"
    assert updated.content == "New Content"
    assert updated.updated_at >= old_updated_at

    assert temp_manager.update_note("invalid-id", title="X") is False


def test_delete_note(temp_manager: NoteManager) -> None:
    note = temp_manager.create_note("To Delete", "Content")

    success = temp_manager.delete_note(note.id)
    assert success is True
    assert len(temp_manager.get_all_notes()) == 0

    fail = temp_manager.delete_note("invalid-id")
    assert fail is False


def test_search_notes(temp_manager: NoteManager) -> None:
    temp_manager.create_note("Python Course", "Advanced decorators and OOP")
    temp_manager.create_note("Shopping List", "Milk and bread")

    by_title = temp_manager.search_notes("python")
    assert len(by_title) == 1
    assert by_title[0].title == "Python Course"

    by_content = temp_manager.search_notes("decorators")
    assert len(by_content) == 1

    assert temp_manager.search_notes("") == []
    assert temp_manager.search_notes("nonexistent") == []


def test_persistence_and_corrupted_json(tmp_path: Path) -> None:
    json_file = tmp_path / "persist.json"
    manager1 = NoteManager(filepath=str(json_file))
    created = manager1.create_note("Persistent", "Saved to disk")

    manager2 = NoteManager(filepath=str(json_file))
    assert len(manager2.get_all_notes()) == 1
    assert manager2.get_all_notes()[0].id == created.id

    # تست فایل JSON خراب
    json_file.write_text("{invalid json", encoding="utf-8")
    manager3 = NoteManager(filepath=str(json_file))
    assert manager3.get_all_notes() == []

    # تست فایل JSON که لیست نیست
    json_file.write_text('{"a": 1}', encoding="utf-8")
    manager4 = NoteManager(filepath=str(json_file))
    assert manager4.get_all_notes() == []


def test_decorators_exception_handling() -> None:
    @handle_exceptions
    @log_execution
    def faulty_function() -> None:
        raise ValueError("Simulated failure")

    assert faulty_function() is None