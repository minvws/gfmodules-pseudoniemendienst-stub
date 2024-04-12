
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.decorator import repository
from app.db.models import PseudonymEntry


@repository(PseudonymEntry)
class PseudonymEntryRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_bsn(self, hashed_bsn: str) -> PseudonymEntry | None:
        stmt = select(PseudonymEntry).where(PseudonymEntry.hashed_bsn == hashed_bsn)
        return self.session.execute(stmt).scalars().first()

    def find_by_pseudonym(self, pseudonym: str) -> PseudonymEntry | None:
        stmt = select(PseudonymEntry).where(PseudonymEntry.pseudonym == pseudonym)
        return self.session.execute(stmt).scalars().first()

    def find_by_bsn_and_provider(self, hashed_bsn: str, provider: str) -> PseudonymEntry | None:
        stmt = (select(PseudonymEntry)
                .where(PseudonymEntry.hashed_bsn == hashed_bsn)
                .where(PseudonymEntry.provider == provider))
        return self.session.execute(stmt).scalars().first()
