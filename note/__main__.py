import typer
from note.manager import NoteManager
from typing import Optional

app = typer.Typer(help="Personal Note Manager CLI")
manager = NoteManager()

@app.command()
def create(title: str, content: str):
    """ایجاد یک یادداشت جدید"""
    note = manager.create_note(title, content)
    typer.echo(f"Note created with ID: {note.id}")

@app.command()
def list():
    """نمایش لیست یادداشت‌ها"""
    notes = manager.get_all_notes()
    for note in notes:
        typer.echo(f"{note.id} | {note.title} (Updated: {note.last_modified_at})")

@app.command()
def delete(note_id: str):
    """حذف یادداشت با ID"""
    if manager.delete_note(note_id):
        typer.echo("Note deleted successfully.")
    else:
        typer.echo("Note not found.")

if __name__ == "__main__":
    app()
