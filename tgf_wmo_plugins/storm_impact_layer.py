"""Buildings and roads coloured by flood depth for one storm, as a map layer."""

import json

from tethysapp.tethysdash.plugin_helpers import (
    LayerConfigurationBuilder,
    TethysDashPlugin,
)

from tgf_wmo_plugins.common import FIRST_WET_STORM, STORM_OPTIONS, coerce_index
from tgf_wmo_plugins.storm_impact import DEPTH_BANDS, banded_features, store_grid
from tgf_wmo_plugins.strings import STRINGS


class BaseStormImpactLayer(TethysDashPlugin):
    LANG = None
    type = "map_layer"
    dynamic_map_layer = True
    args = {"index": STORM_OPTIONS}

    def run(self):
        s = STRINGS[self.LANG]
        builder = LayerConfigurationBuilder(s["storm_layer_name"], "GeoJSON")
        builder.set_plugin_source(self.name, self.received_args)
        builder.set_style(self._style(s))
        builder.set_legend(
            {
                "title": s["depth_legend"],
                "items": [
                    {"label": s["bands"][value], "color": color, "symbol": "square"}
                    for value, color, _floor in DEPTH_BANDS
                ],
            }
        )
        return builder.build()

    def fetch_features(self):
        s = STRINGS[self.LANG]
        index = coerce_index(self.get_arg("index", FIRST_WET_STORM), FIRST_WET_STORM)

        self.send_update(s["msg_sampling"], percentage_complete=40)
        flooded = banded_features(index).copy()
        flooded["nivel"] = flooded.banda.map(s["bands"])

        self.send_update(
            s["msg_flooded"].format(count=len(flooded)), percentage_complete=100
        )
        columns = [
            "tipo",
            "nivel",
            "banda",
            "profundidad_m",
            "poblacion",
            "area_m2",
            "longitud_m",
        ]
        collection = json.loads(flooded[columns + ["geometry"]].to_json())
        # The store's grid is already EPSG:3857, which OpenLayers resolves
        # natively -- no proj4 needed and no reprojection on the way out.
        _transform, _shape, crs = store_grid()
        collection["crs"] = {"type": "name", "properties": {"name": crs}}
        return collection

    @staticmethod
    def _style(s):
        """Rule-based styling on `banda`. See hazard_layer._style for the shape."""
        rules = []
        for value, color, _floor in DEPTH_BANDS:
            condition = {
                "conditionField": "banda",
                "conditionType": "=",
                "conditionValue": str(value),
            }
            rules.append(
                {
                    "name": f"{s['bands'][value]} ({s['buildings']})",
                    "geometryType": "polygon",
                    **condition,
                    "fill": color,
                    "stroke": color,
                    "strokeWidth": "1",
                }
            )
            rules.append(
                {
                    "name": f"{s['bands'][value]} ({s['roads']})",
                    "geometryType": "linestring",
                    **condition,
                    "stroke": color,
                    "strokeWidth": "3",
                }
            )
        return {
            "default": {
                "polygon": {"fill": "#9e9e9e", "stroke": "#9e9e9e", "strokeWidth": "0"},
                "linestring": {"stroke": "#9e9e9e", "strokeWidth": "1"},
            },
            "rules": rules,
        }


class StormImpactLayerEN(BaseStormImpactLayer):
    LANG = "en"
    name = "wmo_storm_impact_layer_en"
    label = f"{STRINGS['en']['storm_layer_label']} ({STRINGS['en']['language']})"
    group = STRINGS["en"]["group"]
    tags = ["flood", "impact", "zarr", "storm", "map_layer", "dynamic", "english"]
    description = STRINGS["en"]["storm_layer_desc"]


class StormImpactLayerES(BaseStormImpactLayer):
    LANG = "es"
    name = "wmo_storm_impact_layer_es"
    label = f"{STRINGS['es']['storm_layer_label']} ({STRINGS['es']['language']})"
    group = STRINGS["es"]["group"]
    tags = ["inundación", "impacto", "zarr", "tormenta", "map_layer", "español"]
    description = STRINGS["es"]["storm_layer_desc"]
