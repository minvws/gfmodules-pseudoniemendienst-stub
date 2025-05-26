import inject

from app.config import ConfigUraMiddleware, get_config
from app.data import UraNumber
from app.db.db import Database
from app.middleware.ura_middleware.allowlisted_ura_middleware import (
    AllowlistedUraMiddleware,
)
from app.middleware.ura_middleware.config_based_ura_middleware import (
    ConfigBasedUraMiddleware,
)
from app.middleware.ura_middleware.request_ura_middleware import RequestUraMiddleware
from app.middleware.ura_middleware.ura_middleware import UraMiddleware
from app.pseudonym.service import PseudonymService


def _ura_middleware(config: ConfigUraMiddleware, db: Database) -> UraMiddleware:
    ura_middleware: UraMiddleware
    if config.override_authentication_ura:
        ura_middleware = ConfigBasedUraMiddleware(
            UraNumber(config.override_authentication_ura)
        )
    else:
        ura_middleware = RequestUraMiddleware()
    if config.use_authentication_ura_allowlist:
        return AllowlistedUraMiddleware(
            db, ura_middleware, config.allowlist_cache_in_seconds
        )
    return ura_middleware


def container_config(binder: inject.Binder) -> None:
    config = get_config()

    db = Database(config.database)
    binder.bind(Database, db)

    ps = PseudonymService(db)
    binder.bind(PseudonymService, ps)
    binder.bind(UraMiddleware, _ura_middleware(config.ura_middleware, db))


def get_database() -> Database:
    return inject.instance(Database)


def get_pseudonym_service() -> PseudonymService:
    return inject.instance(PseudonymService)


inject.configure(container_config)
