from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Literal
from uuid import uuid4


SourceType = Literal["pdf", "docx", "txt", "web"]


@dataclass(frozen=True, slots=True)
class IngestedChunk:
    text: str
    chunk_index: int
    page_number: int | None = None
    url: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(frozen=True, slots=True)
class IngestedDocument:
    source_name: str
    source_type: SourceType
    chunks: tuple[IngestedChunk, ...]
    content_hash: str
    ingested_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    version: int = 1
    id: str = field(default_factory=lambda: str(uuid4()))

    @classmethod
    def create(
        cls,
        source_name: str,
        source_type: SourceType,
        extracted_text: str,
        *,
        chunk_size: int = 1000,
        overlap: int = 150,
        page_number: int | None = None,
        url: str | None = None,
    ) -> "IngestedDocument":
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")
        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("overlap must be between 0 and chunk_size")

        text = extracted_text.strip()
        if not text:
            raise ValueError("Cannot ingest an empty document")

        step = chunk_size - overlap
        chunks = tuple(
            IngestedChunk(
                text=text[start : start + chunk_size],
                chunk_index=index,
                page_number=page_number,
                url=url,
            )
            for index, start in enumerate(range(0, len(text), step))
        )

        return cls(
            source_name=source_name,
            source_type=source_type,
            chunks=chunks,
            content_hash=sha256(text.encode("utf-8")).hexdigest(),
        )