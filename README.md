# tgf_wmo_plugins

TethysDash visualizations for the WMO Guatemala impact-based forecasting
training, in English and Spanish.

Every plugin ships as a matched pair — `_en` and `_es`. The pair shares one
implementation and differs only in the strings it renders, so the two languages
cannot disagree about a number.

## Plugins

| entry point | type | what it shows |
|---|---|---|
| `wmo_impact_summary_en` / `_es` | table | People, buildings and roads in each hazard level |
| `wmo_hazard_layer_en` / `_es` | map_layer | Hazard classification as map polygons |
| `wmo_impact_layer_en` / `_es` | map_layer | Buildings and roads coloured by hazard level |
| `wmo_storm_card_en` / `_es` | card | Magnitude, flooded area and depth for one storm |
| `wmo_storm_impact_summary_en` / `_es` | table | People, buildings and roads by flood depth for one storm |
| `wmo_storm_impact_layer_en` / `_es` | map_layer | Buildings and roads coloured by flood depth for one storm |

The three map layers are `dynamic_map_layer`s: they re-fetch whenever a bound
variable input changes, which is what makes the thresholds and the storm slider
interactive.

## Two products, two questions

The plugins split into two families that answer different questions, and the
distinction is worth keeping straight when building a dashboard:

- **Hazard** (`impact_summary`, `hazard_layer`, `impact_layer`) works from four
  EF5 **exceedance-probability** rasters. Each hazard level has its own
  probability gate, and a feature takes the level of the deepest flood threshold
  it clears. It answers *"what are the odds of at least 30 cm here"*.
- **Storm** (`storm_card`, `storm_impact_summary`, `storm_impact_layer`) samples
  **depth** from one storm of a 200-member RainyDay ensemble. It answers
  *"in storm 150, how deep is the water on this building"*. Depth is a physical
  quantity, so the bands need no reference to a threshold.

The two datasets sit on exactly the same grid — EPSG:3857, 424×319, 5 m cells,
identical origin — so no reprojection or resampling happens anywhere.

## Installing

```bash
pip install -e .
```

Then restart the Tethys server; TethysDash discovers plugins through the
`intake.drivers` entry-point group at startup.

## Adding or changing text

All user-facing text lives in `strings.py`, keyed by language. Hazard levels and
depth bands are keyed by their numeric class value — the value the raster and the
feature attributes actually carry — so a translation can never change a
classification.

`check_parity()` runs at import and raises if the two dictionaries have drifted,
so a missing translation fails at install time rather than in front of a room of
trainees.

## Data

Everything is read from a public S3 bucket; nothing is bundled.

| dataset | what it is |
|---|---|
| `floodmaps_test/` | Zarr store, 200-storm RainyDay ensemble, `depth` in metres |
| `floodmaps_test/ensemble_stats.csv` | Precomputed per-storm summary |
| `Guatemala_IBF/impact_features.geojson` | Buildings and roads with sampled probabilities |
| `Guatemala_IBF/impact_features.csv` | The same rows without geometry, for tables |
| `PBI_Actividad_2/prob_*.tif` | The four exceedance-probability rasters |

Two caveats that matter when reading the output:

- **The probability layer depths are mislabelled upstream.** The filenames say
  7.62 / 10 / 30 / 76 cm, but three of the four are actually 15.24 / 30.48 /
  60.96 cm. The ordering is correct either way, so the classification is
  unaffected — but the labels are not what they claim.
- **The 76 cm layer only ever contains 0 or 0.2.** Any gate above 0.2 therefore
  makes the top hazard level unreachable, not merely rare.

## Site

Santa Inés Petapa, Guatemala. The model domain is 3.38 km² and covers 5,029 of
the 5,147 features in the geopackage; the remaining 118 fall outside it and never
appear as affected, whatever the storm.
