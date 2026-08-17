"""Shared core for per-storm impact on buildings and roads.

The RainyDay ensemble and the IBF buildings/roads turn out to sit on exactly the
same grid -- EPSG:3857, 424x319, 5 m cells, identical origin -- so a storm's depth
raster can be sampled onto the features with no reprojection or resampling at all.

This answers a different question from `impact_summary`. That one reports exposure
against exceedance probabilities ("what are the odds of 30 cm here"); this reports
depth in one specific storm ("in storm 150, how deep at each building"). Depth is a
physical quantity, so a band needs no explanation the way a probability gate does.
"""

from functools import lru_cache

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import rasterize
from shapely import set_precision

from tgf_wmo_plugins.common import DEFAULT_STORE, FEATURES_URL, open_zarr_store

# Ascending, so assigning in order lets the deepest band a feature reaches win --
# the same escalation clasificar_peligro uses for probabilities.
#
# The 0.05 m floor is the store's own `extent_threshold_m`: below it the model
# does not consider a cell wet. The rest are round depths chosen to be read
# without a legend -- ankle, knee/vehicle, storey.
DEPTH_BANDS = [
    (1, "green", 0.05),
    (2, "yellow", 0.30),
    (3, "red", 1.00),
    (4, "purple", 2.00),
]

# Coordinate snapping for the returned geometry, in the store's 5 m grid units.
PRECISION_M = 0.5


@lru_cache(maxsize=2)
def store_grid(store_url=DEFAULT_STORE):
    """The store's affine transform, shape and CRS."""
    group = open_zarr_store(store_url)
    attrs = dict(group.attrs)
    transform = rasterio.Affine(*attrs["transform"])
    rows, cols = attrs["grid_shape"]
    return transform, (rows, cols), attrs["crs"]


@lru_cache(maxsize=2)
def load_features(url=FEATURES_URL, store_url=DEFAULT_STORE):
    """Buildings and roads in the store's CRS, ready to rasterise against it."""
    _transform, _shape, crs = store_grid(store_url)
    gdf = gpd.read_file(url).to_crs(crs)
    # to_crs hands back full float precision, undoing the snapping the
    # precomputed source was written with and tripling the GeoJSON payload.
    # 0.5 m is a tenth of a cell, so it cannot move a feature into another band.
    gdf["geometry"] = set_precision(gdf.geometry.values, PRECISION_M)
    return gdf[~gdf.geometry.is_empty]


@lru_cache(maxsize=2)
def feature_id_grid(url=FEATURES_URL, store_url=DEFAULT_STORE):
    """A grid of 1-based feature ids, and the count of features that reach it.

    This is the expensive step and it does not depend on the storm, so it is paid
    once and reused for every index. all_touched matches how the IBF
    probabilities were sampled onto these same features.

    Features outside the 3.38 km2 model domain get no cells. They are counted
    here so percentages can be reported against what the model actually covers
    rather than against the whole geopackage.
    """
    transform, shape, _crs = store_grid(store_url)
    gdf = load_features(url, store_url)
    ids = rasterize(
        ((geom, i + 1) for i, geom in enumerate(gdf.geometry)),
        out_shape=shape,
        transform=transform,
        fill=0,
        all_touched=True,
        dtype="int32",
    )
    in_domain = np.unique(ids)
    return ids, int((in_domain > 0).sum())


def feature_max_depth(index, url=FEATURES_URL, store_url=DEFAULT_STORE):
    """Deepest water over each feature's own footprint, in metres.

    Reads one storm's chunk (~540 KB) rather than the whole 108 MB array.
    Features outside the domain, and dry ones, come back as 0.
    """
    group = open_zarr_store(store_url)
    depth = np.asarray(group["depth"][index], dtype="float32")
    # The store's nodata is a large negative float; anything non-finite or below
    # zero is "no water", not a depth.
    depth = np.where(np.isfinite(depth) & (depth > 0), depth, 0.0)

    ids, _in_domain = feature_id_grid(url, store_url)
    gdf = load_features(url, store_url)
    per_feature = np.zeros(len(gdf) + 1, dtype="float32")
    np.maximum.at(per_feature, ids.ravel(), depth.ravel())
    # Drop index 0, which accumulates every cell not covered by a feature.
    return per_feature[1:]


def classify_depth(depths):
    """Band value per feature: 0 for dry, then 1..4 by increasing depth."""
    banda = np.zeros(len(depths), dtype="uint8")
    for value, _color, floor in DEPTH_BANDS:
        banda[depths >= floor] = value
    return banda


def banded_features(index, url=FEATURES_URL, store_url=DEFAULT_STORE):
    """Features with a depth band attached, dry ones dropped.

    Returns a copy, so callers may modify it without disturbing the cache.
    """
    gdf = load_features(url, store_url).copy()
    depths = feature_max_depth(index, url, store_url)
    # Classify on the raw depth, round only for display. Rounding first promoted
    # 14 features sitting just under 0.05 m into the wet band -- a display
    # concern silently changing the answer.
    gdf["banda"] = classify_depth(depths)
    gdf["profundidad_m"] = depths.round(2)
    return gdf[gdf.banda > 0]
