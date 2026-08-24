# B3 — chargeable flag (use-side, non-subtotal lines)

Mapping: `b3_label_map.csv` (118 labels: 30 chargeable, 46 non-chargeable, 29 ambiguous, 13 financial). Unmapped labeled values routed to ambiguous: 0 lines (none).

## Coverage
| class | lines | share | $ (printed amounts) |
|---|--:|--:|--:|
| chargeable | 89,756 | 4.6% | $1,010.1B |
| non_chargeable | 196,364 | 10.1% | $832.8B |
| ambiguous | 58,565 | 3.0% | $520.5B |
| financial | 481,741 | 24.8% | $3,308.9B |
| unclassified | 1,118,065 | 57.5% | $8,584.6B |
| **total** | 1,944,491 | | |

Project-classified (ch+non+amb) lines: 344,685; of those, chargeable 26.0% · non-chargeable 57.0% · ambiguous 17.0%.
By printed dollars: chargeable 42.7% · non-chargeable 35.2% · ambiguous 22.0%.

## First glance — chargeable share of classified project dollars, by authorization mode
(chargeable/(chargeable+non-chargeable), ambiguous & financial excluded; NATIONAL, all docs)
| auth mode | $ch (B) | $nc (B) | chargeable share |
|---|--:|--:|--:|
| voter | 32.4 | 258.9 | 11.1% |
| council_or_board | 648.9 | 423.5 | 60.5% |
| statutory | 183.5 | 69.4 | 72.5% |
| refunding_no_new_election | 58.4 | 42.0 | 58.2% |
| unknown | 86.8 | 39.0 | 69.0% |

## Interpretation & caveats
1. **The sorting the theory predicts is visible on first contact:** the voted
   channel carries **11.1%** chargeable dollars — the unvoted channels carry
   **60.5%** (council) and **72.5%** (statutory). Chargeable purposes exit to
   channels where no coalition must be assembled; the consenting public is asked
   almost exclusively about non-chargeable goods (schools, safety, roads, parks).
   This table is descriptive sorting (selection + treatment); C2 turns it into
   the H2 test by putting rule *stringency* on the right-hand side with place and
   entity-type fixed effects.
2. Mapping discipline: all 118 labels mapped explicitly (30 ch / 46 nc / 29
   ambiguous / 13 financial), zero unmapped, ambiguous never guessed. Judgment
   calls the theory session may want to review in `b3_label_map.csv`: hospitals,
   housing (mortgage/rent-backed → chargeable), stadium/convention (chargeable),
   golf (chargeable) vs pools/rec centers (parks → non); transit, higher-ed
   academic, stormwater, TIF/development → ambiguous.
3. Coverage honesty: 57.5% of use-side lines carry no functional label
   (unclassified, excluded) and only ~a third of lines print dollars — shares are
   over classified, printed-amount lines. `financial` ($3.3T, refunding-dominated)
   is excluded from composition per the brief.
