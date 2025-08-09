from typing import List

from fastapi import APIRouter, HTTPException

from ..models import Security
from ..services.master_data_service import master_data_service

router = APIRouter()


@router.get("/securities", response_model=List[Security])
async def list_securities() -> List[Security]:
    """List all securities."""
    return master_data_service.list_securities()


@router.get("/securities/{symbol}", response_model=Security)
async def get_security(symbol: str) -> Security:
    """Get security by symbol."""
    security = master_data_service.get_security(symbol)
    if not security:
        raise HTTPException(status_code=404, detail="Security not found")
    return security


@router.post("/securities", response_model=Security)
async def create_or_update_security(security: Security) -> Security:
    """Create or update a security."""
    return master_data_service.upsert_security(security)
