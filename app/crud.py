import re

from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import Note, Link, Tag


def normalize_tag(name: str) -> str:
    return " ".join(name.strip().lower().split())


def get_or_create_tag(db: Session, name: str) -> Tag | None:
    normalized = normalize_tag(name)

    if not normalized:
        return None

    tag = (
        db.query(Tag)
        .filter(func.lower(Tag.name) == normalized)
        .first()
    )

    if tag:
        return tag

    tag = Tag(name=normalized)
    db.add(tag)

    try:
        db.flush()
        return tag
    except IntegrityError:
        db.rollback()
        return (
            db.query(Tag)
            .filter(func.lower(Tag.name) == normalized)
            .first()
        )


def get_note(db: Session, note_id: int) -> Note | None:
    return (
        db.query(Note)
        .options(
            selectinload(Note.tags),
            selectinload(Note.outgoing_links).selectinload(Link.target),
            selectinload(Note.incoming_links).selectinload(Link.source),
        )
        .filter(Note.id == note_id)
        .first()
    )


def get_all_notes(
    db: Session,
    tag: str | None = None,
    keyword: str | None = None,
) -> list[Note]:
    query = db.query(Note).options(selectinload(Note.tags))

    if tag and tag.strip():
        normalized = normalize_tag(tag)
        query = query.join(Note.tags).filter(
            func.lower(Tag.name) == normalized
        )

    if keyword and keyword.strip():
        search = f"%{keyword.strip()}%"
        query = query.filter(
            or_(
                Note.title.ilike(search),
                Note.content.ilike(search),
            )
        )

    return query.order_by(Note.id).all()


def create_note(
    db: Session,
    title: str,
    content: str,
    tags: list[str],
) -> Note:
    title = title.strip()

    if not title:
        raise ValueError("Title cannot be empty")

    existing = db.query(Note).filter(Note.title == title).first()
    if existing:
        raise ValueError("A note with this title already exists")

    note = Note(title=title, content=content)
    db.add(note)

    try:
        db.flush()

        for name in tags:
            tag = get_or_create_tag(db, name)
            if tag and all(t.name != tag.name for t in note.tags):
                note.tags.append(tag)

        # Resolve [[Note Title]] references to existing notes.
        titles = set(
            re.findall(r"\[\[([^\[\]]+)\]\]", content or "")
        )

        for referenced_title in titles:
            referenced_title = referenced_title.strip()
            if not referenced_title:
                continue

            target = (
                db.query(Note)
                .filter(
                    func.lower(Note.title) ==
                    referenced_title.lower()
                )
                .first()
            )

            if target and target.id != note.id:
                exists = (
                    db.query(Link)
                    .filter(
                        Link.source_id == note.id,
                        Link.target_id == target.id,
                    )
                    .first()
                )

                if not exists:
                    db.add(
                        Link(
                            source_id=note.id,
                            target_id=target.id,
                        )
                    )

        db.commit()
        return get_note(db, note.id)

    except Exception:
        db.rollback()
        raise


def create_link(
    db: Session,
    source_id: int,
    target_id: int,
) -> Link:
    if source_id == target_id:
        raise ValueError("A note cannot link to itself")

    source = db.query(Note).filter(Note.id == source_id).first()
    target = db.query(Note).filter(Note.id == target_id).first()

    if not source or not target:
        raise LookupError("Source or target note was not found")

    existing = (
        db.query(Link)
        .filter(
            Link.source_id == source_id,
            Link.target_id == target_id,
        )
        .first()
    )

    if existing:
        raise ValueError("This link already exists")

    link = Link(source_id=source_id, target_id=target_id)
    db.add(link)
    db.commit()
    return link


def get_tag_suggestions(db: Session) -> list[str]:
    tags = db.query(Tag).order_by(Tag.name).all()
    return [tag.name for tag in tags]