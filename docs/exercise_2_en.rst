.. Guatemala hands-on exercise 2 solution, English. A Spanish translation lives
.. alongside this file as exercise_2_es.rst.

==============================================================
Exercise 2 — Impact for a single storm
==============================================================

Building **Guatemala Hands On 2 (English)** step by step.

.. admonition:: Start here

   Read `Getting Started <getting_started_en.rst>`_ first. It covers installing
   the plugins, the data bucket, and the motions this guide refers to — creating
   a dashboard, entering edit mode, adding an item.

.. contents:: On this page
   :depth: 2
   :local:
   :backlinks: none


What you are building
=====================

A map on the left showing one storm's flood depth and the buildings and roads it
floods, and on the right a table and a card summarising that storm. A dropdown
selects the storm, and everything re-computes.

.. figure:: images/ex2-finished.png
   :alt: The finished exercise 2 dashboard
   :width: 100%

   **Screenshot:** the finished dashboard, with the storm dropdown, map, summary
   table and card.

New ideas here: reading a slice out of a Zarr store, a vector layer whose
features are produced by a plugin rather than fetched from a URL, and one
variable input driving four separate things at once.

.. tip::

   ``notebooks/02_storm_impact.ipynb`` derives the numbers this dashboard shows
   as plain Python — how depth is sampled onto each building and road, and how
   the summary table is assembled. Worth running first if you want to understand
   the analysis before assembling the interface.


Step 1 — Create the dashboard
=============================

Create a new dashboard (see
`Creating a dashboard <getting_started_en.rst#creating-a-dashboard>`_) with:

* **Name**: ``Guatemala Hands On 2 (English)``
* **Description**: ``Solution for WMO Guatemala Hands On Exercise #2``

Turn on **Unrestricted Grid Item Movement** in **Dashboard Settings**.


Step 2 — Add the storm selector first
=====================================

Build this before anything else. Four other items reference it, and they cannot
be wired up until the variable exists.

#. **Add Dashboard Item** → **Edit** → **Visualization Type**
   **Variable Input**.
#. Fill in:

   .. list-table::
      :header-rows: 1
      :widths: 32 68

      * - Argument
        - Value
      * - ``variable_name``
        - ``Storm``
      * - ``show_label``
        - ticked
      * - ``variable_options_source``
        - ``Flood Maps (English): Storm Impact Summary (English) - Index``
      * - ``initial_value``
        - ``2``

   .. note::

      That options source is not something you type. It is generated from an
      existing plugin argument, in the form
      ``<group>: <plugin label> - <Argument>``. Picking it means "offer the same
      choices the Storm Impact Summary plugin's ``index`` argument offers", so
      the dropdown is populated from the plugin and cannot drift out of sync with
      it. The plugin supplies 198 entries, each labelled with the storm's
      magnitude in millimetres rather than its index, because a magnitude is
      something a forecaster can reason about and an index is not.

#. On the **Settings** tab set **Background Color** ``#ffffff``, and a border on
   the right side only.
#. Save and place it along the top of where the map will go.

.. figure:: images/ex2-storm-input.png
   :alt: The storm selector variable input configuration
   :width: 100%

   **Screenshot:** the **Variable Input** arguments for the storm selector, with
   the plugin-derived options source selected.

Also add a **Base Map** variable input, exactly as in
`Exercise 1, step 5 <exercise_1_en.rst#step-5-add-the-base-map-selector>`_.


Step 3 — Add the map with the Zarr depth layer
==============================================

#. **Add Dashboard Item** → **Edit** → **Visualization Type** **Map**.
#. Tick **Layer Control**. Set **Base Map** to ``${Base Map}``.
#. **Add Layer**:

   * **Layer** tab: **Name** = ``Flood Depth``
   * **Source** tab: **Source Type** = **Zarr**, then:

     .. list-table::
        :header-rows: 1
        :widths: 24 76

        * - Field
          - Value
        * - ``url``
          - ``https://cog-s3-test-401506828094-us-east-1-an.s3.us-east-1.amazonaws.com/floodmaps_test``
        * - ``variable``
          - ``depth``
        * - ``index``
          - ``${Storm}``

   * **Style** tab: **Continuous**, ramp **turbo**, **Min** and **Max** empty.
   * **Legend** tab: **default**.

#. Save the layer.

.. important::

   The ``index`` field is where this exercise becomes interactive. The Zarr store
   holds all 198 storms in one array, and ``index`` selects the slice. Binding it
   to ``${Storm}`` means changing the dropdown re-reads a different slice — no
   duplicated layers, no separate files.

.. figure:: images/ex2-zarr-source.png
   :alt: The Source tab configured for the Zarr store
   :width: 100%

   **Screenshot:** the **Source** tab with **Source Type** Zarr, the store URL,
   ``variable`` depth and ``index`` ``${Storm}``.


Step 4 — Add the plugin-backed impact layer
===========================================

This layer's features are computed per request by a plugin. There is no GeoJSON
URL — the plugin samples depth onto every building and road and returns the
result.

