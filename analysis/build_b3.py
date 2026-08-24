#!/usr/bin/env python3
"""B3 — chargeable flag on the use-of-proceeds lines (brief: 'chargeable:
water/sewer/utility/power/parking/ports/airports; non-chargeable: schools/parks/
safety/roads/general govt; ambiguous → flag, don't guess').

Classes:
  chargeable      user-fee-financeable enterprise purposes
  non_chargeable  tax-financed purposes (schools/parks/safety/roads/general govt)
  ambiguous       genuinely mixed (transit, higher-ed academic, stormwater, TIF/
                  development, cultural, EMS, …) — flagged, never guessed
  financial       refunding/reserves/COI/pension/… — EXCLUDED from composition
                  per the brief ('excluding refunding uses')
  unclassified    blank functional_activity (69% of lines) — excluded, reported

Outputs:
  analysis/b3_label_map.csv            the reviewable 118-label mapping
  analysis/cache/b3_doc_flags.csv.gz   per-doc aggregates: line counts + $ by class
                                       (use-side, non-subtotal lines only)
  analysis/B3_RESULTS.md               coverage + first composition glance
All numbers from this script."""
import csv, gzip
from collections import Counter, defaultdict

CH="chargeable"; NC="non_chargeable"; AM="ambiguous"; FI="financial"
MAP={
 # --- chargeable: water/sewer/utility/power/parking/ports/airports + enterprise
 "sewer_collection_system":CH,"wastewater_treatment_plant":CH,
 "water_distribution_mains":CH,"potable_water_supply":CH,"water_treatment_plant":CH,
 "recycled_water_system":CH,
 "electric_generation":CH,"electric_transmission_distribution":CH,
 "natural_gas_utility":CH,"district_heating_cooling":CH,"broadband_telecommunications":CH,
 "public_parking_facility":CH,"airport_parking_access":CH,
 "airport_terminal":CH,"airport_runway_airfield":CH,
 "port_infrastructure":CH,"seaport_marine_terminal":CH,"marina_waterfront":CH,
 "solid_waste_landfill":CH,"recycling_waste_facility":CH,
 "golf_course":CH,
 "public_hospital_facility":CH,"long_term_skilled_nursing":CH,
 "student_housing_dormitory":CH,
 "affordable_multifamily_housing":CH,"single_family_homeownership":CH,
 "senior_housing":CH,"public_housing_rehabilitation":CH,
 "sports_stadium_arena":CH,"convention_exhibition_center":CH,
 # --- non-chargeable: schools / parks / safety / roads / general govt
 "k12_capital_improvements_general":NC,"k12_new_school_construction":NC,
 "k12_renovation_modernization":NC,"k12_athletic_facility":NC,"k12_technology_equipment":NC,
 "charter_school_facility":NC,"education_administrative_facility":NC,
 "community_college_facility":NC,
 "parks_open_space":NC,"trails_greenways":NC,"recreation_community_center":NC,
 "aquatic_center_pool":NC,"community_facility_center":NC,
 "fire_station":NC,"fire_apparatus_equipment":NC,"police_station_facility":NC,
 "combined_public_safety_facility":NC,"emergency_communications_911":NC,
 "emergency_operations_center":NC,"public_safety_training_facility":NC,
 "jail_detention_correctional":NC,"juvenile_facility":NC,"courthouse_justice_facility":NC,
 "arterial_local_roads":NC,"street_resurfacing_improvement":NC,"sidewalks_streetscape":NC,
 "bridges_overpasses":NC,"highways_freeways":NC,"traffic_signals_its":NC,"street_lighting":NC,
 "civic_administrative_center":NC,"city_county_hall":NC,"public_works_corporation_yard":NC,
 "information_technology_systems":NC,"general_capital_equipment":NC,
 "vehicles_fleet_equipment":NC,"public_library_facility":NC,"animal_shelter":NC,
 "social_services_office":NC,"senior_services_center":NC,"workforce_job_training":NC,
 "veterans_facility":NC,"public_health_laboratory":NC,
 "flood_control_infrastructure":NC,"seismic_retrofit_hazard_mitigation":NC,
 "homeless_services_facility":NC,
 # --- ambiguous: mixed fee/tax — flagged, not guessed
 "stormwater_drainage":AM,"dam_reservoir":AM,
 "public_transit_bus":AM,"rail_transit_light_heavy":AM,"commuter_passenger_rail":AM,
 "freight_rail":AM,"ferry_marine_transit":AM,"multimodal_transportation_program":AM,
 "higher_ed_academic_building":AM,"higher_ed_research_facility":AM,
 "community_health_clinic":AM,"mental_behavioral_health_facility":AM,
 "medical_equipment":AM,"emergency_medical_ems":AM,
 "performing_arts_theater":AM,"museum_cultural_facility":AM,"zoo_aquarium":AM,
 "development_infrastructure":AM,"tax_increment_project_area":AM,
 "neighborhood_redevelopment":AM,"blight_remediation":AM,
 "commercial_retail_development":AM,"industrial_development":AM,
 "small_business_incubator":AM,"tourism_convention_promotion":AM,
 "supportive_homeless_housing":AM,"childcare_early_learning":AM,"cemetery":AM,
 "lease_asset_acquisition":AM,
 # --- financial: excluded from composition (refunding + non-project uses)
 "costs_of_issuance":FI,"current_refunding":FI,"advance_refunding":FI,
 "reserve_fund_deposit":FI,"capitalized_interest":FI,"accrued_interest_deposit":FI,
 "working_capital_operating":FI,"swap_termination_payment":FI,"pension_obligation":FI,
 "opeb_obligation":FI,"debt_restructuring":FI,"judgment_litigation_settlement":FI,
 "grant_anticipation":FI,
}
with open("analysis/b3_label_map.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["functional_activity","b3_class"])
    for k,v in sorted(MAP.items()): w.writerow([k,v])

lines=Counter(); dollars=Counter()
doc=defaultdict(lambda: Counter())          # doc_id -> class -> [n, $] via two counters
docamt=defaultdict(lambda: Counter())
docmeta={}
unmapped=Counter()
with gzip.open("inputs/corpus/auth_projects.csv.gz","rt") as f:
    for r in csv.DictReader(f):
        if r.get("side")!="use" or r.get("is_subtotal_row")=="True": continue
        fa=(r.get("functional_activity") or "").strip()
        cls=MAP.get(fa, "unclassified" if not fa else None)
        if cls is None: unmapped[fa]+=1; cls=AM   # never guess: unknown labeled -> ambiguous, reported
        lines[cls]+=1
        try: a=float(r.get("amount_usd") or 0)
        except: a=0.0
        if a>0: dollars[cls]+=a
        d=r["doc_id"]
        doc[d][cls]+=1
        if a>0: docamt[d][cls]+=a
        if d not in docmeta:
            docmeta[d]=(r.get("state",""),r.get("year",""),r.get("auth_mode_final2",""),
                        r.get("pol_accountable_unit_id",""),r.get("security_pledge_class",""))
with gzip.open("analysis/cache/b3_doc_flags.csv.gz","wt",newline="") as f:
    w=csv.writer(f)
    w.writerow(["doc_id","state","year","auth_mode_final2","pol_accountable_unit_id","security_pledge_class",
                "n_chargeable","n_non_chargeable","n_ambiguous","n_financial","n_unclassified",
                "amt_chargeable","amt_non_chargeable","amt_ambiguous"])
    for d,c in doc.items():
        m=docmeta[d]; a=docamt[d]
        w.writerow([d,*m,c[CH],c[NC],c[AM],c[FI],c["unclassified"],
                    f"{a[CH]:.0f}",f"{a[NC]:.0f}",f"{a[AM]:.0f}"])

tot=sum(lines.values()); cls_lines=lines[CH]+lines[NC]+lines[AM]
L=["# B3 — chargeable flag (use-side, non-subtotal lines)\n",
   f"Mapping: `b3_label_map.csv` ({len(MAP)} labels: "
   f"{sum(1 for v in MAP.values() if v==CH)} chargeable, {sum(1 for v in MAP.values() if v==NC)} non-chargeable, "
   f"{sum(1 for v in MAP.values() if v==AM)} ambiguous, {sum(1 for v in MAP.values() if v==FI)} financial). "
   f"Unmapped labeled values routed to ambiguous: {sum(unmapped.values())} lines ({dict(unmapped) if unmapped else 'none'}).\n",
   "## Coverage",
   "| class | lines | share | $ (printed amounts) |","|---|--:|--:|--:|"]
for c in (CH,NC,AM,FI,"unclassified"):
    L.append(f"| {c} | {lines[c]:,} | {lines[c]/tot:.1%} | ${dollars[c]/1e9:,.1f}B |")
L.append(f"| **total** | {tot:,} | | |")
L.append(f"\nProject-classified (ch+non+amb) lines: {cls_lines:,}; of those, "
         f"chargeable {lines[CH]/cls_lines:.1%} · non-chargeable {lines[NC]/cls_lines:.1%} · ambiguous {lines[AM]/cls_lines:.1%}.")
d_ch=dollars[CH]; d_nc=dollars[NC]; d_am=dollars[AM]; d_tot=d_ch+d_nc+d_am
L.append(f"By printed dollars: chargeable {d_ch/d_tot:.1%} · non-chargeable {d_nc/d_tot:.1%} · ambiguous {d_am/d_tot:.1%}.")

# first glance: chargeable share by authorization mode (dollar-weighted, ch vs nc only)
by_mode=defaultdict(lambda:[0.0,0.0])
for d,a in docamt.items():
    mode=docmeta[d][2] or "(unknown)"
    by_mode[mode][0]+=a[CH]; by_mode[mode][1]+=a[NC]
L+=["\n## First glance — chargeable share of classified project dollars, by authorization mode",
    "(chargeable/(chargeable+non-chargeable), ambiguous & financial excluded; NATIONAL, all docs)",
    "| auth mode | $ch (B) | $nc (B) | chargeable share |","|---|--:|--:|--:|"]
for m in ("voter","council_or_board","statutory","refunding_no_new_election","unknown","(unknown)"):
    ch,nc=by_mode.get(m,[0,0])
    if ch+nc>0:
        L.append(f"| {m} | {ch/1e9:,.1f} | {nc/1e9:,.1f} | {ch/(ch+nc):.1%} |")
open("analysis/B3_RESULTS.md","w").write("\n".join(L)+"\n")
print("\n".join(L))
