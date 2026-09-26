import os

import pandas as pd

from order_reporting.processing import prepare_orders

INPUT_FILE = "data/orders.csv"
OUTPUT_FOLDER = "output"

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

    total_sales = round(
        data["discounted_value"].sum(),
        2,
    )

    number_of_orders = data["order_id"].nunique()
    number_of_returns = int(data["returned"].sum())

    overview = pd.DataFrame(
        {
            "metric": [
                "total_sales",
                "order_count",
                "return_count",
            ],
            "value": [
                total_sales,
                number_of_orders,
                number_of_returns,
            ],
        }
    )

    overview.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "overview.csv",
        ),
        index=False,
    )

    print("Sparade overview.csv")

    result1 = data.groupby(
        "product_category",
        as_index=False,
    ).agg(
        order_count=("order_id", "nunique"),
        total_sales=("discounted_value", "sum"),
        returns=("returned", "sum"),
    )

    result1["total_sales"] = result1["total_sales"].round(2)

    result1["return_rate"] = (result1["returns"] / result1["order_count"]).round(3)

    result1 = result1.sort_values(
        "total_sales",
        ascending=False,
    ).reset_index(drop=True)

    result1.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "sales_by_category.csv",
        ),
        index=False,
    )

    print("Sparade sales_by_category.csv")

    result2 = data.groupby(
        "region",
        as_index=False,
    ).agg(
        order_count=("order_id", "nunique"),
        total_sales=("discounted_value", "sum"),
        returns=("returned", "sum"),
    )

    result2["total_sales"] = result2["total_sales"].round(2)

    result2["return_rate"] = (result2["returns"] / result2["order_count"]).round(3)

    result2 = result2.sort_values(
        "total_sales",
        ascending=False,
    ).reset_index(drop=True)

    result2.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "sales_by_region.csv",
        ),
        index=False,
    )

    print("Sparade sales_by_region.csv")

    returns_by_category = data.groupby(
        "product_category",
        as_index=False,
    ).agg(
        order_count=("order_id", "nunique"),
        returns=("returned", "sum"),
    )

    returns_by_category["return_rate"] = (
        returns_by_category["returns"] / returns_by_category["order_count"]
    ).round(3)

    returns_by_category = returns_by_category.sort_values(
        "return_rate",
        ascending=False,
    ).reset_index(drop=True)

    returns_by_category.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "returns_by_category.csv",
        ),
        index=False,
    )

    print("Sparade returns_by_category.csv")
    print("Klart")

except Exception as error:
    print("Något gick fel:", error)
