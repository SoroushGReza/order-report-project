from pathlib import Path

import pandas as pd

from order_reporting.config import ReportConfig
from order_reporting.processing import prepare_orders
from order_reporting.reporting import create_reports


def main():
    project_root = Path(__file__).resolve().parent

    config = ReportConfig(
        input_path=project_root / "data" / "orders.csv",
        output_dir=project_root / "output",
    )

    print("Startar orderrapport")

    try:
        data = pd.read_csv(config.input_path)

        required = {
            "order_id",
            "order_date",
            "customer_id",
            "region",
            "product_category",
            "quantity",
            "unit_price",
            "discount",
            "returned",
        }

        if not required.issubset(data.columns):
            raise Exception("Fel data")

        print("Läste in", len(data), "rader")

        data = prepare_orders(data)
        reports = create_reports(data)

        config.output_dir.mkdir(parents=True, exist_ok=True)

        for filename, report in reports.items():
            report.to_csv(
                config.output_dir / filename,
                index=False,
            )
            print("Sparade", filename)

        print("Klart")

    except Exception as error:
        print("Något gick fel:", error)


if __name__ == "__main__":
    main()
