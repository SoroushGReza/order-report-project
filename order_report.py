from pathlib import Path

import pandas as pd

from order_reporting.config import ReportConfig
from order_reporting.processing import prepare_orders
from order_reporting.reporting import create_reports
from order_reporting.validation import validate_orders


def main() -> int:
    project_root = Path(__file__).resolve().parent

    config = ReportConfig(
        input_path=project_root / "data" / "orders.csv",
        output_dir=project_root / "output",
    )

    print("Startar orderrapport")

    try:
        data = pd.read_csv(config.input_path)
        print("Läste in", len(data), "rader")

        validate_orders(data)

        data = prepare_orders(data)
        reports = create_reports(data)

        config.output_dir.mkdir(parents=True, exist_ok=True)

        for filename, report in reports.items():
            report.to_csv(
                config.output_dir / filename,
                index=False,
            )
            print("Sparade", filename)

    except (OSError, ValueError, pd.errors.ParserError) as error:
        print("Körningen misslyckades:", error)
        return 1

    print("Klart")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
