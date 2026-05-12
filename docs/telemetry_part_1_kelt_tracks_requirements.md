# Part 1 — Visualization of Steelhead Kelt GPS Tracks

## Software Requirements Specification (SRS)

---

# 1. Purpose

This document defines the software requirements for Part 1 of the `blueSteel` telemetry project:

> Visualization and exploratory analysis of marine migration tracks from satellite-tagged steelhead kelts.

The purpose of this component is to:

- ingest reconstructed fish movement tracks,
- visualize individual and cohort migration paths,
- compute basic movement metrics,
- provide reproducible exploratory notebooks,
- and establish the geospatial foundation for later fish–ocean coupling analyses.

This document is intended for:

- human developers,
- GitHub Copilot,
- Claude,
- and future contributors.

---

# 2. Scope

Part 1 focuses exclusively on:

- fish movement visualization,
- GPS/geolocation track handling,
- trajectory analysis,
- and map generation.

Part 1 explicitly excludes:

- ocean environmental datasets,
- SST integration,
- habitat modeling,
- machine learning,
- statistical ecological inference,
- or fish–ocean overlay analyses.

Those will be implemented in later project phases.

---

# 3. Dataset Architecture

The telemetry framework shall support:

- multiple rivers,
- multiple deployment years,
- multiple telemetry studies,
- and heterogeneous telemetry sources.

The currently provided Situk River dataset is considered:

> an initial reference implementation and validation dataset.

The software architecture shall therefore be generalized and extensible rather than tightly coupled to:

- a single river,
- a single telemetry program,
- or a single CSV schema.

---

## 3.1 Initial Reference Dataset

Initial input track file:

```text
ATN_steelhead_tracks_10.6.2021.csv
```

Expected columns:

| Column | Description |
|---|---|
| Ptt | Satellite transmitter ID |
| date.GMT | Observation date |
| Latitude | Decimal latitude |
| Longitude | Decimal longitude |

Initial associated metadata file:

```text
Seitz_ATN Tag Deployment Metadata_steelhead kelts_10.7.2021.csv
```

---

## 3.2 Future Dataset Support

The system shall support future ingestion of:

- additional Situk River cohorts,
- additional Southeast Alaska rivers,
- Washington steelhead telemetry datasets,
- alternative telemetry providers,
- and future telemetry modalities.

Examples may include:

- PSAT telemetry,
- Argos telemetry,
- acoustic telemetry,
- archival tag datasets,
- and state-space reconstructed tracks.

The ingestion framework shall therefore:

- separate schema normalization from downstream analysis,
- support configurable column mappings,
- and avoid assumptions tied to any single study.

---|---|
| Ptt | Satellite transmitter ID |
| date.GMT | Observation date |
| Latitude | Decimal latitude |
| Longitude | Decimal longitude |

Associated metadata file:

```text
Seitz_ATN Tag Deployment Metadata_steelhead kelts_10.7.2021.csv
```

---

# 4. Objectives

The software shall:

1. Load and validate telemetry track datasets.
2. Convert timestamps into timezone-aware datetime objects.
3. Create geospatial track objects.
4. Visualize fish migration trajectories.
5. Compute movement metrics.
6. Export publication-quality figures.
7. Support exploratory notebook workflows.
8. Provide reusable Python modules for downstream analyses.

---

# 5. Repository Structure

```text
telemetry/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── environmental/
│   └── derived/
│
├── notebooks/
│   ├── 01_tracks/
│   ├── 02_ocean_fields/
│   ├── 03_track_overlay/
│   └── 04_analysis/
│
├── src/
│   ├── io/
│   ├── tracks/
│   ├── ocean/
│   ├── plotting/
│   └── models/
│
├── figures/
├── exports/
└── docs/
```

---

# 6. Required Python Environment

Minimum Python version:

```text
Python 3.11+
```

Required libraries:

```text
pandas
numpy
geopandas
matplotlib
cartopy
pyproj
shapely
xarray
jupyter
ipykernel
```

Optional libraries:

```text
movingpandas
folium
hvplot
holoviews
contextily
```

---

# 6.1 Kelt Object Model

The software shall support a reusable kelt-centered object model.

Each kelt object shall support:

| Property | Description |
|---|---|
| fish_id | Internal unique identifier |
| ptt_id | Telemetry transmitter ID |
| river | River or watershed origin |
| deployment_year | Tagging year |
| sex | Fish sex |
| fork_length_mm | Fish fork length |
| deployment_datetime | Tagging timestamp |
| release_location | Initial release coordinates |
| track | Associated geospatial trajectory |
| metadata | Additional deployment metadata |

The software shall support linking:

- track observations,
- deployment metadata,
- biological metadata,
- and future environmental covariates

into unified fish-level objects.

