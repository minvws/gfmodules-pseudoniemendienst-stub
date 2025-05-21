from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from app.db.models.base import Base


class PseudonymEntry(Base):
    __tablename__ = "pseudonyms"

    id: Mapped[str] = mapped_column("id", String(36), primary_key=True)
    hashed_bsn: Mapped[str] = mapped_column("hashed_bsn", String(64), nullable=False, index=True)
    provider: Mapped[str] = mapped_column("provider", String(36), nullable=False)
    pseudonym: Mapped[str] = mapped_column("pseudonym", String(36), nullable=False)

    def __repr__(self) -> str:
        return f"<PseudonymEntry(hashed_bsn={self.hashed_bsn}, provider={self.provider}, pseudonym={self.pseudonym})>"

