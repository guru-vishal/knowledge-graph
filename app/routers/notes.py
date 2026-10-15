from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud
from app.models import Note
from app.schemas import (
    NoteCreate,
    NoteLinkRequest,
    NoteResponse,
    NoteSummary,
)

router = APIRouter(prefix="/notes", tags=["Notes"])


def summary(note: Note) -> NoteSummary:
    return NoteSummary(
        id=note.id,
        title=note.title,
        tags=[tag.name for tag in note.tags],
    )


def serialize_note(note: Note) -> NoteResponse:
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        tags=[tag.name for tag in note.tags],
        linked_notes=[
            summary(link.target)
            for link in note.outgoing_links
        ],
        backlinks=[
            summary(link.source)
            for link in note.incoming_links
        ],
    )


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    try:
        note = crud.create_note(
            db,
            payload.title,
            payload.content,
            payload.tags,
        )
        return serialize_note(note)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A note with this title already exists",
        )


@router.get("/", response_model=list[NoteResponse])
def list_notes(
    tag: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    notes = crud.get_all_notes(db, tag=tag, keyword=keyword)
    return [serialize_note(note) for note in notes]


@router.get("/tags/suggestions", response_model=list[str])
def tag_suggestions(db: Session = Depends(get_db)):
    return crud.get_tag_suggestions(db)


@router.get("/{note_id}", response_model=NoteResponse)
def note_details(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return serialize_note(note)


@router.patch("/{note_id}/link", status_code=201)
def link_notes(
    note_id: int,
    payload: NoteLinkRequest,
    db: Session = Depends(get_db),
):
    try:
        crud.create_link(db, note_id, payload.target_id)
        return {
            "message": "Notes linked successfully",
            "source_id": note_id,
            "target_id": payload.target_id,
        }
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="The link already exists or is invalid",
        )