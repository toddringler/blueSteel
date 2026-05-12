from __future__ import annotations

import numpy as np
import pandas as pd
from pyproj import Geod

GEOD = Geod(ellps="WGS84")


def compute_step_metrics(df: pd.DataFrame) -> pd.DataFrame:
    tracks = df.sort_values(["fish_id", "timestamp"]).copy()

    tracks["prev_latitude"] = tracks.groupby("fish_id")["latitude"].shift(1)
    tracks["prev_longitude"] = tracks.groupby("fish_id")["longitude"].shift(1)
    tracks["prev_timestamp"] = tracks.groupby("fish_id")["timestamp"].shift(1)

    valid_step = (
        tracks["prev_latitude"].notna()
        & tracks["prev_longitude"].notna()
        & tracks["prev_timestamp"].notna()
    )

    fwd_azimuth = np.full(len(tracks), np.nan)
    distance_m = np.full(len(tracks), np.nan)

    if valid_step.any():
        az_fwd, _, dist = GEOD.inv(
            tracks.loc[valid_step, "prev_longitude"].to_numpy(),
            tracks.loc[valid_step, "prev_latitude"].to_numpy(),
            tracks.loc[valid_step, "longitude"].to_numpy(),
            tracks.loc[valid_step, "latitude"].to_numpy(),
        )
        fwd_azimuth[valid_step.to_numpy()] = az_fwd
        distance_m[valid_step.to_numpy()] = dist

    tracks["bearing_deg"] = (fwd_azimuth + 360) % 360
    tracks["daily_displacement_km"] = distance_m / 1000.0
    tracks["step_days"] = (
        (tracks["timestamp"] - tracks["prev_timestamp"]).dt.total_seconds() / 86400.0
    )
    tracks["speed_km_day"] = tracks["daily_displacement_km"] / tracks["step_days"]
    tracks.loc[tracks["step_days"] <= 0, "speed_km_day"] = np.nan
    tracks["cumulative_distance_km"] = tracks.groupby("fish_id")["daily_displacement_km"].cumsum()

    return tracks


def summarize_track_metrics(step_metrics_df: pd.DataFrame) -> pd.DataFrame:
    g = step_metrics_df.groupby("fish_id", observed=True)

    summary = pd.DataFrame({
        "fish_id": g.size().index,
        "n_observations": g.size().to_numpy(),
        "track_start": g["timestamp"].min().to_numpy(),
        "track_end": g["timestamp"].max().to_numpy(),
        "track_duration_days": (g["timestamp"].max() - g["timestamp"].min()).dt.total_seconds().to_numpy() / 86400.0,
        "cumulative_distance_km": g["daily_displacement_km"].sum(min_count=1).fillna(0).to_numpy(),
    })
    summary["mean_speed_km_day"] = summary["cumulative_distance_km"] / summary["track_duration_days"].replace(0, np.nan)
    return summary
