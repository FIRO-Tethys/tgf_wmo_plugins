.. Guatemala hands-on exercise 3 solution, English. A Spanish translation lives
.. alongside this file as exercise_3_es.rst.

==============================================================
Exercise 3 — Hazard classification with adjustable thresholds
==============================================================

Building **Guatemala Hands On 3 (English)** step by step.

.. admonition:: Start here

   Read `Getting Started <getting_started_en.rst>`_ first. It covers installing
   the plugins, the data bucket, and the motions this guide refers to — creating
   a dashboard, entering edit mode, adding an item.

   This exercise reuses the five raster layers from
   `Exercise 1 <exercise_1_en.rst>`_. Building that one first will save you time.

.. contents:: On this page
   :depth: 2
   :local:
   :backlinks: none


What you are building
=====================

A full-window map carrying the five rasters from exercise 1 plus two computed
layers: a hazard classification and the buildings and roads that fall inside it.
Four number inputs across the top set the probability threshold for each hazard
level, and an impact table sits under them. Change a threshold and the
classification, the affected features and the table all recompute.

.. figure:: images/ex3-finished.png
   :alt: The finished exercise 3 dashboard
   :width: 100%

   **Screenshot:** the finished dashboard — full-window map, four threshold
   inputs along the top, impact table on the right.

This is the most interactive of the three, and the one where what the interface
*implies* deserves the most scrutiny.

.. tip::

   ``notebooks/03_hazard_classification.ipynb`` derives this classification as
   plain Python, including the gate sweep that shows what each threshold controls.
   Worth running first if you want to understand the analysis before assembling
   the interface.


Understanding the four thresholds
=================================

Each hazard level is tied to **one** depth threshold and has its **own**
probability gate:

.. list-table::
   :header-rows: 1
   :widths: 18 32 25 25

   * - Level
     - Driven by
     - Colour
     - Notebook default gate
   * - Low
     - P(≥ 7.6 cm)
     - green
     - 0.3
   * - Medium
     - P(≥ 10 cm)
     - yellow
     - 0.2
   * - High
     - P(≥ 30 cm)
     - red
     - 0.1
   * - Severe
     - P(≥ 76 cm)
     - purple
     - 0.15

A cell takes the level of the **deepest** threshold whose gate it clears.

.. warning::

   Two things to know before you present this, both covered at length in
   ``notebooks/03_hazard_classification.ipynb``:

   **The 76 cm raster contains only the values 0 and 0.2.** At most 2 of 10
   ensemble members ever reached that depth anywhere in the domain. So any
   Severe gate above 0.2 makes the Severe class *unreachable* — the colour simply
   never appears, and a viewer moving that slider gets no feedback distinguishing
   "nothing qualifies" from "the control is broken".

   **Three of the four depth labels are wrong upstream.** The files say
   7.62 / 10 / 30 / 76 cm; three are actually 15.24 / 30.48 / 60.96 cm (6, 12
   and 24 inches). The ordering is right, so the classification is unaffected,
   but do not quote the centimetre figures as verified.


Step 1 — Create the dashboard and the base map input
====================================================

Create a new dashboard (see
`Creating a dashboard <getting_started_en.rst#creating-a-dashboard>`_) with:

* **Name**: ``Guatemala Hands On 3 (English)``
* **Description**: ``Solution for WMO Guatemala Hands On Exercise #3``

Turn on **Unrestricted Grid Item Movement**, then add a **Base Map** variable
input as in
`Exercise 1, step 5 <exercise_1_en.rst#step-5-add-the-base-map-selector>`_. Give
it a border on all four sides and a white background.


Step 2 — Add the four threshold inputs
======================================

Build all four before the layers that consume them. Each is a **Variable Input**
with ``variable_options_source`` set to ``number``:

.. list-table::
   :header-rows: 1
   :widths: 44 14 14 14 14

   * - ``variable_name``
     - min
     - max
     - step
     - ``initial_value``
   * - ``Low Threshold (P(≥7.6 cm))``
     - 0
     - 1
     - 0.05
     - 0.8
   * - ``Medium Threshold (P(≥10 cm))``
     - 0
     - 1
     - 0.05
     - 0.8
   * - ``High Threshold (P(≥30 cm))``
     - 0
     - 1
     - 0.05
     - 0.8
   * - ``Severe Threshold (P(≥76 cm))``
     - 0
     - 1
     - 0.05
     - 0.8

