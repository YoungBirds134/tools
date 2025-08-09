from pydantic import BaseModel, Field


class Security(BaseModel):
    """Represents security master data."""

    symbol: str = Field(..., description="Trading symbol")
    exchange: str = Field(..., description="Exchange code")
    lot_size: int = Field(..., description="Lot size")
    tick_size: float = Field(..., description="Tick size")
