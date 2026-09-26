import pandas as pd


def prepare_orders(data: pd.DataFrame) -> pd.DataFrame:
    """Rensa orderdata och beräkna ordervärden enligt originalets regler."""
    data = data.copy()

    data["region"] = (
        data["region"].fillna("Unknown").astype(str).str.strip().str.title()
    )

    data["product_category"] = (
        data["product_category"].fillna("Unknown").astype(str).str.strip().str.title()
    )

    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce").fillna(1)

    data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce")
    data["unit_price"] = data["unit_price"].fillna(data["unit_price"].median())

    data["discount"] = pd.to_numeric(data["discount"], errors="coerce").fillna(0)

    data["returned"] = (
        data["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1", "ja"])
    )

    data["order_value"] = data["quantity"] * data["unit_price"]

    data["discounted_value"] = data["order_value"] * (1 - data["discount"])

    return data
