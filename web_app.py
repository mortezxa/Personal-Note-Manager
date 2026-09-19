from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from note.manager import NoteManager
from fastapi import HTTPException


app = FastAPI(title="Personal Note Manager")

templates = Jinja2Templates(directory="templates")

# ساخت منیجر
manager = NoteManager()

@app.get("/", response_class=HTMLResponse)
def list_notes(request: Request):
    # دریافت لیست یادداشت‌ها (اگر نال بود لیست خالی برگردان)
    notes = manager.get_all_notes() or []
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "notes": notes}
    )

@app.post("/notes/create")
async def create_note(title: str = Form(...), content: str = Form(...)):
    manager.create_note(title=title, content=content)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/notes/delete/{note_id}")
async def delete_note(note_id: str):
    manager.delete_note(note_id)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/notes/edit/{note_id}", response_class=HTMLResponse)
async def edit_note_page(request: Request, note_id: str):
    note = manager.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="یادداشت پیدا نشد")
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"request": request, "note": note}
    )

@app.post("/notes/update/{note_id}")
async def update_note(
    note_id: str,
    title: str = Form(...),
    content: str = Form(...)
):
    success = manager.update_note(note_id=note_id, title=title, content=content)
    if not success:
        raise HTTPException(status_code=404, detail="یادداشت پیدا نشد")
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)