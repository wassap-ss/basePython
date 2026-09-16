"""Точка входа: пакетный анализ заказов."""

from config import DATA_DIR
from src.analyzer import OrderAnalyzer


def main():
    analyzer = OrderAnalyzer(data_dir=DATA_DIR)
    results, errors = analyzer.process_all()
    analyzer.save_report(results)

    print("\n" + "=" * 50)
    print(f"Обработано файлов: {len(results)}")
    print(f"Файлов с ошибками: {errors}")
    print("=" * 50)


if __name__ == "__main__":
    main()