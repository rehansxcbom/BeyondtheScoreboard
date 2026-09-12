"""RQ3 — Does possession become more valuable when combined with attacking
threat?
"""

import numpy as np
import plotly.express as px


def build_tactical_profiles(match_team):
    tactical = match_team.copy()

    pos_median = tactical["possession_pct"].median()
    sot_median = tactical["shots_on_target"].median()

    tactical["possession_profile"] = np.where(tactical["possession_pct"] >= pos_median, "High possession", "Low possession")
    tactical["threat_profile"] = np.where(tactical["shots_on_target"] >= sot_median, "High threat", "Low threat")
    tactical["tactical_style"] = tactical["possession_profile"] + " + " + tactical["threat_profile"]

    return tactical, pos_median, sot_median


def possession_threat_figure(tactical, pos_median, sot_median):
    fig = px.scatter(
        tactical,
        x="possession_pct",
        y="shots_on_target",
        color="tactical_style",
        symbol="win",
        labels={
            "possession_pct": "Possession Control Ratio (%)",
            "shots_on_target": "Target Shots Generated",
            "tactical_style": "Profile Quadrant",
        },
        title="Possession vs. Attacking Threat: Performance Style Segments",
    )
    fig.add_vline(x=pos_median, line_dash="dash", line_color="grey")
    fig.add_hline(y=sot_median, line_dash="dash", line_color="grey")
    return fig


def run(match_team):
    tactical, pos_median, sot_median = build_tactical_profiles(match_team)

    print(f"Baseline median possession: {pos_median:.1f}%")
    print(f"Baseline median target shots: {sot_median:.1f}")

    win_rate_by_style = tactical.groupby("tactical_style")["win"].mean().sort_values(ascending=False).round(3)
    print(win_rate_by_style)

    possession_threat_figure(tactical, pos_median, sot_median).show()
    return tactical, win_rate_by_style