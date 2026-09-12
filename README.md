# ⚽ What Really Drives Success at the FIFA World Cup 2026?

A data-driven exploration of team strength, match performance, expected goals
(xG) and player efficiency at the FIFA World Cup 2026.

## Central Question

What separates teams that progress deep into the World Cup from those that
exit early?

## Project Objectives

1. Clean and validate a multi-table football dataset using Python.
2. Explore relationships between team strength, squad value and tournament
   progression.
3. Identify match statistics associated with winning.
4. Investigate whether possession translates into meaningful attacking threat.
5. Examine the relationship between expected goals (xG) and actual goals.
6. Compare player attacking efficiency using playing-time-adjusted metrics.
7. Identify different tactical profiles using unsupervised learning.
8. Communicate the findings through clear, evidence-based visualisations.

## Research Questions

- **RQ1 — Team Strength:** How strongly are FIFA ranking, Elo rating, and
  squad market value associated with tournament progression?
- **RQ2 — Match Success:** Which match-performance variables are most
  strongly associated with winning?
- **RQ3 — Possession & Threat:** Does possession become more valuable when
  combined with attacking threat?
- **RQ4 — Expected Goals:** How well does xG explain actual goals, and which
  teams over/under-perform their expected scoring output?
- **RQ5 — Player Efficiency:** Which players generate the highest goal
  contributions relative to their playing time?

## Status

🚧 Work in progress — see commit history for build-up of the analysis
pipeline, stage by stage.

## Setup

```bash
pip install -r requirements.txt
python main.py
```

Place the FIFA World Cup 2026 dataset zip in the project root before running.