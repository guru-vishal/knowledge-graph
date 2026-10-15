from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = ""
    tags: list[str] = Field(default_factory=list)


class NoteLinkRequest(BaseModel):
    target_id: int = Field(gt=0)


class TagResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NoteSummary(BaseModel):
    id: int
    title: str
    tags: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str | None
    created_at: datetime | None
    tags: list[str] = Field(default_factory=list)
    linked_notes: list[NoteSummary] = Field(default_factory=list)
    backlinks: list[NoteSummary] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class GraphNode(BaseModel):
    id: int
    title: str
    tags: list[str]


class GraphEdge(BaseModel):
    source: int
    target: int


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]