"""Unsupervised tactical-style clustering (K-Means + PCA) over match-level
performance statistics.
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px

CLUSTER_FEATURES = [
    "possession_pct", "total_shots", "shots_on_target", "corners", "fouls", "offsides", "saves",
]


def cluster_match_styles(match_team, n_clusters=4, random_state=42):
    cluster_df = match_team[CLUSTER_FEATURES].dropna().copy()
    X = StandardScaler().fit_transform(cluster_df)

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=20)
    labels = kmeans.fit_predict(X)

    clustered = match_team.loc[cluster_df.index].copy()
    clustered["cluster"] = labels

    cluster_profile = clustered.groupby("cluster")[CLUSTER_FEATURES].mean()

    pca = PCA(n_components=2, random_state=random_state)
    coords = pca.fit_transform(X)
    clustered["PC1"] = coords[:, 0]
    clustered["PC2"] = coords[:, 1]

    return clustered, cluster_profile, pca.explained_variance_ratio_


def label_cluster(row):
    if row["shots_on_target"] > 0.5 and row["total_shots"] > 0.4:
        return "High Attacking Output / Dominant"
    if row["possession_pct"] > 0.5:
        return "Possession-Oriented / Control"
    if row["saves"] > 0.5 and row["possession_pct"] < 0:
        return "Defensive / Sustained Under Pressure"
    return "Balanced / Transition Direct"


def name_clusters(cluster_profile):
    z_profile = pd.DataFrame(
        StandardScaler().fit_transform(cluster_profile),
        index=cluster_profile.index,
        columns=cluster_profile.columns,
    )
    return {idx: label_cluster(row) for idx, row in z_profile.iterrows()}


def cluster_scatter_figure(clustered):
    return px.scatter(
        clustered,
        x="PC1", y="PC2",
        color="style",
        hover_data=["match_id", "team_id", "win", "possession_pct", "shots_on_target"],
        title="Tactical Style Clusters (PCA Projection)",
    )


def run(match_team):
    clustered, cluster_profile, explained = cluster_match_styles(match_team)
    cluster_names = name_clusters(cluster_profile)
    clustered["style"] = clustered["cluster"].map(cluster_names)

    print(f"PCA explained variance: PC1 = {explained[0]:.1%}, PC2 = {explained[1]:.1%}")
    print(cluster_profile.round(2))

    cluster_scatter_figure(clustered).show()

    for c, name in cluster_names.items():
        print(f"Cluster {c}: {name}")

    return clustered, cluster_profile, cluster_names