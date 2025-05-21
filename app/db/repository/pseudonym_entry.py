from sqlalchemy import select

from app.db.decorator import repository
from app.db.models.pseudonym_entry import PseudonymEntry
from app.db.repository.respository_base import RepositoryBase


@repository(PseudonymEntry)
class PseudonymEntryRepository(RepositoryBase):
    def find_by_bsn(self, hashed_bsn: str) -> PseudonymEntry | None:
        stmt = select(PseudonymEntry).where(PseudonymEntry.hashed_bsn == hashed_bsn)
        return self.db_session.execute(stmt).scalars().first()

    def find_by_pseudonym(self, pseudonym: str) -> PseudonymEntry | None:
        stmt = select(PseudonymEntry).where(PseudonymEntry.pseudonym == pseudonym)
        return self.db_session.execute(stmt).scalars().first()

    def find_by_bsn_and_provider(
        self, hashed_bsn: str, provider: str
    ) -> PseudonymEntry | None:
        stmt = (
            select(PseudonymEntry)
            .where(PseudonymEntry.hashed_bsn == hashed_bsn)
            .where(PseudonymEntry.provider == provider)
        )
        return self.db_session.execute(stmt).scalars().first()
