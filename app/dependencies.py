from typing import cast

import inject
from fastapi import Request

from app.config import Config
from app.data import UraNumber
from app.db.db import Database
from app.middleware.ura_middleware.ura_middleware import UraMiddleware






def get_ura_middleware() -> UraMiddleware:
    return cast(UraMiddleware, inject.instance(UraMiddleware))


def authenticated_ura(request: Request) -> UraNumber:
    return get_ura_middleware().authenticated_ura(request)
