"""FIFA World Cup 2026 — Performance Analysis pipeline entry point."""

from src.config import configure_environment
from src.data_loader import load_all_tables


def main():
    configure_environment()
    raw = load_all_tables()
    return raw


if __name__ == "__main__":
    main()