# Rev E startup simulator implementation plan

Goal: reproduce the Rev E startup margin and exercise PACK-based fault recovery.

- Encode the BQ298217 POR and discharge-fault recovery comparisons using integer millivolts.
- Represent charger output and path drop as editable assumptions. Represent each transition as an event without a timing claim.
- Deliver a standalone browser page with scenario presets, manual events, and an event trace.
- Verify the 30 mV full-cell case, the strict 700 mV boundary, the UV inhibit, isolated wake and a persistent-fault restart.