For each one:

#. **Add Dashboard Item** → **Edit** → **Visualization Type**
   **Variable Input**.
#. Set ``variable_name`` from the table. Tick ``show_label``.
#. Set ``variable_options_source`` to ``number``, then fill the metadata:
   **Minimum** ``0``, **Maximum** ``1``, **Step** ``0.05``.
#. Set ``initial_value`` to ``0.8``.
#. **Settings** tab: **Background Color** ``#ffffff``, and a top border. Give the
   leftmost input a left border and the rightmost a right border, so the four
   read as one strip.
#. Save, and place them side by side across the top of the map area.

.. note::

   The variable names carry their meaning — ``Low Threshold (P(≥7.6 cm))`` rather
   than ``umbral_bajo``. The name is what the viewer reads above the input, so it
   has to say which probability is being gated. It is also the key other items
   reference, so choose it before wiring anything and avoid renaming later.

.. figure:: images/ex3-threshold-inputs.png
   :alt: The four threshold variable inputs across the top of the dashboard
   :width: 100%

   **Screenshot:** the four threshold inputs side by side, each showing its
   label and value.


Step 3 — Add the map and the five rasters
=========================================

Add a **Map** item and build the same five raster layers as
`Exercise 1 <exercise_1_en.rst>`_ — same names, URLs, ramps and bounds. Set
**Base Map** to ``${Base Map}`` and tick **Layer Control**.

The quickest route, if you still have exercise 1: open its map item's three-dot
menu, choose **Export**, then use **Import Dashboard Item** here and edit the
imported copy. That carries all five layers over intact.


Step 4 — Add the hazard classification layer
============================================

#. **Add Layer** on the map.
#. **Source** tab: **Source Type** → **Flood Hazard Layer (English)**.
#. Four arguments appear. Bind each to its variable:

   .. list-table::
      :header-rows: 1
      :widths: 26 74

      * - Argument
        - Value
      * - ``umbral_bajo``
        - ``${Low Threshold (P(≥7.6 cm))}``
      * - ``umbral_medio``
        - ``${Medium Threshold (P(≥10 cm))}``
      * - ``umbral_alto``
        - ``${High Threshold (P(≥30 cm))}``
      * - ``umbral_severo``
        - ``${Severe Threshold (P(≥76 cm))}``

#. Click **Fetch plugin defaults**. The layer is named
   **Hazard classification**, styled with four rules on the ``peligro``
   attribute, and given a four-item **Hazard** legend.
#. Save the layer.

.. note::

   The argument names are Spanish (``umbral_bajo`` = "low threshold") because the
   plugins were ported from the original UFFIS notebook and the internal names
   were kept so the two can be read side by side. Only the labels were
   translated. This is worth mentioning if attendees notice the mismatch.

.. figure:: images/ex3-hazard-layer-source.png
   :alt: The hazard layer source configuration with four bound thresholds
   :width: 100%

   **Screenshot:** the **Source** tab for the hazard layer, four arguments bound
   to the four threshold variables.


Step 5 — Add the affected-features layer
========================================

#. **Add Layer** again.
#. **Source** tab: **Source Type** → **Flood Impact Layer (English)**.
#. Bind the same four arguments to the same four variables as in step 4.
#. **Fetch plugin defaults** → the layer arrives as
   **Buildings and roads at risk** with eight rules (polygon and linestring per
   level) and a **Hazard** legend.
#. Save the layer.

The two layers answer different questions from the same thresholds: the hazard
layer classifies *ground*, this one classifies *assets*. Keeping them separate
lets a viewer turn off the ground shading and look only at what is affected.


Step 6 — Finish the map
=======================

#. **Map Extent**: **Use a Custom Extent**, ``-10077781.20,1629865.34,15.13``.
#. **Settings** tab: turn on **Fill Viewport**.
#. Save.

.. important::

   The rasters must be the ``PBI_Actividad_2`` EPSG:3857 copies. If any layer
   points at a ``Guatemala_IBF`` UTM original, the map will auto-fit to that
   raster's projection, jump somewhere far from Guatemala, and the vector layers
   will appear to load and then vanish. This exact bug cost real debugging time
   on this dashboard.


