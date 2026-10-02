import sys

import typer
import uvicorn

from note.manager import NoteManager

app = typer.Typer(help="Manage your notes efficiently\n\nPersonal Note Manager")
manager = NoteManager()


@app.command()
def create(
    title: str | None = typer.Option(None, "--title", "-t", help="Note title"),
    content: str | None = typer.Option(None, "--content", "-c", help="Note content"),
) -> None:
    """Create a new note interactively."""
    typer.echo("Creating a new note")
    if title is None:
        title = typer.prompt("Enter note title")

    if content is None:
        typer.echo("Enter note content (press Ctrl+C when finished):")
        lines: list[str] = []
        try:
            for line in sys.stdin:
                lines.append(line.rstrip("\r\n"))
        except KeyboardInterrupt:
            pass
        content = "\n".join(lines).strip()
        if not content:
            content = typer.prompt("Enter note content")

    note = manager.create_note(title=title, content=content)
    if note:
        typer.echo(f"✓ Note created successfully with ID: {note.id}")
    else:
        typer.echo("Failed to create note.")


@app.command(name="list")
def list_notes() -> None:
    """List all notes."""
    notes = manager.get_all_notes()
    if not notes:
        typer.echo("No notes found")
        return

    typer.echo("Your Notes")
    typer.echo(f"{'ID':<38} | {'Title':<20} | {'Created':<16} | {'Updated':<16}")
    typer.echo("-" * 98)
    for note in notes:
        created = note.created_at.strftime("%Y-%m-%d %H:%M")
        updated = note.updated_at.strftime("%Y-%m-%d %H:%M")
        typer.echo(f"{note.id:<38} | {note.title:<20} | {created:<16} | {updated:<16}")


@app.command()
def show(note_id: str) -> None:
    """Show details of a specific note."""
    note = manager.get_note_by_id(note_id)
    if not note:
        typer.echo(f"Error: Note with ID '{note_id}' not found.")
        raise typer.Exit(code=1)

    typer.echo(f"ID:         {note.id}")
    typer.echo(f"Title:      {note.title}")
    typer.echo(f"Created At: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    typer.echo(f"Updated At: {note.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    typer.echo("-" * 40)
    typer.echo(note.content)


@app.command()
def update(
    note_id: str,
    title: str | None = typer.Option(None, "--title", "-t", help="New title"),
    content: str | None = typer.Option(None, "--content", "-c", help="New content"),
) -> None:
    """Update an existing note."""
    note = manager.get_note_by_id(note_id)
    if not note:
        typer.echo(f"Error: Note with ID '{note_id}' not found.")
        raise typer.Exit(code=1)

    typer.echo(f"Current Title:   {note.title}")
    typer.echo(f"Current Content: {note.content}")

    if title is None and content is None:
        new_title = typer.prompt(
            "Enter new title (leave blank to keep current)",
            default=note.title,
        )
        new_content = typer.prompt(
            "Enter new content (leave blank to keep current)",
            default=note.content,
        )
    else:
        new_title = title if title is not None else note.title
        new_content = content if content is not None else note.content

    if manager.update_note(note_id, title=new_title, content=new_content):
        typer.echo("✓ Note updated successfully.")
    else:
        typer.echo("Failed to update note.")


@app.command()
def delete(
    note_id: str,
    force: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
) -> None:
    """Delete a note."""
    note = manager.get_note_by_id(note_id)
    if not note:
        typer.echo(f"Error: Note with ID '{note_id}' not found.")
        raise typer.Exit(code=1)

    if not force:
        confirmed = typer.confirm(
            f"Are you sure you want to delete note with ID {note_id}?"
        )
        if not confirmed:
            typer.echo("Deletion cancelled.")
            return

    if manager.delete_note(note_id):
        typer.echo("✓ Note deleted successfully.")
    else:
        typer.echo("Failed to delete note.")


@app.command()
def search(query: str) -> None:
    """Search notes by title or content."""
    results = manager.search_notes(query)
    if not results:
        typer.echo(f"No notes found matching '{query}'.")
        return

    typer.echo(f"Found {len(results)} matching note(s):")
    for note in results:
        typer.echo(f"{note.id} | {note.title}")


@app.command()
def web(
    port: int = typer.Option(8000, "--port", "-p", help="Port to run web server on"),
) -> None:
    """Run the web application."""
    uvicorn.run("note.web_app:app", host="127.0.0.1", port=port)


if __name__ == "__main__":
    app()