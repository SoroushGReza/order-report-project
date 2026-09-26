import pandas as pd


def summarize_sales(data: pd.DataFrame, group_by: str) -> pd.DataFrame:
    """Sammanställ försäljning och returer för en grupperingskolumn."""
    summary = data.groupby(group_by, as_index=False).agg(
        order_count=("order_id", "nunique"),
        total_sales=("discounted_value", "sum"),
        returns=("returned", "sum"),
    )

    summary["total_sales"] = summary["total_sales"].round(2)
    summary["return_rate"] = (summary["returns"] / summary["order_count"]).round(3)

    return summary.sort_values("total_sales", ascending=False).reset_index(drop=True)


def create_reports(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Skapa programmets fyra rapporter utan att skriva till filer."""
    overview = pd.DataFrame(
        {
            "metric": [
                "total_sales",
                "order_count",
                "return_count",
            ],
            "value": [
                round(data["discounted_value"].sum(), 2),
                data["order_id"].nunique(),
                int(data["returned"].sum()),
            ],
        }
    )

    sales_by_category = summarize_sales(data, "product_category")
    sales_by_region = summarize_sales(data, "region")

    returns_by_category = data.groupby("product_category", as_index=False).agg(
        order_count=("order_id", "nunique"),
        returns=("returned", "sum"),
    )

    returns_by_category["return_rate"] = (
        returns_by_category["returns"] / returns_by_category["order_count"]
    ).round(3)

    returns_by_category = returns_by_category.sort_values(
        "return_rate", ascending=False
    ).reset_index(drop=True)

    return {
        "overview.csv": overview,
        "sales_by_category.csv": sales_by_category,
        "sales_by_region.csv": sales_by_region,
        "returns_by_category.csv": returns_by_category,
    }
