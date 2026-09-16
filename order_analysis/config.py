"""Конфигурация проекта: пути и настройки анализа."""

from pathlib import Path

# --- Базовые пути ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

# --- Выходные файлы ---
REPORT_FILE = REPORTS_DIR / "report.csv"
LOG_FILE = LOGS_DIR / "errors.log"

# --- Настройки фильтрации ---
STATUS_COLUMN = "status"
DELIVERED_STATUS = "Delivered"

# --- Обязательные колонки во входных файлах ---
REQUIRED_COLUMNS = {"order_id", STATUS_COLUMN, "total_amount"}