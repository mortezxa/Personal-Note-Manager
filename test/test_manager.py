import pytest

from note.manager import NoteManager


@pytest.fixture
def temp_manager(tmp_path):
    """ایجاد محیط ایزوله برای هر تست"""
    test_file = tmp_path / "test_notes.json"
    return NoteManager(filepath=str(test_file))

def test_create_note(temp_manager):
    note = temp_manager.create_note("Test Title", "Test Content")
    assert note.title == "Test Title"
    assert len(temp_manager.get_all_notes()) == 1

def test_get_note_by_id(temp_manager):
    # ایجاد یک یادداشت برای تست
    created = temp_manager.create_note("Title", "Content")

    # تست پیدا کردن یادداشت موجود
    found = temp_manager.get_note_by_id(created.id)
    assert found is not None
    assert found.title == "Title"

    # تست پیدا نشدن یادداشت ناموجود
    missing = temp_manager.get_note_by_id("non-existent-id")
    assert missing is None

def test_update_note(temp_manager):
    # ایجاد اولیه
    note = temp_manager.create_note("Old Title", "Old Content")

    # آپدیت موفقیت‌آمیز
    success = temp_manager.update_note(note.id,
                                       title="New Title", content="New Content")
    assert success is True

    # بررسی تغییرات
    updated = temp_manager.get_note_by_id(note.id)
    assert updated.title == "New Title"
    assert updated.content == "New Content"

def test_delete_note(temp_manager):
    # ایجاد و حذف
    note = temp_manager.create_note("To Delete", "Content")

    # حذف موفق
    success = temp_manager.delete_note(note.id)
    assert success is True
    assert len(temp_manager.get_all_notes()) == 0

    # تست حذف چیزی که وجود نداره (باید False برگردونه)
    fail = temp_manager.delete_note("invalid-id")
    assert fail is False
