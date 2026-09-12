"""RQ2 — Which match-performance variables are most strongly associated
with winning?
"""

import numpy as np
import pandas as pd
from scipy.stats import pointbiserialr
import plotly.graph_objects as go

PERFORMANCE_COLS = [
    "possession_pct", "total_shots", "shots_on_target", "corners", "fouls", "offsides", "saves",
]


def get_winner(row):
    if row["home_score"] > row["away_score"]:
        return row["home_team_id"]
    if row["away_score"] > row["home_score"]:
        return row["away_team_id"]
    if pd.notna(row["home_penalty_score"]) and pd.notna(row["away_penalty_score"]):
        return row["home_team_id"] if row["home_penalty_score"] > row["away_penalty_score"] else row["away_team_id"]
    return np.nan


def build_match_team_table(matches, mtstats):
    match_winners = matches[[
        "match_id", "home_team_id", "away_team_id", "home_score", "away_score", "home_xg", "away_xg", "result_type",
    ]].copy()
    match_winners["winner_id"] = matches.apply(get_winner, axis=1)

    match_team = mtstats.merge(
        match_winners[["match_id", "winner_id", "home_team_id", "away_team_id"]],
        on="match_id", how="left",
    )
    match_team["win"] = (match_team["team_id"] == match_team["winner_id"]).astype(int)
    return match_team


def validate_performance_metrics(match_team):
    """Point-biserial correlation of each performance metric against winning."""
    rows = []
    for c in PERFORMANCE_COLS:
        r, p = pointbiserialr(match_team["win"], match_team[c])
        rows.append({
            "Metric": c.replace("_", " ").title(),
            "Winner Mean": match_team.loc[match_team["win"] == 1, c].mean(),
            "Non-Winner Mean": match_team.loc[match_team["win"] == 0, c].mean(),
            "Point-Biserial r": r,
            "p-value": p,
        })
    return pd.DataFrame(rows).sort_values("Point-Biserial r", ascending=False)


def winner_profile_figure(match_team):
    winner_means = match_team.groupby("win")[PERFORMANCE_COLS].mean().T
    winner_means.columns = ["Non-winner", "Winner"]

    profile_z = (winner_means.sub(winner_means.mean(axis=1), axis=0)).div(
        winner_means.std(axis=1).replace(0, np.nan), axis=0
    )

    fig = go.Figure()
    for label in winner_means.columns:
        fig.add_trace(go.Scatterpolar(
            r=profile_z[label].fillna(0).values,
            theta=[c.replace("_", " ").title() for c in PERFORMANCE_COLS],
            fill="toself",
            name=label,
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[-2, 2])),
        title="Winner vs. Non-Winner Match Performance Profile",
    )
    return fig


def run(data):
    match_team = build_match_team_table(data["matches"], data["match_team_stats"])
    validation = validate_performance_metrics(match_team)
    print(validation)
    winner_profile_figure(match_team).show()
    return match_team, validation