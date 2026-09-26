import logging
from pathlib import Path

import pandas as pd

from order_reporting.config import ReportConfig
from order_reporting.processing import prepare_orders
from order_reporting.reporting import create_reports
from order_reporting.validation import validate_orders

logger = logging.getLogger(__name__)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(name)s | %(message)s",
    )

    project_root = Path(__file__).resolve().parent

    config = ReportConfig(
        input_path=project_root / "data" / "orders.csv",
        output_dir=project_root / "output",
    )

    logger.info("Startar orderrapport.")

    try:
        logger.info("Läser data från %s.", config.input_path)
        data = pd.read_csv(config.input_path)
        logger.info("Läste in %d rader.", len(data))

        validate_orders(data)
        logger.info("Valideringen är klar.")

        data = prepare_orders(data)
        reports = create_reports(data)
        logger.info("Skapade %d rapporter.", len(reports))

        config.output_dir.mkdir(parents=True, exist_ok=True)

        for filename, report in reports.items():
            output_path = config.output_dir / filename
            report.to_csv(output_path, index=False)
            logger.info("Sparade rapport till %s.", output_path)

    except (OSError, ValueError, pd.errors.ParserError) as error:
        logger.error("Körningen misslyckades: %s", error)
        return 1

    logger.info("Klart.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
