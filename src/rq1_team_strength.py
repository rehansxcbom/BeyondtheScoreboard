"""RQ1 — How strongly are FIFA ranking, Elo rating and squad market value
associated with tournament progression?
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.preprocessing import StandardScaler
import plotly.express as px

STAGE_SCORE = {
    "Group Stage": 1,
    "Round of 32": 2,
    "Round of 16": 3,
    "Quarter-finals": 4,
    "Semi-finals": 5,
    "Third-place match": 5,  # treated as equivalent depth to a semi-final exit
    "Final": 6,
}


def build_team_analysis(teams, matches, mdetail, squads):
    """Build a per-team table of strength indicators and progression depth."""
    team_progress = []
    for _, row in teams.iterrows():
        tid = row["team_id"]
        mids = matches.loc[
            (matches["home_team_id"] == tid) | (matches["away_team_id"] == tid),
            "match_id",
        ]
        played_stages = mdetail.loc[mdetail["match_id"].isin(mids), "stage_name"].map(STAGE_SCORE)
        team_progress.append(played_stages.max() if len(played_stages) else np.nan)

    team_analysis = teams[["team_id", "team_name", "fifa_ranking_pre_tournament", "elo_rating"]].copy()
    team_analysis["progression_score"] = team_progress

    team_values = (
        squads.groupby("team_id", as_index=False)["market_value_eur"]
        .sum()
        .rename(columns={"market_value_eur": "squad_market_value_eur"})
    )
    team_analysis = team_analysis.merge(team_values, on="team_id", how="left")
    team_analysis["log_market_value"] = np.log1p(team_analysis["squad_market_value_eur"])

    scaler = StandardScaler()
    z = scaler.fit_transform(team_analysis[["fifa_ranking_pre_tournament", "elo_rating", "log_market_value"]])
    team_analysis["strength_score"] = (-z[:, 0] + z[:, 1] + z[:, 2]) / 3
    team_analysis["strength_percentile"] = team_analysis["strength_score"].rank(pct=True) * 100

    return team_analysis


def correlate_with_progression(team_analysis):
    rho_rank, p_rank = spearmanr(team_analysis["fifa_ranking_pre_tournament"], team_analysis["progression_score"])
    rho_elo, p_elo = spearmanr(team_analysis["elo_rating"], team_analysis["progression_score"])
    rho_value, p_value = spearmanr(team_analysis["squad_market_value_eur"], team_analysis["progression_score"])
    return {
        "fifa_ranking": (rho_rank, p_rank),
        "elo_rating": (rho_elo, p_elo),
        "squad_value": (rho_value, p_value),
    }


def strength_vs_progression_figure(team_analysis):
    fig = px.scatter(
        team_analysis,
        x="squad_market_value_eur",
        y="progression_score",
        size="strength_percentile",
        color="strength_score",
        hover_name="team_name",
        labels={
            "squad_market_value_eur": "Total Squad Market Value (€)",
            "progression_score": "Furthest Tournament Tier Achieved",
            "strength_score": "Composite Strength Index Score",
        },
        title="Squad Value vs. Tournament Progression",
    )
    fig.update_xaxes(type="log")
    fig.update_yaxes(
        tickmode="array",
        tickvals=[1, 2, 3, 4, 5, 6],
        ticktext=["Group Stage", "Round of 32", "Round of 16", "Quarter-finals", "Semi-finals", "Final"],
    )
    return fig


def run(data):
    team_analysis = build_team_analysis(data["teams"], data["matches"], data["matches_detailed"], data["squads_players"])
    correlations = correlate_with_progression(team_analysis)

    for label, (rho, p) in correlations.items():
        print(f"{label} vs progression: Spearman rho = {rho:.3f}, p = {p:.4g}")

    strength_vs_progression_figure(team_analysis).show()
    return team_analysis, correlations