"""FIFA World Cup 2026 — Performance Analysis pipeline entry point."""

from src.config import configure_environment
from src.data_loader import load_all_tables
from src.data_cleaning import clean_all
from src import eda
from src import rq1_team_strength


def main():
    configure_environment()
    raw = load_all_tables()
    data, quality_report = clean_all(raw)
    print(quality_report)
    eda.run(data)
    team_analysis, rq1_correlations = rq1_team_strength.run(data)
    return data, team_analysis


if __name__ == "__main__":
    main()