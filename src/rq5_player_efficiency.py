"""RQ5 — Which players generate the highest goal contributions relative to
their playing time?
"""

from scipy.stats import spearmanr
import plotly.express as px

MIN_MINUTES = 300


def build_player_efficiency_table(players):
    player_impact = players.copy()
    player_impact["goals"] = player_impact["goals"].fillna(0)
    player_impact["assists"] = player_impact["assists"].fillna(0)
    player_impact["goal_contributions"] = player_impact["goals"] + player_impact["assists"]

    # Filter out small sample sizes so per-90 rates aren't dominated by cameo appearances.
    player_impact = player_impact[player_impact["minutes_played"] >= MIN_MINUTES].copy()
    player_impact["contributions_per_90"] = player_impact["goal_contributions"] / (player_impact["minutes_played"] / 90)
    return player_impact


def top_players_figure(top_players):
    fig = px.bar(
        top_players.sort_values("contributions_per_90"),
        x="contributions_per_90",
        y="player_name",
        orientation="h",
        labels={"contributions_per_90": "Goal Contributions per 90 Minutes", "player_name": "Player"},
        title="Top Players by Goal Contributions per 90 Minutes",
    )
    return fig


def run(data):
    player_impact = build_player_efficiency_table(data["player_stats"])
    top_players = player_impact.sort_values("contributions_per_90", ascending=False).head(12)

    top_players_figure(top_players).show()

    rho_minutes, p_minutes = spearmanr(
        data["player_stats"]["minutes_played"],
        data["player_stats"]["goals"].fillna(0) + data["player_stats"]["assists"].fillna(0),
    )
    print(f"Minutes played vs raw contributions: Spearman rho = {rho_minutes:.3f}, p = {p_minutes:.4g}")
    print(top_players[["player_name", "goals", "assists", "minutes_played", "contributions_per_90"]])

    return player_impact, top_players