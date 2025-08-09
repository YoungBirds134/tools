from typing import Dict, List, Optional
import logging

from ..models import Security

logger = logging.getLogger(__name__)


class MasterDataService:
    """In-memory master data store."""

    def __init__(self) -> None:
        self._securities: Dict[str, Security] = {}

    def list_securities(self) -> List[Security]:
        return list(self._securities.values())

    def get_security(self, symbol: str) -> Optional[Security]:
        return self._securities.get(symbol)

    def upsert_security(self, security: Security) -> Security:
        self._securities[security.symbol] = security
        logger.info("Event: masterData.security.updated", extra={"symbol": security.symbol})
        return security


master_data_service = MasterDataService()
