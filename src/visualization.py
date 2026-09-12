"""Interactive team explorer and stage-evolution summary visualisations."""

import pandas as pd
from scipy.stats import ttest_ind
import plotly.graph_objects as go
import plotly.express as px

STAGE_ORDER = [
    "Group Stage", "Round of 32", "Round of 16",
    "Quarter-finals", "Semi-finals", "Third-place match", "Final",
]


def scoring_by_stage_figure(goal_perf, mdetail):
    stage_goal_xg = (
        goal_perf.merge(mdetail[["match_id", "stage_name"]], on="match_id", how="left")
        .groupby("stage_name", as_index=False)
        .agg(avg_goals=("goals", "mean"), avg_xg=("xg", "mean"))
    )
    stage_goal_xg["stage_name"] = pd.Categorical(stage_goal_xg["stage_name"], categories=STAGE_ORDER, ordered=True)
    stage_goal_xg = stage_goal_xg.sort_values("stage_name")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stage_goal_xg["stage_name"], y=stage_goal_xg["avg_goals"], mode="lines+markers", name="Actual Goals"))
    fig.add_trace(go.Scatter(x=stage_goal_xg["stage_name"], y=stage_goal_xg["avg_xg"], mode="lines+markers", name="Expected Goals (xG)"))
    fig.update_layout(title="Scoring Output Across Tournament Stages", xaxis_title="Tournament Stage", yaxis_title="Average per Team-Match")
    return fig, stage_goal_xg


def group_vs_knockout_test(goal_perf, mdetail):
    group = goal_perf.merge(mdetail[["match_id", "stage_name"]], on="match_id")
    group_avg = group.loc[group["stage_name"] == "Group Stage", "goals"]
    knockout_avg = group.loc[group["stage_name"] != "Group Stage", "goals"]
    t_stat, p_stage = ttest_ind(group_avg, knockout_avg, equal_var=False)
    return {
        "group_mean": group_avg.mean(),
        "knockout_mean": knockout_avg.mean(),
        "t_stat": t_stat,
        "p_value": p_stage,
    }


def team_explorer_figure(match_team, teams):
    merged = match_team.merge(teams[["team_id", "team_name"]], on="team_id", how="left")
    team_summary = merged.groupby("team_name", as_index=False).agg(
        matches=("match_id", "count"),
        wins=("win", "sum"),
        avg_possession=("possession_pct", "mean"),
        avg_shots_on_target=("shots_on_target", "mean"),
    )
    team_summary["win_rate"] = (team_summary["wins"] / team_summary["matches"]).round(3)

    fig = px.scatter(
        team_summary,
        x="avg_possession",
        y="avg_shots_on_target",
        size="matches",
        color="win_rate",
        hover_name="team_name",
        labels={
            "avg_possession": "Average Possession (%)",
            "avg_shots_on_target": "Average Shots on Target",
            "win_rate": "Win Rate",
        },
        title="Interactive Team Explorer: Possession, Threat & Win Rate",
    )
    return fig, team_summary


def run(data, goal_perf, match_team):
    fig_stage, stage_goal_xg = scoring_by_stage_figure(goal_perf, data["matches_detailed"])
    fig_stage.show()

    test_result = group_vs_knockout_test(goal_perf, data["matches_detailed"])
    print(f"Group stage mean goals: {test_result['group_mean']:.3f}")
    print(f"Knockout stage mean goals: {test_result['knockout_mean']:.3f}")
    print(f"Welch's t-test p-value: {test_result['p_value']:.4f}")

    fig_explorer, team_summary = team_explorer_figure(match_team, data["teams"])
    fig_explorer.show()

    return stage_goal_xg, test_result, team_summary