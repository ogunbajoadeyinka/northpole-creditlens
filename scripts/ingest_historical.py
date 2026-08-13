"""Run the NorthPole CreditLens historical ingestion pipeline."""

from __future__ import annotations

import argparse
import json
import os

from creditlens.data.pipeline import run_historical_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database-url",
        default=os.getenv("DATABASE_URL"),
        help="Optional PostgreSQL URL. If omitted, pipeline validates without loading.",
    )
    args = parser.parse_args()
    result = run_historical_pipeline(database_url=args.database_url)
    print(json.dumps(result.as_dict(), indent=2))


if __name__ == "__main__":
    main()
