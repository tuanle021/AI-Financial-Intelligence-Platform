from pydantic import BaseModel, ConfigDict

from app.models.asset_type import AssetType
from app.models.instrument_code import InstrumentCode


class InstrumentResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    code: InstrumentCode
    display_symbol: str
    name: str
    asset_type: AssetType
    base_asset: str | None = None
    quote_asset: str | None = None

    supports_latest: bool
    supports_history: bool
    supports_sentiment: bool