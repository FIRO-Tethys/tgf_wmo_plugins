"""Every user-facing string, in English and Spanish.

The plugins come in an `_en` and an `_es` variant. Keeping the text in one table
rather than in two parallel sets of modules is what stops the pair drifting: a
new string has to be added to both dictionaries or `check_parity()` fails, and
nothing that computes a number lives here.

Hazard levels and depth bands are keyed by their numeric class value, which is
what the raster and the feature attributes actually carry, so a translation can
never change a classification.
"""

LANGUAGES = ("en", "es")

STRINGS = {
    "en": {
        "language": "English",
        "group": "Flood Maps (English)",
        # Hazard levels, keyed by the `peligro` class value.
        "levels": {1: "Low", 2: "Medium", 3: "High", 4: "Severe"},
        # Depth bands, keyed by the `banda` class value.
        "bands": {
            1: "0.05 - 0.3 m",
            2: "0.3 - 1 m",
            3: "1 - 2 m",
            4: "2 m or more",
        },
        "buildings": "buildings",
        "roads": "roads",
        # Shared table columns.
        "col_level": "Level",
        "col_depth": "Depth",
        "col_buildings": "Buildings",
        "col_population": "Population",
        "col_area": "Area (m²)",
        "col_roads_km": "Roads (km)",
        "col_pop_share": "% of population",
        "row_total_hazard": "TOTAL at risk",
        "row_total_flooded": "TOTAL affected",
        "out_of_range": "Out of range",
        # Hazard (probability-gated) plugins.
        "hazard_summary_title": "Impact by hazard level",
        "hazard_summary_label": "Flood Impact Summary",
        "hazard_summary_desc": (
            "People, buildings and roads in each flood hazard level, "
            "classified from the same probability gates as the hazard map."
        ),
        "hazard_layer_name": "Hazard classification",
        "hazard_layer_label": "Flood Hazard Layer",
        "hazard_layer_desc": (
            "Flood hazard classification from four EF5 exceedance-probability "
            "rasters, as map polygons. Re-classifies when a gate changes."
        ),
        "hazard_legend": "Hazard",
        "impact_layer_name": "Buildings and roads at risk",
        "impact_layer_label": "Flood Impact Layer",
        "impact_layer_desc": (
            "Buildings and roads coloured by flood hazard level, using the "
            "same probability gates as the hazard map."
        ),
        # Storm (depth-sampled) plugins.
        "storm_summary_title": "Impact by depth — storm {index}",
        "storm_summary_label": "Storm Impact Summary",
        "storm_summary_desc": (
            "People, buildings and roads by flood depth for one storm of the "
            "ensemble. The bands are depths, so they read without reference "
            "to a threshold."
        ),
        "storm_layer_name": "Flooded buildings and roads",
        "storm_layer_label": "Storm Impact Layer",
        "storm_layer_desc": (
            "Buildings and roads coloured by how deep the water gets on them "
            "in one storm of the ensemble."
        ),
        "depth_legend": "Depth",
        "storm_card_label": "Storm Summary",
        "storm_card_desc": (
            "Magnitude, flooded area and depth for one storm of the ensemble."
        ),
        "card_magnitude": "Magnitude",
        "card_flooded_area": "Flooded area",
        "card_max_depth": "Max depth",
        "card_mean_depth": "Mean depth (wet)",
        "card_flooding": "Flooding",
        "card_no_flooding": "None at this magnitude",
        # Progress messages.
        "msg_reading": "Reading probability layers...",
        "msg_classifying": "Classifying hazard...",
        "msg_polygons": "Building polygons...",
        "msg_loading_features": "Loading buildings and roads...",
        "msg_sampling": "Sampling depth...",
        "msg_done": "Done",
        "msg_at_risk": "{count:,} elements at risk",
        "msg_flooded": "{count:,} elements flooded",
    },
    "es": {
        "language": "Español",
        "group": "Mapas de Inundación (Español)",
        "levels": {1: "Bajo", 2: "Medio", 3: "Alto", 4: "Severo"},
        "bands": {
            1: "0.05 - 0.3 m",
            2: "0.3 - 1 m",
            3: "1 - 2 m",
            4: "2 m o más",
        },
        "buildings": "edificios",
        "roads": "carreteras",
        "col_level": "Nivel",
        "col_depth": "Profundidad",
        "col_buildings": "Edificios",
        "col_population": "Población",
        "col_area": "Área (m²)",
        "col_roads_km": "Carreteras (km)",
        "col_pop_share": "% de la población",
        "row_total_hazard": "TOTAL en peligro",
        "row_total_flooded": "TOTAL afectado",
        "out_of_range": "Fuera de rango",
        "hazard_summary_title": "Impacto por nivel de peligro",
        "hazard_summary_label": "Resumen de Impacto",
        "hazard_summary_desc": (
            "Personas, edificios y carreteras en cada nivel de peligro por "
            "inundación, clasificados con los mismos umbrales de probabilidad "
            "que el mapa de peligro."
        ),
        "hazard_layer_name": "Clasificación de peligro",
        "hazard_layer_label": "Capa de Peligro",
        "hazard_layer_desc": (
            "Clasificación de peligro por inundación a partir de cuatro "
            "rásteres de probabilidad de excedencia EF5, como polígonos. Se "
            "reclasifica cuando cambia un umbral."
        ),
        "hazard_legend": "Peligro",
        "impact_layer_name": "Edificios y carreteras en peligro",
        "impact_layer_label": "Capa de Impacto",
        "impact_layer_desc": (
            "Edificios y carreteras coloreados por nivel de peligro, usando "
            "los mismos umbrales de probabilidad que el mapa de peligro."
        ),
        "storm_summary_title": "Impacto por profundidad — tormenta {index}",
        "storm_summary_label": "Resumen de Impacto por Tormenta",
        "storm_summary_desc": (
            "Personas, edificios y carreteras por profundidad de inundación "
            "para una tormenta del conjunto. Las bandas son profundidades, "
            "así que se leen sin referencia a un umbral."
        ),
        "storm_layer_name": "Edificios y carreteras inundados",
        "storm_layer_label": "Capa de Impacto por Tormenta",
        "storm_layer_desc": (
            "Edificios y carreteras coloreados según la profundidad que "
            "alcanza el agua sobre ellos en una tormenta del conjunto."
        ),
        "depth_legend": "Profundidad",
        "storm_card_label": "Resumen de Tormenta",
        "storm_card_desc": (
            "Magnitud, área inundada y profundidad de una tormenta del conjunto."
        ),
        "card_magnitude": "Magnitud",
        "card_flooded_area": "Área inundada",
        "card_max_depth": "Profundidad máxima",
        "card_mean_depth": "Profundidad media (mojado)",
        "card_flooding": "Inundación",
        "card_no_flooding": "Ninguna con esta magnitud",
        "msg_reading": "Leyendo capas de probabilidad...",
        "msg_classifying": "Clasificando peligro...",
        "msg_polygons": "Generando polígonos...",
        "msg_loading_features": "Cargando edificios y carreteras...",
        "msg_sampling": "Muestreando profundidad...",
        "msg_done": "Listo",
        "msg_at_risk": "{count:,} elementos en peligro",
        "msg_flooded": "{count:,} elementos inundados",
    },
}


def check_parity():
    """Raise if the two dictionaries have drifted apart.

    Called at import so a missing translation is a hard failure at install time
    rather than a KeyError in front of a room of trainees.
    """
    en, es = set(STRINGS["en"]), set(STRINGS["es"])
    if en != es:
        missing_es = sorted(en - es)
        missing_en = sorted(es - en)
        raise ValueError(
            f"strings out of sync -- missing from es: {missing_es}, "
            f"missing from en: {missing_en}"
        )
    for key in ("levels", "bands"):
        if set(STRINGS["en"][key]) != set(STRINGS["es"][key]):
            raise ValueError(f"{key} class values differ between languages")


check_parity()
