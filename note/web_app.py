from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from note.manager import NoteManager

app = FastAPI(title="Personal Note Manager")

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

manager = NoteManager()


@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/notes", status_code=status.HTTP_302_FOUND)


@app.get("/notes", response_class=HTMLResponse)
async def list_notes(request: Request) -> HTMLResponse:
    notes = manager.get_all_notes() or []
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "notes": notes},
    )


@app.post("/notes")
@app.post("/notes/create")
async def create_note(
    title: str = Form(...),
    content: str = Form(...),
) -> RedirectResponse:
    manager.create_note(title=title, content=content)
    return RedirectResponse(url="/notes", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/notes/{note_id}", response_class=HTMLResponse)
async def show_note(request: Request, note_id: str) -> HTMLResponse:
    note = manager.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"request": request, "note": note},
    )


@app.get("/notes/edit/{note_id}", response_class=HTMLResponse)
async def edit_note_page(request: Request, note_id: str) -> HTMLResponse:
    note = manager.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"request": request, "note": note},
    )


@app.post("/notes/update/{note_id}")
async def update_note(
    note_id: str,
    title: str = Form(...),
    content: str = Form(...),
) -> RedirectResponse:
    success = manager.update_note(note_id=note_id, title=title, content=content)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return RedirectResponse(url="/notes", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/notes/delete/{note_id}")
async def delete_note(note_id: str) -> RedirectResponse:
    manager.delete_note(note_id)
    return RedirectResponse(url="/notes", status_code=status.HTTP_303_SEE_OTHER)