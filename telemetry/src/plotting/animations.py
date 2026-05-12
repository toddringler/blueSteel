from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

try:
    import cartopy.crs as ccrs
except Exception:  # pragma: no cover
    ccrs = None


def build_track_animation(
    gdf,
    fish_id=None,
    extent: tuple[float, float, float, float] = (-170, -130, 50, 63),
    interval_ms: int = 150,
):
    if fish_id is None:
        fish_id = gdf["fish_id"].iloc[0]

    track = gdf[gdf["fish_id"].astype(str) == str(fish_id)].sort_values("timestamp").reset_index(drop=True)
    if track.empty:
        raise ValueError(f"No track found for fish_id={fish_id}")

    if ccrs is not None:
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})
        ax.coastlines(resolution="50m", linewidth=0.8)
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        transform = ccrs.PlateCarree()
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
        ax.grid(alpha=0.3)
        transform = None

    line, = ax.plot([], [], color="tab:blue", linewidth=1.5, transform=transform)
    point = ax.scatter([], [], color="tab:red", s=50, transform=transform)
    title = ax.set_title("")

    def update(frame_index: int):
        chunk = track.iloc[: frame_index + 1]
        line.set_data(chunk["longitude"], chunk["latitude"])
        point.set_offsets([[chunk.iloc[-1]["longitude"], chunk.iloc[-1]["latitude"]]])
        ts = chunk.iloc[-1]["timestamp"]
        title.set_text(f"Fish {fish_id} | {ts}")
        return line, point, title

    return FuncAnimation(fig, update, frames=len(track), interval=interval_ms, blit=False)


def save_animation(animation: FuncAnimation, output_path: str, dpi: int = 150) -> None:
    animation.save(output_path, dpi=dpi)
