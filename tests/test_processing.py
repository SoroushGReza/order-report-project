import pandas as pd

from order_reporting.processing import prepare_orders


def test_prepare_orders_calculates_values_and_returns():
    data = pd.DataFrame(
        {
            "order_id": ["O001", "O002"],
            "order_date": ["2026-01-01", "2026-01-02"],
            "customer_id": ["C001", "C002"],
            "region": ["North", "South"],
            "product_category": ["Books", "Electronics"],
            "quantity": [2, 3],
            "unit_price": [100.0, 200.0],
            "discount": [0.10, 0.25],
            "returned": ["true", "false"],
        }
    )

    result = prepare_orders(data)

    assert result["order_value"].tolist() == [200.0, 600.0]
    assert result["discounted_value"].tolist() == [180.0, 450.0]
    assert result["returned"].tolist() == [True, False]


def test_prepare_orders_handles_missing_and_inconsistent_values():
    data = pd.DataFrame(
        {
            "order_id": ["O001", "O002", "O003"],
            "order_date": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "customer_id": ["C001", "C002", "C003"],
            "region": [" north ", "SOUTH", None],
            "product_category": ["electronics ", "HOME", None],
            "quantity": [2, None, 1],
            "unit_price": [100.0, 300.0, None],
            "discount": ["unknown", None, 0.10],
            "returned": ["Yes", "no", None],
        }
    )

    result = prepare_orders(data)

    assert result["region"].tolist() == ["North", "South", "Unknown"]
    assert result["product_category"].tolist() == [
        "Electronics",
        "Home",
        "Unknown",
    ]

    assert result["quantity"].tolist() == [2, 1, 1]
    assert result["unit_price"].tolist() == [100.0, 300.0, 200.0]
    assert result["discount"].tolist() == [0.0, 0.0, 0.10]
    assert result["returned"].tolist() == [True, False, False]

    assert result["order_value"].tolist() == [200.0, 300.0, 200.0]
    assert result["discounted_value"].tolist() == [200.0, 300.0, 180.0]
