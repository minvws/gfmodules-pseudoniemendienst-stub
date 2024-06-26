import uuid
from typing import cast

from app.db.db import Database
from app.db.session import DbSession
from app.db.models import PseudonymEntry
from app.db.repository.pseudonym_entry import PseudonymEntryRepository


class PseudonymService:
    def __init__(self, db: Database):
        self.db = db

    def register(self, hashed_bsn: str, provider: str) -> PseudonymEntry:
        with self.db.get_db_session() as session:
            repository = self.get_pseudonym_entry_repository(session)

            entry = repository.find_by_bsn_and_provider(hashed_bsn, provider)
            if entry is not None:
                return entry

            new_entry = PseudonymEntry(
                id=str(uuid.uuid4()),
                hashed_bsn=hashed_bsn,
                provider=provider,
                pseudonym=str(uuid.uuid4())
            )
            session.add(new_entry)
            session.commit()

            return new_entry

    def exchange(self, pseudonym: str, target_provider: str) -> PseudonymEntry|None:
        with self.db.get_db_session() as session:
            repository = self.get_pseudonym_entry_repository(session)

            # Find the requested pseudonym in the database
            cur_entry = repository.find_by_pseudonym(pseudonym)
            if cur_entry is None:
                return None

            # Check if the target provider already has a pseudonym for the same BSN
            new_entry = repository.find_by_bsn_and_provider(cur_entry.hashed_bsn, target_provider)
            if new_entry is not None:
                return new_entry

            # Create new target, as it does not exist yet
            new_entry = PseudonymEntry(
                id = str(uuid.uuid4()),
                hashed_bsn=cur_entry.hashed_bsn,
                provider=target_provider,
                pseudonym = str(uuid.uuid4()),
            )
            session.add(new_entry)
            session.commit()

        return new_entry

    @staticmethod
    def get_pseudonym_entry_repository(session: DbSession) -> PseudonymEntryRepository:
        return cast(
            PseudonymEntryRepository,
            session.get_repository(PseudonymEntry)
        )