#. **Add Layer** on the same map.
#. Go straight to the **Source** tab and set **Source Type** to
   **Storm Impact Layer (English)**. Dynamic map-layer plugins appear in the same
   **Source Type** dropdown as GeoTIFF and Zarr, listed under their plugin group.
#. The plugin's arguments appear. Set ``index`` to ``${Storm}``.
#. Click **Fetch plugin defaults**.

   .. note::

      This is the step that saves the most work. The plugin's ``run()`` returns a
      ready-made scaffold — the layer name, the source binding, a rule-based
      style keyed on the ``banda`` (depth band) attribute, and a matching legend.
      After fetching you should see the layer named
      **Flooded buildings and roads**, eight style rules, and a four-item
      **Depth** legend, none of which you had to author. Authoring vector style
      rules by hand is error-prone: a rule in the wrong shape silently never
      matches and leaves every feature grey.

#. Check the **Style** and **Legend** tabs to see what arrived. Colours run green
   → yellow → red → purple across four depth bands, with separate rules for
   polygons (buildings) and linestrings (roads) so roads get a stroke wide enough
   to see.
#. Save the layer.

.. figure:: images/ex2-dynamic-layer-source.png
   :alt: The Source tab with a dynamic map-layer plugin selected
   :width: 100%

   **Screenshot:** the **Source** tab with **Storm Impact Layer (English)**
   selected, ``index`` bound to ``${Storm}``, and the **Fetch plugin defaults**
   button.

.. figure:: images/ex2-dynamic-layer-style.png
   :alt: The Style tab showing the fetched rule-based style
   :width: 100%

   **Screenshot:** the **Style** tab after fetching, showing the eight rules on
   the ``banda`` attribute.

Then finish the map:

#. **Map Extent**: **Use a Custom Extent**, ``-10078413.13,1629754.90,14.83``.
#. **Settings** tab: **Background Color** ``#ffffff`` and a border on all four
   sides. This map does *not* fill the viewport — it shares the window with the
   table and card.
#. Save.


Step 5 — Add the summary table
==============================

#. **Add Dashboard Item** → **Edit**.
#. **Visualization Type** → **Storm Impact Summary (English)**.
#. Set ``index`` to ``${Storm}``.
#. Save and place it to the right of the map.

The table breaks the storm's flooded features into depth bands, deepest first,
with counts of buildings, population, area, road length and the share of the
municipality's population affected.


Step 6 — Add the storm card
===========================

#. **Add Dashboard Item** → **Edit**.
#. **Visualization Type** → **Storm Summary (English)**.
#. Set ``index`` to ``${Storm}``.
#. Save and place it below the table.

The card gives the headline figures — the storm, its magnitude, the flooded area
and the population affected — for someone who will not read a table.


Step 7 — Save and test the wiring
=================================

Save the dashboard, leave edit mode, and change the storm dropdown. All four
items should update: the Zarr layer re-reads its slice, the impact layer
re-runs, and the table and card re-fetch.

.. figure:: images/ex2-table-card.png
   :alt: The summary table and storm card
   :width: 100%

   **Screenshot:** the summary table and card for one storm.


Checkpoint
==========

* A storm dropdown labelled with magnitudes in millimetres, not indices.
* Changing it updates the depth raster, the coloured buildings and roads, the
  table and the card — all four.
* The layer control lists **Flood Depth** and **Flooded buildings and roads**.
* The impact layer is coloured by depth band with a **Depth** legend, and roads
  are visible as coloured lines rather than hairlines.


Talking points
==============

* **One variable, four consumers.** ``${Storm}`` appears in a Zarr source index,
  a plugin layer argument, and two visualization arguments. Nothing in the four
  items knows about the others; they all just declare a dependency on a name.
* **Dynamic layers re-run; static layers re-fetch.** The Zarr layer re-reads a
  slice of an existing array. The impact layer re-executes Python that samples a
  raster onto 5,000-odd geometries. Same trigger, very different cost — which is
  why the plugin reports progress while it works.
* **Labels versus values.** The dropdown shows magnitude, the plugin receives an
  index. Presenting a meaningful label over an opaque key is nearly always worth
  the indirection.
* **The magnitudes are placeholders.** They are illustrative, not measured. They
  are unique and monotonic, so they identify a storm reliably and sort sensibly,
  but do not present them as physical rainfall totals.
* **Why the plugin ships a style.** The alternative — hand-authoring eight rules
  in the GUI — fails silently when a rule is malformed. Shipping the style from
  ``run()`` means the layer is correct the first time and stays correct if the
  bands change.


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
   * - Map
     - 0
     - 0
     - 55
     - 38
   * - Variable Input — Base Map
     - 0
     - 0
     - 15
     - 6
   * - Variable Input — Storm
     - 43
     - 0
     - 12
     - 6
   * - Storm Impact Summary (table)
     - 55
     - 2
     - 45
     - 26
   * - Storm Summary (card)
     - 55
     - 25
     - 45
     - 12


Next
====

`Exercise 3 — Hazard classification with adjustable thresholds <exercise_3_en.rst>`_
turns the thresholds themselves over to the viewer.
