"""Класс OrderAnalyzer: пакетный анализ CSV с заказами."""

import logging
from pathlib import Path

import pandas as pd

from config import (
    DATA_DIR,
    REPORTS_DIR,
    LOGS_DIR,
    REPORT_FILE,
    LOG_FILE,
    STATUS_COLUMN,
    DELIVERED_STATUS,
    REQUIRED_COLUMNS,
)


class OrderAnalyzer:
    """Анализирует CSV-файлы с заказами и сохраняет сводку."""

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = Path(data_dir)
        self.logger = self._setup_logger()

    # Логирование
    def _setup_logger(self) -> logging.Logger:
        """Логгер, пишущий ошибки в logs/errors.log."""
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("order_analyzer")
        logger.setLevel(logging.ERROR)

        if not logger.handlers:
            handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
            handler.setFormatter(
                logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            )
            logger.addHandler(handler)

        return logger

    # Загрузка одного файла
    def load_file(self, file_path: Path) -> pd.DataFrame:
        """
        Читает CSV и проверяет наличие нужных колонок.
        Бросает исключение при битом/пустом/неверном файле.
        """
        df = pd.read_csv(file_path)

        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(
                f"отсутствуют колонки: {', '.join(sorted(missing))}"
            )

        # total_amount должен быть числовым
        if not pd.api.types.is_numeric_dtype(df["total_amount"]):
            raise ValueError("колонка total_amount содержит нечисловые значения")

        return df

    # Фильтрация
    def filter_delivered(self, df: pd.DataFrame) -> pd.DataFrame:
        """Оставляет только заказы со статусом Delivered."""
        return df[df[STATUS_COLUMN] == DELIVERED_STATUS]

    # Расчёт метрик 
    def calculate_metrics(
        self, delivered: pd.DataFrame, file_name: str
    ) -> dict:
        """Считает выручку, средний чек и количество заказов."""
        if delivered.empty:
            return {
                "file": file_name,
                "orders_count": 0,
                "total_revenue": 0.0,
                "average_check": 0.0,
            }

        return {
            "file": file_name,
            "orders_count": int(len(delivered)),
            "total_revenue": round(float(delivered["total_amount"].sum()), 2),
            "average_check": round(float(delivered["total_amount"].mean()), 2),
        }

    # Обработка одного файла
    def process_file(self, file_path: Path) -> dict | None:
        """
        Обрабатывает один CSV.
        При ошибке логирует и возвращает None.
        """
        try:
            df = self.load_file(file_path)
            delivered = self.filter_delivered(df)
            return self.calculate_metrics(delivered, file_path.name)
        except Exception as e:
            self.logger.error(
                f"{file_path.name}: {type(e).__name__}: {e}"
            )
            print(f"✖ {file_path.name}: пропущен ({type(e).__name__})")
            return None

    # Обработка всех файлов 
    def process_all(self) -> tuple[list[dict], int]:
        """
        Обходит все CSV в data/, обрабатывает каждый.
        Возвращает (список метрик, число ошибок).
        """
        if not self.data_dir.exists():
            print(f"Папка {self.data_dir} не найдена.")
            return [], 0

        csv_files = sorted(self.data_dir.glob("*.csv"))
        if not csv_files:
            print(f"В папке {self.data_dir} нет CSV-файлов.")
            return [], 0

        results, errors = [], 0

        for file_path in csv_files:
            metrics = self.process_file(file_path)
            if metrics is None:
                errors += 1
            else:
                results.append(metrics)
                print(f"✔ {file_path.name}: {metrics['orders_count']} заказов")

        return results, errors

    # Сохранение сводки
    def save_report(self, results: list[dict]) -> None:
        """Сохраняет итоговый CSV в reports/."""
        if not results:
            return
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(results).to_csv(
            REPORT_FILE, index=False, encoding="utf-8"
        )
        print(f"\nСводка сохранена: {REPORT_FILE}")