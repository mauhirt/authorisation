# B3 — chargeable flag (use-side, non-subtotal lines)

Mapping: `b3_label_map.csv` (118 labels: 30 chargeable, 46 non-chargeable, 29 ambiguous, 13 financial). Unmapped labeled values routed to ambiguous: 0 lines (none).

## Coverage
| class | lines | share | $ (printed amounts) |
|---|--:|--:|--:|
| chargeable | 93,121 | 4.8% | $1,021.6B |
| non_chargeable | 208,536 | 10.7% | $855.2B |
| ambiguous | 59,820 | 3.1% | $530.9B |
| financial | 489,803 | 25.2% | $3,332.7B |
| unclassified | 1,093,211 | 56.2% | $8,516.3B |
| **total** | 1,944,491 | | |

Project-classified (ch+non+amb) lines: 361,477; of those, chargeable 25.8% · non-chargeable 57.7% · ambiguous 16.5%.
By printed dollars: chargeable 42.4% · non-chargeable 35.5% · ambiguous 22.1%.

## First glance — chargeable share of classified project dollars, by authorization mode
(chargeable/(chargeable+non-chargeable), ambiguous & financial excluded; NATIONAL, all docs)
| auth mode | $ch (B) | $nc (B) | chargeable share |
|---|--:|--:|--:|
| voter | 33.8 | 264.1 | 11.3% |
| council_or_board | 658.6 | 439.9 | 60.0% |
| statutory | 183.8 | 69.7 | 72.5% |
| refunding_no_new_election | 73.5 | 47.4 | 60.8% |
| unknown | 72.0 | 34.0 | 67.9% |
