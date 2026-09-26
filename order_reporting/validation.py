import pandas as pd

REQUIRED_COLUMNS = {
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


def validate_orders(data: pd.DataFrame) -> None:
    """Kontrollera att orderdata kan bearbetas på ett rimligt sätt."""
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        columns = ", ".join(sorted(missing_columns))
        raise ValueError(f"Obligatoriska kolumner saknas: {columns}")

    if data.empty:
        raise ValueError("Orderfilen innehåller inga orderrader.")

    numeric_columns = {}

    for column in ("quantity", "unit_price", "discount"):
        values = pd.to_numeric(data[column], errors="coerce")
        numeric_columns[column] = values

        if values.isin([float("inf"), float("-inf")]).any():
            raise ValueError(f"{column} innehåller oändliga värden.")

    quantity = numeric_columns["quantity"]
    unit_price = numeric_columns["unit_price"]
    discount = numeric_columns["discount"]

    if (quantity <= 0).any():
        raise ValueError("quantity måste vara större än 0.")

    if (unit_price < 0).any():
        raise ValueError("unit_price får inte vara negativt.")

    if ((discount < 0) | (discount > 1)).any():
        raise ValueError("discount måste vara mellan 0 och 1.")

    if unit_price.isna().all():
        raise ValueError(
            "unit_price saknar giltiga priser. "
            "Det går inte att beräkna ett medianpris."
        )
