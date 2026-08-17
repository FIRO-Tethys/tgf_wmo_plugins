"""Flood hazard classification as a dynamic map layer.

A map layer config can only point at a URL, and there is no endpoint that serves
a computed raster, so the classified grid is vectorized: each connected run of
equal class becomes one polygon carrying a `peligro` attribute. On this dataset
that comes to roughly 600 polygons.

Being a dynamic map_layer, `fetch_features` re-runs whenever a bound variable
input changes, so wiring the four gates to variable inputs makes the
classification interactive.
"""

import rasterio
from rasterio.features import shapes
from tethysapp.tethysdash.plugin_helpers import (
    LayerConfigurationBuilder,
    TethysDashPlugin,
)

from tgf_wmo_plugins.classification import (
    LEVELS,
    NODATA,
    PROB_URLS,
    clasificar_peligro,
)
from tgf_wmo_plugins.impact_summary import DEFAULT_GATES
from tgf_wmo_plugins.strings import STRINGS

# Vectorizing a heavily fragmented classification could produce a huge payload.
# Warn loudly rather than silently shipping megabytes of geometry.
POLYGON_WARN_LIMIT = 20000


class BaseHazardLayer(TethysDashPlugin):
    LANG = None
    type = "map_layer"
    dynamic_map_layer = True
    args = {
        "umbral_bajo": "number",
        "umbral_medio": "number",
        "umbral_alto": "number",
        "umbral_severo": "number",
    }

    def run(self):
        """Configure-time scaffold: source binding, style and legend."""
        s = STRINGS[self.LANG]
        builder = LayerConfigurationBuilder(s["hazard_layer_name"], "GeoJSON")
        # received_args, not args: `self.args` is the schema, while the runtime
        # re-invocation needs the configured values, including any "${Variable}"
        # bindings to resolve later.
        builder.set_plugin_source(self.name, self.received_args)
        builder.set_style(self._style(s))
        builder.set_legend(
            {
                "title": s["hazard_legend"],
                "items": [
                    {"label": s["levels"][value], "color": color, "symbol": "square"}
                    for value, color in LEVELS
                ],
            }
        )
        return builder.build()

    def fetch_features(self):
        """Runtime features: re-run on load and on variable-input change."""
        s = STRINGS[self.LANG]
        urls = [PROB_URLS[k] for k in ("7p62", "10cm", "30cm", "76cm")]
        umbrales = {
            1: self._gate("umbral_bajo", DEFAULT_GATES[1]),
            2: self._gate("umbral_medio", DEFAULT_GATES[2]),
            3: self._gate("umbral_alto", DEFAULT_GATES[3]),
            4: self._gate("umbral_severo", DEFAULT_GATES[4]),
        }

        self.send_update(s["msg_reading"], percentage_complete=10)
        layers, transform, crs = self._read(urls)

        self.send_update(s["msg_classifying"], percentage_complete=50)
        peligro = clasificar_peligro(*layers, umbrales)

        self.send_update(s["msg_polygons"], percentage_complete=75)
        features = self._vectorize(s, peligro, transform)

        self.send_update(s["msg_done"], percentage_complete=100)
        return {
            "type": "FeatureCollection",
            "features": features,
            "crs": {"type": "name", "properties": {"name": str(crs)}},
        }

    def _gate(self, arg, default):
        try:
            return float(self.get_arg(arg, default))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _read(urls):
        layers, transform, crs = [], None, None
        for url in urls:
            with rasterio.open(url) as ds:
                layers.append(ds.read(1, masked=True))
                if transform is None:
                    transform, crs = ds.transform, ds.crs
        shapes_seen = {layer.shape for layer in layers}
        if len(shapes_seen) != 1:
            raise ValueError(
                f"the four probability rasters must share a grid, got {shapes_seen}"
            )
        return layers, transform, crs

    @staticmethod
    def _vectorize(s, peligro, transform):
        """One polygon per connected run of equal class.

        Normal and NoData are left out: Normal is ~90% of the grid and would
        dominate the payload while adding nothing a basemap does not show.
        """
        mask = (peligro > 0) & (peligro != NODATA)
        features = [
            {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "peligro": int(value),
                    "nivel": s["levels"].get(int(value), ""),
                },
            }
            for geometry, value in shapes(peligro, mask=mask, transform=transform)
        ]
        if len(features) > POLYGON_WARN_LIMIT:
            print(
                f"hazard layer: {len(features):,} polygons exceeds "
                f"{POLYGON_WARN_LIMIT:,}; the classification is heavily "
                "fragmented and the payload will be large"
            )
        return features

    @staticmethod
    def _style(s):
        """Rule-based styling keyed on the `peligro` attribute.

        The shape matters: createJsonStyleFunction reads `geometryType` (not
        `geometry`), takes the condition from `conditionField`/`conditionType`
        on the rule itself, and merges the rule's own keys as the style -- there
        is no nested `style` object, and the operator is "=" not "==". A rule in
        any other shape silently never matches, leaving every feature grey.
        """
        return {
            "default": {
                "polygon": {"fill": "#9e9e9e", "stroke": "#9e9e9e", "strokeWidth": "0"}
            },
            "rules": [
                {
                    "name": s["levels"][value],
                    "geometryType": "polygon",
                    "conditionField": "peligro",
                    "conditionType": "=",
                    "conditionValue": str(value),
                    "fill": color,
                    "stroke": color,
                    "strokeWidth": "0",
                }
                for value, color in LEVELS
            ],
        }


class HazardLayerEN(BaseHazardLayer):
    LANG = "en"
    name = "wmo_hazard_layer_en"
    label = f"{STRINGS['en']['hazard_layer_label']} ({STRINGS['en']['language']})"
    group = STRINGS["en"]["group"]
    tags = ["flood", "hazard", "EF5", "map_layer", "dynamic", "english"]
    description = STRINGS["en"]["hazard_layer_desc"]


class HazardLayerES(BaseHazardLayer):
    LANG = "es"
    name = "wmo_hazard_layer_es"
    label = f"{STRINGS['es']['hazard_layer_label']} ({STRINGS['es']['language']})"
    group = STRINGS["es"]["group"]
    tags = ["inundación", "peligro", "EF5", "map_layer", "dinámico", "español"]
    description = STRINGS["es"]["hazard_layer_desc"]
