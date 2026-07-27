"""seed initial instruments

Revision ID: 72fa21184068
Revises: 2872cdb2b12a
Create Date: 2026-07-26 23:14:16.386831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72fa21184068'
down_revision: Union[str, Sequence[str], None] = '2872cdb2b12a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

instruments_table = sa.table(
    "instruments",
    sa.column("code", sa.String),
    sa.column("display_symbol", sa.String),
    sa.column("name", sa.String),
    sa.column("asset_type", sa.String),
    sa.column("base_asset", sa.String),
    sa.column("quote_asset", sa.String),
    sa.column("market_data_provider", sa.String),
    sa.column("provider_symbol", sa.String),
    sa.column("supports_latest", sa.Boolean),
    sa.column("supports_history", sa.Boolean),
    sa.column("supports_sentiment", sa.Boolean),
    sa.column("is_active", sa.Boolean),
)


def upgrade() -> None:
    """Seed the initial supported instruments."""

    op.bulk_insert(
        instruments_table,
        [
            {
                "code": "XAUUSD",
                "display_symbol": "XAU/USD",
                "name": "Gold Spot / US Dollar",
                "asset_type": "commodity",
                "base_asset": "XAU",
                "quote_asset": "USD",
                "market_data_provider": "twelve_data",
                "provider_symbol": "XAU/USD",
                "supports_latest": True,
                "supports_history": True,
                "supports_sentiment": False,
                "is_active": True,
            },
            {
                "code": "GOLD_FUTURES",
                "display_symbol": "GC=F",
                "name": "Gold Futures",
                "asset_type": "futures",
                "base_asset": "GOLD",
                "quote_asset": "USD",
                "market_data_provider": "yahoo",
                "provider_symbol": "GC=F",
                "supports_latest": True,
                "supports_history": True,
                "supports_sentiment": False,
                "is_active": True,
            },
            {
                "code": "GBPUSD",
                "display_symbol": "GBP/USD",
                "name": "British Pound / US Dollar",
                "asset_type": "forex",
                "base_asset": "GBP",
                "quote_asset": "USD",
                "market_data_provider": "twelve_data",
                "provider_symbol": "GBP/USD",
                "supports_latest": True,
                "supports_history": True,
                "supports_sentiment": False,
                "is_active": True,
            },
            {
                "code": "EURUSD",
                "display_symbol": "EUR/USD",
                "name": "Euro / US Dollar",
                "asset_type": "forex",
                "base_asset": "EUR",
                "quote_asset": "USD",
                "market_data_provider": "twelve_data",
                "provider_symbol": "EUR/USD",
                "supports_latest": True,
                "supports_history": True,
                "supports_sentiment": False,
                "is_active": True,
            },
        ],
    )

def downgrade() -> None:
    """Remove the initially seeded instruments."""

    op.execute(
        sa.delete(instruments_table).where(
            instruments_table.c.code.in_(
                [
                    "XAUUSD",
                    "GOLD_FUTURES",
                    "GBPUSD",
                    "EURUSD",
                ]
            )
        )
    )