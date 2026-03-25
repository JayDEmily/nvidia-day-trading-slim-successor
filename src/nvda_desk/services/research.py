from __future__ import annotations

import json

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import ResearchNote
from nvda_desk.schemas.research import (
    ResearchNoteCreate,
    ResearchNoteListResponse,
    ResearchNotePayload,
)


class ResearchService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def create_note(self, payload: ResearchNoteCreate) -> ResearchNotePayload:
        with self._session_factory() as session:
            note = ResearchNote(
                symbol=payload.symbol,
                title=payload.title,
                thesis=payload.thesis,
                body_md=payload.body_md,
                tags_json=json.dumps(payload.tags),
            )
            session.add(note)
            session.commit()
            session.refresh(note)
            return self._to_payload(note)

    def list_notes(self, limit: int = 20) -> ResearchNoteListResponse:
        with self._session_factory() as session:
            stmt = select(ResearchNote).order_by(desc(ResearchNote.created_at)).limit(limit)
            notes = list(session.scalars(stmt))
        return ResearchNoteListResponse(notes=[self._to_payload(note) for note in notes])

    def _to_payload(self, note: ResearchNote) -> ResearchNotePayload:
        return ResearchNotePayload(
            note_id=note.id,
            created_at=note.created_at,
            symbol=note.symbol,
            title=note.title,
            thesis=note.thesis,
            body_md=note.body_md,
            tags=list(json.loads(note.tags_json)),
        )
