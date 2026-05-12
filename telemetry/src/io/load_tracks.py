from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import geopandas as gpd
import pandas as pd


@dataclass(frozen=True)
class TrackSchema:
    fish_id_col: str = "Ptt"
    timestamp_col: str = "date.GMT"
    latitude_col: str = "Latitude"
    longitude_col: str = "Longitude"


@dataclass(frozen=True)
class ValidationReport:
    input_rows: int
    output_rows: int
    dropped_rows: int
    malformed_dates: int
    invalid_latitudes: int
    invalid_longitudes: int


DEFAULT_SCHEMA = TrackSchema()


def normalize_track_columns(
    df: pd.DataFrame,
    column_mapping: Mapping[str, str] | None = None,
    schema: TrackSchema = DEFAULT_SCHEMA,
) -> pd.DataFrame:
    mapping = {
        "fish_id": schema.fish_id_col,
        "timestamp": schema.timestamp_col,
        "latitude": schema.latitude_col,
        "longitude": schema.longitude_col,
    }
    if column_mapping:
        mapping.update(column_mapping)

    missing = [source for source in mapping.values() if source not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df.rename(
        columns={
            mapping["fish_id"]: "fish_id",
            mapping["timestamp"]: "timestamp",
            mapping["latitude"]: "latitude",
            mapping["longitude"]: "longitude",
        }
    )


def validate_and_clean_tracks(df: pd.DataFrame) -> tuple[pd.DataFrame, ValidationReport]:
    cleaned = df.copy()
    input_rows = len(cleaned)

    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], utc=True, errors="coerce")
    cleaned["latitude"] = pd.to_numeric(cleaned["latitude"], errors="coerce")
    cleaned["longitude"] = pd.to_numeric(cleaned["longitude"], errors="coerce")

    bad_date = cleaned["timestamp"].isna()
    bad_lat = cleaned["latitude"].isna() | (cleaned["latitude"] < -90) | (cleaned["latitude"] > 90)
    bad_lon = cleaned["longitude"].isna() | (cleaned["longitude"] < -180) | (cleaned["longitude"] > 180)
    bad_rows = bad_date | bad_lat | bad_lon

    cleaned = cleaned.loc[~bad_rows].copy()
    cleaned = cleaned.sort_values(["fish_id", "timestamp"]).reset_index(drop=True)

    report = ValidationReport(
        input_rows=input_rows,
        output_rows=len(cleaned),
        dropped_rows=int(bad_rows.sum()),
        malformed_dates=int(bad_date.sum()),
        invalid_latitudes=int(bad_lat.sum()),
        invalid_longitudes=int(bad_lon.sum()),
    )
    return cleaned, report


def load_track_csv(
    csv_path: str | Path,
    column_mapping: Mapping[str, str] | None = None,
    schema: TrackSchema = DEFAULT_SCHEMA,
) -> tuple[pd.DataFrame, ValidationReport]:
    df = pd.read_csv(csv_path)
    normalized = normalize_track_columns(df=df, column_mapping=column_mapping, schema=schema)
    return validate_and_clean_tracks(normalized)


def load_metadata_csv(csv_path: str | Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def to_geodataframe(df: pd.DataFrame, crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
    if not {"longitude", "latitude"}.issubset(df.columns):
        raise ValueError("Expected longitude and latitude columns before geospatial conversion")
    return gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs=crs,
    )


def reproject_tracks(gdf: gpd.GeoDataFrame, target_crs: str) -> gpd.GeoDataFrame:
    if gdf.crs is None:
        raise ValueError("GeoDataFrame has no CRS set")
    return gdf.to_crs(target_crs)


def group_tracks(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    grouped: dict[str, pd.DataFrame] = {}
    for fish_id, chunk in df.groupby("fish_id", sort=True):
        grouped[str(fish_id)] = chunk.reset_index(drop=True)
    return grouped
