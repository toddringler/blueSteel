from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Kelt:
    fish_id: str
    ptt_id: str | None = None
    river: str | None = None
    deployment_year: int | None = None
    sex: str | None = None
    fork_length_mm: float | None = None
    deployment_datetime: str | None = None
    release_location: tuple[float, float] | None = None
    track: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_metadata_row(cls, row: dict[str, Any], fish_id: str | None = None) -> "Kelt":
        ptt = row.get("PTTID") or row.get("Ptt")
        deployment_dt = row.get("DeploymentStartDatetimeUTC")
        deployment_year = None
        if isinstance(deployment_dt, str) and len(deployment_dt) >= 4 and deployment_dt[:4].isdigit():
            deployment_year = int(deployment_dt[:4])

        release_lat = row.get("DeploymentLatitude")
        release_lon = row.get("DeploymentLongitude")
        release_location = None
        if release_lat is not None and release_lon is not None:
            release_location = (float(release_lat), float(release_lon))

        fork_length = row.get("AnimalLength")
        return cls(
            fish_id=str(fish_id or ptt),
            ptt_id=str(ptt) if ptt is not None else None,
            river=row.get("DeploymentLocation"),
            deployment_year=deployment_year,
            sex=row.get("AnimalSex"),
            fork_length_mm=float(fork_length) if fork_length not in (None, "") else None,
            deployment_datetime=deployment_dt,
            release_location=release_location,
            metadata=dict(row),
        )

    def attach_track(self, track) -> None:
        self.track = track


def build_kelt_index(metadata_df) -> dict[str, Kelt]:
    index: dict[str, Kelt] = {}
    for row in metadata_df.to_dict(orient="records"):
        kelt = Kelt.from_metadata_row(row)
        if kelt.ptt_id is not None:
            index[kelt.ptt_id] = kelt
    return index
