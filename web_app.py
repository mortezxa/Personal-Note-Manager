from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from note.manager import NoteManager

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
