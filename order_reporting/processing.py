import logging

import pandas as pd

logger = logging.getLogger(__name__)


def prepare_orders(data: pd.DataFrame) -> pd.DataFrame:
    """Rensa orderdata och beräkna ordervärden enligt originalets regler."""
    data = data.copy()

    text_defaults = {
        "region": "Unknown",
        "product_category": "Unknown",
        "returned": "false",
    }

    for column, replacement in text_defaults.items():
        missing_count = int(data[column].isna().sum())

        if missing_count:
            logger.warning(
                "%s: ersätter %d saknade värden med %s.",
                column,
                missing_count,
                replacement,
            )

        data[column] = data[column].fillna(replacement)

    data["region"] = data["region"].astype(str).str.strip().str.title()

    data["product_category"] = (
        data["product_category"].astype(str).str.strip().str.title()
    )

    for column in ("quantity", "unit_price", "discount"):
        data[column] = pd.to_numeric(data[column], errors="coerce")

    numeric_defaults = {
        "quantity": 1,
        "unit_price": data["unit_price"].median(),
        "discount": 0,
    }

    for column, replacement in numeric_defaults.items():
        missing_count = int(data[column].isna().sum())

        if missing_count:
            logger.warning(
                "%s: ersätter %d saknade eller ogiltiga värden med %s.",
                column,
                missing_count,
                replacement,
            )

        data[column] = data[column].fillna(replacement)

    data["returned"] = (
        data["returned"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1", "ja"])
    )

    data["order_value"] = data["quantity"] * data["unit_price"]

    data["discounted_value"] = data["order_value"] * (1 - data["discount"])

    return data
