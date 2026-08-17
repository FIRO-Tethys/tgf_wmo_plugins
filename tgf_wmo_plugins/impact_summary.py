"""Exposure by hazard class: people, buildings and roads in each level.

Applies the notebook's `clasificar_peligro` rule to features instead of pixels.
Each building and road in the IBF geopackage already carries the four exceedance
probabilities, sampled as the maximum over its own footprint, so the same
escalating gates classify a feature directly.

Reads a slim precomputed CSV rather than the 37.7 MB geopackage, whose attributes
take about 160 s to pull over /vsicurl/.
"""

from functools import lru_cache

import pandas as pd
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin

from tgf_wmo_plugins.classification import LEVELS
from tgf_wmo_plugins.common import (
    FEATURES_CSV_URL,
    PROB_FIELDS,
    TOTAL_POPULATION,
)
from tgf_wmo_plugins.strings import STRINGS

# The notebook's defaults, one gate per hazard level, keyed by class value.
DEFAULT_GATES = {1: 0.3, 2: 0.2, 3: 0.1, 4: 0.15}


@lru_cache(maxsize=4)
def _load(url):
    return pd.read_csv(url)


class BaseImpactSummary(TethysDashPlugin):
    """Language-independent computation; subclasses only choose the strings."""

    LANG = None
    type = "table"
    args = {
        "umbral_bajo": "number",
        "umbral_medio": "number",
        "umbral_alto": "number",
        "umbral_severo": "number",
    }

    def run(self):
        s = STRINGS[self.LANG]
        df = _load(FEATURES_CSV_URL).copy()
        gates = {
            1: self._gate("umbral_bajo", DEFAULT_GATES[1]),
            2: self._gate("umbral_medio", DEFAULT_GATES[2]),
            3: self._gate("umbral_alto", DEFAULT_GATES[3]),
            4: self._gate("umbral_severo", DEFAULT_GATES[4]),
        }

        # Escalating assignment: the deepest threshold a feature clears wins,
        # exactly as clasificar_peligro does for pixels.
        df["peligro"] = 0
        for field, (value, _color) in zip(PROB_FIELDS, LEVELS):
            df.loc[df[field] >= gates[value], "peligro"] = value

        # Deepest level first. Normal is left out: it is everything the gates did
        # not catch, so it carries no exposure and only pads the table.
        rows = [
            self._row(s, s["levels"][value], df[df.peligro == value])
            for value, _color in reversed(LEVELS)
        ]
        rows.append(self._row(s, s["row_total_hazard"], df[df.peligro > 0]))
        return {"title": s["hazard_summary_title"], "data": rows}

    def _gate(self, arg, default):
        """Gates arrive from the GUI as strings."""
        try:
            return float(self.get_arg(arg, default))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _row(s, name, group):
        buildings = group[group.tipo == "edificio"]
        return {
            s["col_level"]: name,
            s["col_buildings"]: f"{len(buildings):,}",
            s["col_population"]: f"{group.poblacion.sum():,.0f}",
            s["col_area"]: f"{group.area_m2.sum():,.0f}",
            s["col_roads_km"]: f"{group.longitud_m.sum() / 1000:,.1f}",
            s["col_pop_share"]: (
                f"{100 * group.poblacion.sum() / TOTAL_POPULATION:.2f}%"
            ),
        }


class ImpactSummaryEN(BaseImpactSummary):
    LANG = "en"
    name = "wmo_impact_summary_en"
    label = f"{STRINGS['en']['hazard_summary_label']} ({STRINGS['en']['language']})"
    group = STRINGS["en"]["group"]
    tags = ["flood", "impact", "IBF", "exposure", "table", "english"]
    description = STRINGS["en"]["hazard_summary_desc"]


class ImpactSummaryES(BaseImpactSummary):
    LANG = "es"
    name = "wmo_impact_summary_es"
    label = f"{STRINGS['es']['hazard_summary_label']} ({STRINGS['es']['language']})"
    group = STRINGS["es"]["group"]
    tags = ["inundación", "impacto", "IBF", "exposición", "tabla", "español"]
    description = STRINGS["es"]["hazard_summary_desc"]
