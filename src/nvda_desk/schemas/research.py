from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ResearchNoteCreate(BaseModel):
    symbol: str = Field(default="NVDA", min_length=1)
    title: str = Field(min_length=1)
    thesis: str = Field(min_length=1)
    body_md: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)


class ResearchNotePayload(BaseModel):
    note_id: int
    created_at: datetime
    symbol: str
    title: str
    thesis: str
    body_md: str
    tags: list[str]


class ResearchNoteListResponse(BaseModel):
    notes: list[ResearchNotePayload]
