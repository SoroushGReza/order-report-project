import pandas as pd
import pytest

from order_reporting.validation import validate_orders


@pytest.fixture
def valid_orders():
    return pd.DataFrame(
        {
            "order_id": ["O001"],
            "order_date": ["2026-01-01"],
            "customer_id": ["C001"],
            "region": ["North"],
            "product_category": ["Books"],
            "quantity": [2.0],
            "unit_price": [100.0],
            "discount": [0.10],
            "returned": ["false"],
        }
    )


def test_validate_orders_accepts_valid_data(valid_orders):
    assert validate_orders(valid_orders) is None


def test_validate_orders_rejects_missing_column(valid_orders):
    data = valid_orders.drop(columns=["quantity"])

    with pytest.raises(ValueError, match="Obligatoriska kolumner saknas: quantity"):
        validate_orders(data)


def test_validate_orders_rejects_empty_data(valid_orders):
    data = valid_orders.iloc[:0]

    with pytest.raises(ValueError, match="inga orderrader"):
        validate_orders(data)


@pytest.mark.parametrize(
    "column, value",
    [
        ("quantity", -1.0),
        ("unit_price", -100.0),
        ("discount", 1.20),
    ],
)
def test_validate_orders_rejects_unreasonable_values(valid_orders, column, value):
    valid_orders.loc[0, column] = value

    with pytest.raises(ValueError, match=column):
        validate_orders(valid_orders)


def test_validate_orders_rejects_data_without_valid_prices(valid_orders):
    valid_orders["unit_price"] = ["unknown"]

    with pytest.raises(ValueError, match="saknar giltiga priser"):
        validate_orders(valid_orders)
