"""Tournament-level exploratory data analysis: headline KPIs and stage mix."""

import plotly.express as px

STAGE_ORDER = [
    "Group Stage", "Round of 32", "Round of 16",
    "Quarter-finals", "Semi-finals", "Third-place match", "Final",
]


def compute_kpis(data):
    """Return a list of (label, value) tournament headline KPIs."""
    teams, matches = data["teams"], data["matches"]
    players, squads, stages = data["player_stats"], data["squads_players"], data["tournament_stages"]

    total_goals = int(matches["home_score"].sum() + matches["away_score"].sum())
    top_scorer = players.loc[players["goals"].idxmax(), ["player_name", "goals"]]

    most_valuable_team = (
        squads.groupby("team_id", as_index=False)["market_value_eur"].sum()
        .merge(teams[["team_id", "team_name"]], on="team_id")
        .sort_values("market_value_eur", ascending=False)
        .iloc[0]
    )

    return [
        ("Competing Nations", f"{len(teams):,}"),
        ("Matches Contested", f"{len(matches):,}"),
        ("Total Goals Aggregated", f"{total_goals:,}"),
        ("Tournament Structural Tiers", f"{len(stages):,}"),
        ("Golden Boot Leader", f"{top_scorer['player_name']} ({int(top_scorer['goals'])} Goals)"),
        ("Highest Valued Squad (€)", f"{most_valuable_team['team_name']} (€{most_valuable_team['market_value_eur']:,.0f})"),
    ]


def stage_distribution_figure(mdetail):
    """Bar chart of matches played per tournament stage."""
    stage_counts = mdetail["stage_name"].value_counts().reindex(STAGE_ORDER).dropna()
    fig = px.bar(
        x=stage_counts.index, y=stage_counts.values,
        labels={"x": "Tournament Tier", "y": "Matches Scheduled"},
        title="Match Distribution Across Tournament Tiers",
    )
    fig.update_layout(xaxis_tickangle=-30)
    return fig


def run(data):
    kpis = compute_kpis(data)
    for label, value in kpis:
        print(f"{label}: {value}")
    fig = stage_distribution_figure(data["matches_detailed"])
    fig.show()
    return kpis