Step 7 — Add the impact summary table
=====================================

#. **Add Dashboard Item** → **Edit**.
#. **Visualization Type** → **Flood Impact Summary (English)**.
#. Bind the same four arguments to the same four variables.
#. **Settings** tab: white background, borders on the left, right and bottom so
   it joins the strip of threshold inputs above it.
#. Save and place it directly below the threshold inputs on the right.


Step 8 — Save and test
======================

Save, leave edit mode, and move a threshold. The hazard shading, the affected
features and the table should all recompute together.

.. figure:: images/ex3-thresholds-in-action.png
   :alt: The dashboard before and after lowering a threshold
   :width: 100%

   **Screenshot:** the same view before and after lowering the High threshold,
   showing the classification expand.


Checkpoint
==========

* A full-window map with seven layers in the layer control.
* Four labelled threshold inputs across the top, each stepping by 0.05.
* Moving any threshold updates the hazard layer, the impact layer and the table.
* Raising the Severe threshold above 0.2 makes purple disappear entirely — and
  it should, for the reason in the warning above.
* Progress messages appear while the layers recompute.


Talking points
==============

* **Four gates on four different questions.** "Severe" means P(≥76 cm) ≥ 0.15
  while "High" means P(≥30 cm) ≥ 0.1. Those are different questions with
  different cutoffs, so the level names are not comparable to each other and
  "severe" carries no meaning on its own. Setting all four gates equal is a good
  demonstration: the levels then differ only by depth, which is far easier to
  explain.
* **An unreachable class is an interface problem.** The Severe gate can be set
  where nothing can qualify, and the interface gives no hint. Ask attendees how
  they would fix it — cap the input at 0.2? show the value range? annotate the
  legend? There is no single right answer, and the discussion is the point.
* **Vectorising a classification.** A map layer can only point at a URL, and
  nothing here serves a computed raster, so the plugin vectorises the classified
  grid into roughly 600 polygons. Adjacent cells of equal class merge, so this is
  exact rather than an approximation. Normal and NoData are dropped — about 90%
  of the grid — because a basemap shows unaffected ground better than a coloured
  layer does.
* **Where the probabilities came from.** These arrived already populated in the
  partners' geopackage with no note on method. Notebook 3 recovers it by testing
  four candidate samplings and lands on ``all_touched`` zonal maximum at about
  98% agreement, with the residual pointing at a real open question about the
  data. Worth raising as a lesson in verifying rather than assuming.


Item positions
==============

The grid is 100 columns wide. Positions are ``x``, ``y`` (top-left) and ``w``,
``h`` (size in grid units). Match approximately; these are for reference, not
transcription.

.. list-table::
   :header-rows: 1
   :widths: 46 14 14 13 13

   * - Item
     - x
     - y
     - w
     - h
   * - Map (**Fill Viewport**)
     - 0
     - 0
     - 99
     - 41
   * - Variable Input — Base Map
     - 0
     - 0
     - 17
     - 6
   * - Variable Input — Low Threshold
     - 56
     - 0
     - 11
     - 7
   * - Variable Input — Medium Threshold
     - 66
     - 0
     - 13
     - 7
   * - Variable Input — High Threshold
     - 78
     - 0
     - 11
     - 7
   * - Variable Input — Severe Threshold
     - 88
     - 0
     - 12
     - 7
   * - Flood Impact Summary (table)
     - 56
     - 7
     - 44
     - 21


Notes on the shipped JSON
=========================

Two small discrepancies you may notice when comparing this guide against
``dashboards/Guatemala_Hands_On_3_English.json``. Neither affects behaviour; both
are recorded so they do not read as mistakes in your own work.

* **The 30 cm probability layer has** ``rampMin`` **of** ``"00"`` **rather than**
  ``"0"``. A typing artifact from the GUI. It parses to zero identically.
* **The threshold inputs store two different defaults.** The active value,
  ``initial_value``, is ``0.8`` on all four. The options metadata also carries an
  ``initialValue`` of 0.3 / 0.2 / 0.1 / 0.15 — the notebook defaults — left over
  from an earlier revision. The dashboard loads at 0.8. If you want the
  notebook's classification on first load, set ``initial_value`` to the values in
  `Understanding the four thresholds`_ instead.
