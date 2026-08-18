# Workshop notebooks

Two walkthroughs of the analysis behind the Guatemala hands-on dashboards. They
derive the same numbers the dashboard plugins produce, but as plain code you can
read and re-run, so the logic is visible rather than hidden behind a plugin class.

| notebook | dashboard | question it answers |
|---|---|---|
| `02_storm_impact.ipynb` | Hands On 2 | How deep did the water get on each building and road, in one storm? |
| `03_hazard_classification.ipynb` | Hands On 3 | What are the odds of at least 30 cm here, and what does that classify as? |

Each ends with the real plugin source and notes on how the notebook logic maps
onto it.

## Running them

All data is read over HTTPS from a public S3 bucket — nothing to download first,
but you do need a network connection, and a few cells take 10–30 seconds while
they pull rasters.

```bash
pip install jupyter matplotlib "zarr>=3.0" fsspec aiohttp \
            rasterio geopandas shapely numpy pandas
jupyter lab
```

If you have already installed this package (`pip install -e .`), only `jupyter`
and `matplotlib` are missing.

## A note on the exercises

Both notebooks are written to be re-run with different values — change the storm
index, move the thresholds — and several sections ask you to do exactly that.
The final section of each lists suggested experiments.

Two things the notebooks deliberately flag rather than paper over:

- **The ensemble magnitudes are placeholders.** The mm labels on the storm picker
  are illustrative, not measured. `02` explains where they come from.
- **Three of the four depth labels are wrong upstream.** The filenames say
  7.62 / 10 / 30 / 76 cm; three are actually 15.24 / 30.48 / 60.96 cm. The
  ordering is right, so the classification is unaffected, but do not quote the
  centimetre figures. `03` covers this.

Section 5 of `03` also works through recovering an undocumented sampling method
from the data itself, and stops at "~98% plus an open question" rather than
claiming a match it cannot support. That pattern — verify, then report the
residual honestly — is worth more than either notebook's specific numbers.
