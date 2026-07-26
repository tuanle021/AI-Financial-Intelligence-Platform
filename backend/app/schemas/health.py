from typing import Literal

from pydantic import BaseModel, ConfigDict


class DatabaseHealthResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    status: Literal["healthy"]
    database: Literal["available"]