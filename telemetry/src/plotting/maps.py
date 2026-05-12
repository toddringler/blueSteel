from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
except Exception:  # pragma: no cover
    ccrs = None
    cfeature = None


def _new_map_axis(extent: tuple[float, float, float, float] | None = None):
    if ccrs is not None:
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})
        ax.coastlines(resolution="50m", linewidth=0.8)
        if cfeature is not None:
            ax.add_feature(cfeature.BORDERS, linewidth=0.5)
            ax.add_feature(cfeature.LAND, alpha=0.2)
        gl = ax.gridlines(draw_labels=True, linewidth=0.3, alpha=0.4)
        gl.top_labels = False
        gl.right_labels = False
        if extent is not None:
            ax.set_extent(extent, crs=ccrs.PlateCarree())
        return fig, ax

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.grid(True, alpha=0.3)
    if extent is not None:
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    return fig, ax


def plot_individual_track(
    gdf,
    fish_id,
    extent: tuple[float, float, float, float] = (-170, -130, 50, 63),
    color_by_date: bool = True,
):
    track = gdf[gdf["fish_id"].astype(str) == str(fish_id)].sort_values("timestamp")
    if track.empty:
        raise ValueError(f"No track found for fish_id={fish_id}")

    fig, ax = _new_map_axis(extent)
    transform = ccrs.PlateCarree() if ccrs is not None else None

    ax.plot(track["longitude"], track["latitude"], linewidth=1.2, color="tab:blue", transform=transform)
    if color_by_date:
        sc = ax.scatter(
            track["longitude"],
            track["latitude"],
            c=track["timestamp"].astype("int64"),
            s=18,
            cmap="viridis",
            transform=transform,
        )
        fig.colorbar(sc, ax=ax, label="Timestamp")

    ax.scatter(track.iloc[0]["longitude"], track.iloc[0]["latitude"], marker="o", s=60, color="green", label="Start", transform=transform)
    ax.scatter(track.iloc[-1]["longitude"], track.iloc[-1]["latitude"], marker="X", s=70, color="red", label="End", transform=transform)
    ax.legend(loc="best")
    ax.set_title(f"Steelhead kelt track: {fish_id}")
    return fig, ax


def plot_all_tracks(
    gdf,
    fish_ids: Iterable[str] | None = None,
    extent: tuple[float, float, float, float] = (-170, -130, 50, 63),
):
    if fish_ids is not None:
        subset_ids = {str(v) for v in fish_ids}
        tracks = gdf[gdf["fish_id"].astype(str).isin(subset_ids)].copy()
    else:
        tracks = gdf.copy()

    fig, ax = _new_map_axis(extent)
    transform = ccrs.PlateCarree() if ccrs is not None else None

    for fish_id, track in tracks.sort_values("timestamp").groupby("fish_id", observed=True):
        ax.plot(track["longitude"], track["latitude"], linewidth=1.0, label=str(fish_id), transform=transform)

    ax.set_title("Steelhead kelt cohort tracks")
    if tracks["fish_id"].nunique() <= 12:
        ax.legend(loc="best", fontsize=8)
    return fig, ax


def export_figure(
    fig,
    output_stem: str | Path,
    formats: tuple[str, ...] = ("png", "svg", "pdf"),
    dpi: int = 300,
) -> list[Path]:
    output_stem = Path(output_stem)
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for ext in formats:
        path = output_stem.with_suffix(f".{ext}")
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        paths.append(path)
    return paths
