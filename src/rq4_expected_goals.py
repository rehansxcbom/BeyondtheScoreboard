"""RQ4 — How well does expected goals (xG) explain actual goals, and which
teams over/under-perform their expected scoring output?
"""

import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import plotly.express as px


def build_goal_performance_table(matches, teams):
    goal_rows = []
    for _, r in matches.iterrows():
        goal_rows.append({"match_id": r["match_id"], "team_id": r["home_team_id"], "goals": r["home_score"], "xg": r["home_xg"]})
        goal_rows.append({"match_id": r["match_id"], "team_id": r["away_team_id"], "goals": r["away_score"], "xg": r["away_xg"]})

    goal_perf = pd.DataFrame(goal_rows).merge(teams[["team_id", "team_name"]], on="team_id", how="left")
    goal_perf["finishing_residual"] = goal_perf["goals"] - goal_perf["xg"]
    return goal_perf


def fit_xg_relationship(goal_perf):
    r_xg, p_xg = pearsonr(goal_perf["xg"], goal_perf["goals"])
    slope, intercept = np.polyfit(goal_perf["xg"], goal_perf["goals"], 1)
    r2 = r_xg ** 2
    return {"r": r_xg, "p": p_xg, "r2": r2, "slope": slope, "intercept": intercept}


def finishing_residual_figure(goal_perf):
    fig = px.scatter(
        goal_perf,
        x="xg",
        y="finishing_residual",
        size="goals",
        color="finishing_residual",
        color_continuous_scale=px.colors.sequential.Viridis,
        hover_name="team_name",
        labels={
            "xg": "Expected Goals (xG)",
            "finishing_residual": "Finishing Residual (Goals − xG)",
        },
        title="Chance Generation vs. Finishing: Residual Performance",
    )
    fig.add_hline(y=0, line_dash="dash", line_color="black")
    return fig


def team_residual_summary(goal_perf):
    team_xg = (
        goal_perf.groupby("team_name", as_index=False)
        .agg(actual_goals=("goals", "sum"), total_xg=("xg", "sum"))
    )
    team_xg["residual"] = team_xg["actual_goals"] - team_xg["total_xg"]
    return team_xg


def run(data):
    goal_perf = build_goal_performance_table(data["matches"], data["teams"])
    fit = fit_xg_relationship(goal_perf)

    print(f"xG vs actual goals: Pearson r = {fit['r']:.3f}, p = {fit['p']:.4g}, R2 = {fit['r2']:.3f}")
    print(f"Actual Goals = {fit['intercept']:.3f} + {fit['slope']:.3f} * xG")

    finishing_residual_figure(goal_perf).show()

    team_xg = team_residual_summary(goal_perf)
    print("Top over-performers:")
    print(team_xg.sort_values("residual", ascending=False).head(7))
    print("Top under-performers:")
    print(team_xg.sort_values("residual", ascending=True).head(7))

    return goal_perf, fit, team_xg