The linkage mechanism shall support:

- PTT identifiers,
- deployment identifiers,
- and future telemetry-specific identifiers.

Fish-level objects shall persist metadata throughout downstream processing and plotting workflows.

---

# 7. Functional Requirements

## 7.1 Data Loading

The software shall:

- load CSV track data using pandas,
- validate required columns,
- detect malformed rows,
- remove invalid coordinates,
- sort observations chronologically,
- and group observations by fish ID.

### Validation Rules

Latitude:

```text
-90 <= latitude <= 90
```

Longitude:

```text
-180 <= longitude <= 180
```

Dates must parse successfully into UTC datetimes.

---

## 7.2 Geospatial Conversion

The software shall:

- convert track data into GeoDataFrames,
- support EPSG:4326 coordinate reference system,
- preserve original coordinates,
- and support reprojection.

---

## 7.3 Track Visualization

The software shall support:

### Individual Fish Maps

- single-fish trajectory plots,
- directional migration visualization,
- date-colored trajectories,
- and start/end markers.

### Cohort Maps

- all fish in a deployment year,
- multi-year overlays,
- fish-specific color schemes,
- and regional occupancy maps.

### Basemap Features

Maps shall support:

- coastlines,
- bathymetry overlays,
- political boundaries,
- latitude/longitude grids,
- Gulf of Alaska extent,
- Aleutian extent.

---

## 7.4 Movement Metrics

The software shall compute:

| Metric | Description |
|---|---|
| Daily displacement | Distance between sequential positions |
| Cumulative distance | Total migration distance |
| Mean speed | Mean km/day |
| Bearing | Direction of movement |
| Track duration | Days at liberty |

Geodesic calculations shall use ellipsoidal Earth geometry.

---

## 7.5 Figure Export

The software shall export:

- PNG,
- SVG,
- PDF.

Publication-quality output shall support:

- configurable DPI,
- vector graphics,
- consistent typography,
- reproducible dimensions.

---

# 8. Notebook Requirements

Primary notebook location:

```text
telemetry/notebooks/01_tracks/
```

Required notebooks:

| Notebook | Purpose |
|---|---|
| 01_load_tracks.ipynb | Data loading and validation |
| 02_plot_individual_tracks.ipynb | Individual fish maps |
| 03_plot_all_tracks.ipynb | Cohort migration visualization |
| 04_compute_metrics.ipynb | Movement metric calculations |
| 05_animation_prototype.ipynb | Animated movement testing |

---

# 9. Source Module Requirements

Reusable logic shall be implemented in `src/`.

Example modules:

```text
src/io/load_tracks.py
src/tracks/metrics.py
src/tracks/filtering.py
src/plotting/maps.py
src/plotting/animations.py
```

Notebooks shall import reusable logic rather than duplicating code.

---

# 10. Coordinate System Requirements

Primary CRS:

```text
EPSG:4326
```

Optional projected CRS support:

- Alaska Albers
- North Pacific stereographic

---

# 11. Performance Requirements

The software should:

- load datasets in under 5 seconds,
- render standard maps in under 10 seconds,
- support at least 100k track points,
- and avoid excessive memory duplication.

---

# 12. Reproducibility Requirements

The project shall:

- support deterministic outputs,
- maintain stable environment specifications,
- avoid notebook state dependency,
- and separate reusable code from exploratory code.

A future environment file shall be created:

```text
environment.yml
```

or:

```text
pyproject.toml
```

---

# 13. Future Compatibility

Part 1 outputs shall support later integration with:

- SST datasets,
- chlorophyll fields,
- current vectors,
- marine heatwave indices,
- and fish–ocean overlap analyses.

Track objects should therefore preserve:

- precise timestamps,
- spatial fidelity,
- and fish-specific identifiers.

---

# 14. Non-Goals

Part 1 shall not implement:

- ecological inference,
- habitat selection models,
- machine learning,
- Bayesian movement models,
- hidden Markov models,
- or climate attribution.

---

# 15. Deliverables

Part 1 deliverables shall include:

| Deliverable | Description |
|---|---|
| Cleaned telemetry loader | Reusable ingestion code |
| Standardized GeoDataFrame pipeline | Track representation |
| Static migration maps | Publication-ready figures |
| Exploratory notebooks | Interactive workflows |
| Basic movement metrics | Distance and speed calculations |
| Animation prototype | Time-evolving trajectories |

---

# 16. Success Criteria

Part 1 is considered successful when:

1. All fish tracks can be loaded reproducibly.
2. Tracks render correctly on Gulf of Alaska maps.
3. Fish movement can be animated through time.
4. Basic migration metrics are reproducible.
5. Code is modular enough for Part 2 environmental integration.
6. Future AI coding assistants can implement functionality directly from this specification.

