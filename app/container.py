
import inject
from app.db.db import Database
from app.config import get_config
from app.pseudonym.service import PseudonymService


def container_config(binder: inject.Binder) -> None:
    config = get_config()

    db = Database(dsn=config.database.dsn)
    binder.bind(Database, db)

    ps = PseudonymService(db)
    binder.bind(PseudonymService, ps)


def get_database() -> Database:
    return inject.instance(Database)


def get_pseudonym_service() -> PseudonymService:
    return inject.instance(PseudonymService)


inject.configure(container_config)
