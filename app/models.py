from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Table,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


note_tags = Table(
    "note_tags",
    Base.metadata,
    Column(
        "note_id",
        Integer,
        ForeignKey("notes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False, index=True)
    content = Column(Text, nullable=True)
    created_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    tags = relationship(
        "Tag",
        secondary=note_tags,
        back_populates="notes",
    )

    outgoing_links = relationship(
        "Link",
        foreign_keys="Link.source_id",
        back_populates="source",
        cascade="all, delete-orphan",
    )

    incoming_links = relationship(
        "Link",
        foreign_keys="Link.target_id",
        back_populates="target",
        cascade="all, delete-orphan",
    )


class Link(Base):
    __tablename__ = "links"

    source_id = Column(
        Integer,
        ForeignKey("notes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    target_id = Column(
        Integer,
        ForeignKey("notes.id", ondelete="CASCADE"),
        primary_key=True,
    )

    source = relationship(
        "Note",
        foreign_keys=[source_id],
        back_populates="outgoing_links",
    )
    target = relationship(
        "Note",
        foreign_keys=[target_id],
        back_populates="incoming_links",
    )

    __table_args__ = (
        # The composite primary key prevents duplicate directed links.
        # Self-links will also be rejected by the API logic.
        UniqueConstraint(
            "source_id",
            "target_id",
            name="uq_link_source_target",
        ),
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    notes = relationship(
        "Note",
        secondary=note_tags,
        back_populates="tags",
    )