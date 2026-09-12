"""FIFA World Cup 2026 — Performance Analysis pipeline entry point."""

from src.config import configure_environment
from src.data_loader import load_all_tables
from src.data_cleaning import clean_all
from src import eda
from src import rq1_team_strength
from src import rq2_match_success
from src import rq3_possession_threat


def main():
    configure_environment()
    raw = load_all_tables()
    data, quality_report = clean_all(raw)
    print(quality_report)
    eda.run(data)
    team_analysis, rq1_correlations = rq1_team_strength.run(data)
    match_team, rq2_validation = rq2_match_success.run(data)
    tactical, rq3_win_rates = rq3_possession_threat.run(match_team)
    return data, team_analysis, match_team, tactical


if __name__ == "__main__":
    main()