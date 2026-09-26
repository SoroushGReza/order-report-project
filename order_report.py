import os

import pandas as pd

from order_reporting.processing import prepare_orders
from order_reporting.reporting import create_reports

INPUT_FILE = "data/orders.csv"
OUTPUT_FOLDER = "output"


def main():
    print("Startar orderrapport")

    try:
        data = pd.read_csv(INPUT_FILE)

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

        for filename, report in reports.items():
            report.to_csv(
                os.path.join(OUTPUT_FOLDER, filename),
                index=False,
            )
            print("Sparade", filename)

        print("Klart")

    except Exception as error:
        print("Något gick fel:", error)


if __name__ == "__main__":
    main()
