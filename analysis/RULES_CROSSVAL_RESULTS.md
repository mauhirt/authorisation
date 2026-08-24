# Rules cross-validation — our panel vs independent green-bond-paper coding

Municipal GO debt, 2024 cells; theirs = state_bond_referenda_requirements.csv
(50 states, sourced to Ballotpedia/state law), ours = PRELIMINARY AI pass-1.

**Agreement on 'voter approval required': 29/37 codable-both states (78%); 13 not-codable in ours (conditional/home-rule cells).**

| state | status | theirs: required | ours: strict |
|---|---|---|---|
| CT | NOT CODABLE (ours) | False |  |
| DE | NOT CODABLE (ours) | True |  |
| HI | NOT CODABLE (ours) | False |  |
| IA | NOT CODABLE (ours) | True |  |
| IL | NOT CODABLE (ours) | True |  |
| IN | NOT CODABLE (ours) | True |  |
| KS | NOT CODABLE (ours) | True |  |
| KY | DISAGREE | True | False |
| MA | DISAGREE | True | False |
| MD | NOT CODABLE (ours) | True |  |
| ME | DISAGREE | True | False |
| MN | NOT CODABLE (ours) | True |  |
| MS | DISAGREE | True | False |
| NH | DISAGREE | True | False |
| NV | NOT CODABLE (ours) | True |  |
| NY | NOT CODABLE (ours) | True |  |
| PA | NOT CODABLE (ours) | True |  |
| RI | NOT CODABLE (ours) | True |  |
| TN | DISAGREE | True | False |
| VA | DISAGREE | True | False |
| WI | DISAGREE | True | False |

Disagreements + not-codables above are the priority worklist for the human
pass-2 (two independent codings disagreeing = a genuinely hard cell).
