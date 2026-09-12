"""FIFA World Cup 2026 — Performance Analysis pipeline entry point."""

from src.config import configure_environment
from src.data_loader import load_all_tables
from src.data_cleaning import clean_all
from src import eda
from src import rq1_team_strength
from src import rq2_match_success
from src import rq3_possession_threat
from src import rq4_expected_goals
from src import rq5_player_efficiency
from src import clustering
from src import visualization


def _banner(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    """Run the full FIFA World Cup 2026 analysis pipeline end to end."""
    _banner("ENVIRONMENT SETUP")
    configure_environment()

    _banner("DATA INGESTION")
    raw = load_all_tables()

    _banner("DATA CLEANING")
    data, quality_report = clean_all(raw)
    print(quality_report)

    _banner("TOURNAMENT OVERVIEW (EDA)")
    eda.run(data)

    _banner("RQ1 — TEAM STRENGTH VS PROGRESSION")
    team_analysis, rq1_correlations = rq1_team_strength.run(data)

    _banner("RQ2 — MATCH PERFORMANCE VS WINNING")
    match_team, rq2_validation = rq2_match_success.run(data)

    _banner("RQ3 — POSSESSION & ATTACKING THREAT")
    tactical, rq3_win_rates = rq3_possession_threat.run(match_team)

    _banner("RQ4 — EXPECTED GOALS VS ACTUAL GOALS")
    goal_perf, rq4_fit, team_xg = rq4_expected_goals.run(data)

    _banner("RQ5 — PLAYER EFFICIENCY")
    player_impact, top_players = rq5_player_efficiency.run(data)

    _banner("TACTICAL STYLE CLUSTERING")
    clustered, cluster_profile, cluster_names = clustering.run(match_team)

    _banner("STAGE EVOLUTION & TEAM EXPLORER")
    stage_goal_xg, stage_test, team_summary = visualization.run(data, goal_perf, match_team)

    _banner("PIPELINE COMPLETE")
    return {
        "data": data,
        "team_analysis": team_analysis,
        "match_team": match_team,
        "tactical": tactical,
        "goal_perf": goal_perf,
        "player_impact": player_impact,
        "clustered": clustered,
        "team_summary": team_summary,
    }


if __name__ == "__main__":
    main()