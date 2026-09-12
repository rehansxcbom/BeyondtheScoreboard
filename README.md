## Findings

### Insight 1 — Squad Value and Ratings Track Progression, but Imperfectly
FIFA ranking, Elo rating and squad market value all show a meaningful
association with how far a team advances, with squad value and Elo showing
the strongest relationships. None of the three is a perfect predictor —
plenty of tournament drama sits in the residual.

### Insight 2 — Winning Requires More Than Simply Having the Ball
Comparing match statistics between winners and non-winners, shots on target
shows the strongest relationship with winning, ahead of possession and total
shots. Creating a genuine scoring threat matters more than control alone.

| Performance Variable | Winner Mean | Non-Winner Mean | Relationship |
| --------------------- | ----------: | ---------------: | ------------- |
| Shots on Target        |   **6.07**  |        **3.26**  | Strong        |
| Possession (%)         |  **54.96**  |       **44.53**  | Moderate      |
| Total Shots            |  **14.70**  |       **10.71**  | Moderate      |
| Corners                |   **5.48**  |        **4.02**  | Weak          |

### Insight 3 — Possession Matters Most When It Creates Threat
Splitting matches into possession/threat quadrants shows a clear hierarchy:

| Profile                           |  Win Rate |
| ---------------------------------- | --------: |
| High Possession + High Threat      | **71.1%** |
| Low Possession + High Threat       |     35.7% |
| High Possession + Low Threat       |     15.8% |
| Low Possession + Low Threat        |      8.5% |

High possession alone does not guarantee success — it pays off when
converted into shots on target.

### Insight 4 — Chance Quality Explains Goals, but Finishing Creates the Difference
xG correlates strongly with actual goals (Pearson r = 0.813, R² = 0.660,
Actual Goals ≈ −0.317 + 1.353 × xG), leaving room for finishing quality to
separate teams. England, France, USA and Argentina were the strongest
over-performers relative to their xG; Colombia, Ecuador and Spain
under-performed theirs.

### Insight 5 — Player Efficiency Matters Beyond Total Goals
Standardising goal contributions per 90 minutes (players with ≥300 minutes
played) surfaces efficiency independent of playing time. Messi, Mbappé and
Dembélé lead on this measure. Minutes played does correlate with raw
contribution totals (Spearman ρ = 0.416, p < 0.001), which is exactly why
the per-90 adjustment matters for fair comparison.

### Tactical Styles
Unsupervised clustering over match statistics (K-Means + PCA) recovers
distinct tactical identities — high-output attacking performances,
possession-oriented control, defensively resilient displays, and balanced/
transition-based approaches — cutting across nominal team strength.

## Status

✅ Analysis pipeline complete — see commit history for the stage-by-stage
build-up from raw data to final insights.

## Visuals

https://drive.google.com/file/d/1MjttHgULPA7ADeqpfQucdaksO-rGDpAJ/view?usp=share_link