import logging

from fastapi import APIRouter, HTTPException, Depends

from app import container
from app.db.models import RegisterRequest, RegisterResponse, ExchangeRequest, ExchangeResponse
from app.pseudonym.service import PseudonymService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register",
            summary="Register a new pseudonym for a (hashed) BSN",
            tags=["pseudonym"]
            )
def post_register(req: RegisterRequest, service: PseudonymService = Depends(container.get_pseudonym_service)) -> RegisterResponse:
    entry = service.register(req.bsn_hash, req.provider_id)
    return RegisterResponse(pseudonym=entry.pseudonym)



@router.post("/exchange",
            summary="Exchange a pseudonym for another one",
            tags=["pseudonym"]
            )
def post_exchange(req: ExchangeRequest, service: PseudonymService = Depends(container.get_pseudonym_service)) -> ExchangeResponse:
    entry = service.exchange(req.source_pseudonym, req.target_provider_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Pseudonym not found")

    return ExchangeResponse(pseudonym=entry.pseudonym)