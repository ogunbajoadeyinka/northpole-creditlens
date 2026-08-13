"""Database loading utilities for CreditLens historical data."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sqlalchemy import Engine, create_engine, text


@dataclass(frozen=True)
class LoadResult:
    rows_written: int
    schema: str
    table: str


def build_engine(database_url: str) -> Engine:
    """Create a SQLAlchemy engine from a PostgreSQL-compatible URL."""
    return create_engine(database_url, pool_pre_ping=True)


def ensure_schema(engine: Engine, schema: str = "creditlens") -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))


def replace_historical_table(
    frame: pd.DataFrame,
    engine: Engine,
    schema: str = "creditlens",
    table: str = "historical_credit_observation",
) -> LoadResult:
    """Replace the historical baseline table with a validated canonical frame.

    This is intentionally used only for the reproducible historical baseline.
    Live application and prediction tables will use append/upsert patterns.
    """
    ensure_schema(engine, schema=schema)
    rows = int(
        frame.to_sql(
            table,
            con=engine,
            schema=schema,
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=2_000,
        )
        or len(frame)
    )
    return LoadResult(rows_written=rows, schema=schema, table=table)
