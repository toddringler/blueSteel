from __future__ import annotations

import pandas as pd


def subset_fish_ids(df: pd.DataFrame, fish_ids: list[str] | list[int]) -> pd.DataFrame:
    fish_ids_as_str = {str(v) for v in fish_ids}
    return df[df["fish_id"].astype(str).isin(fish_ids_as_str)].copy()


def subset_date_range(
    df: pd.DataFrame,
    start: str | pd.Timestamp | None = None,
    end: str | pd.Timestamp | None = None,
) -> pd.DataFrame:
    filtered = df.copy()
    if start is not None:
        filtered = filtered[filtered["timestamp"] >= pd.to_datetime(start, utc=True)]
    if end is not None:
        filtered = filtered[filtered["timestamp"] <= pd.to_datetime(end, utc=True)]
    return filtered


def drop_short_tracks(df: pd.DataFrame, min_points: int = 2) -> pd.DataFrame:
    keep_ids = (
        df.groupby("fish_id", observed=True)
        .size()
        .loc[lambda x: x >= min_points]
        .index
    )
    return df[df["fish_id"].isin(keep_ids)].copy()
