from pathlib import Path

import pandas as pd
import pytest

from order_reporting.processing import prepare_orders
from order_reporting.reporting import create_reports

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "filename",
    [
        "overview.csv",
        "sales_by_category.csv",
        "sales_by_region.csv",
        "returns_by_category.csv",
    ],
)
def test_report_matches_original(filename):
    data = pd.read_csv(PROJECT_ROOT / "data" / "orders.csv")
    reports = create_reports(prepare_orders(data))

    expected = pd.read_csv(
        PROJECT_ROOT / "tests" / "fixtures" / "original_reports" / filename
    )

    pd.testing.assert_frame_equal(
        reports[filename],
        expected,
        check_dtype=False,
        check_exact=True,
    )
