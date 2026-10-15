from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Note, Link
from app.schemas import GraphNode, GraphEdge, GraphResponse

router = APIRouter(prefix="/graph", tags=["Graph"])


@router.get("/", response_model=GraphResponse)
def get_graph(db: Session = Depends(get_db)):
    notes = (
        db.query(Note)
        .options(selectinload(Note.tags))
        .order_by(Note.id)
        .all()
    )

    links = db.query(Link).all()

    nodes = [
        GraphNode(
            id=note.id,
            title=note.title,
            tags=[tag.name for tag in note.tags],
        )
        for note in notes
    ]

    edges = [
        GraphEdge(source=link.source_id, target=link.target_id)
        for link in links
    ]

    return GraphResponse(nodes=nodes, edges=edges)