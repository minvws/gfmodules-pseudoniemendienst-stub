import logging

from fastapi import APIRouter, HTTPException, Depends
from opentelemetry import trace

from pydantic import BaseModel

from app import container
from app.pseudonym.service import PseudonymService

logger = logging.getLogger(__name__)
router = APIRouter()


class RegisterRequest(BaseModel):
    provider_id: str
    bsn_hash: str


class RegisterResponse(BaseModel):
    pseudonym: str


class ExchangeRequest(BaseModel):
    target_provider_id: str
    source_pseudonym: str


class ExchangeResponse(BaseModel):
    pseudonym: str


@router.post("/register",
            summary="Register a new pseudonym for a (hashed) BSN",
            tags=["pseudonym"]
            )
def post_register(req: RegisterRequest, service: PseudonymService = Depends(container.get_pseudonym_service)) -> RegisterResponse:
    span = trace.get_current_span()
    span.set_attribute("data.bsn_hash", req.bsn_hash)
    span.set_attribute("data.provider_id", req.provider_id)

    entry = service.register(req.bsn_hash, req.provider_id)
    return RegisterResponse(pseudonym=entry.pseudonym)


@router.post("/exchange",
            summary="Exchange a pseudonym for another one",
            tags=["pseudonym"]
            )
def post_exchange(
    req: ExchangeRequest,
    service: PseudonymService = Depends(container.get_pseudonym_service)
) -> ExchangeResponse:

    span = trace.get_current_span()
    span.set_attribute("data.source_pseudonym", req.source_pseudonym)
    span.set_attribute("data.target_provider_id", req.target_provider_id)

    entry = service.exchange(req.source_pseudonym, req.target_provider_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Pseudonym not found")

    return ExchangeResponse(pseudonym=entry.pseudonym)
