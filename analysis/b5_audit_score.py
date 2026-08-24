#!/usr/bin/env python3
"""B5 audit scoring — compares the deterministic bridge's verdicts
(cache/b5_audit_key.csv) with the independent blind labels
(cache/b5_audit_labels.csv, produced without access to the key).
Appends the precision report to analysis/B5_RESULTS.md."""
import csv
key={r["pair_id"]:int(r["bridge_match"]) for r in csv.DictReader(open("analysis/cache/b5_audit_key.csv"))}
lab={r["pair_id"]:int(r["llm_match"]) for r in csv.DictReader(open("analysis/cache/b5_audit_labels.csv"))}
ids=[i for i in key if i in lab]
tp=sum(1 for i in ids if key[i]==1 and lab[i]==1)
fp=sum(1 for i in ids if key[i]==1 and lab[i]==0)
fn=sum(1 for i in ids if key[i]==0 and lab[i]==1)
tn=sum(1 for i in ids if key[i]==0 and lab[i]==0)
prec=tp/(tp+fp) if tp+fp else float("nan")
rec=tp/(tp+fn) if tp+fn else float("nan")
agree=(tp+tn)/len(ids)
out=["\n## Audit result (blind labels vs bridge)",
     f"Pairs scored: {len(ids)} (labeler blind to the bridge verdict).",
     f"| | labeler: match | labeler: no match |","|---|--:|--:|",
     f"| bridge: match | {tp} | {fp} |",
     f"| bridge: no match | {fn} | {tn} |",
     f"\n**Bridge precision {prec:.1%} · recall {rec:.1%} · agreement {agree:.1%}** "
     f"(against the blind judgment standard).",
     "Citation rule: the continuation RD and recomposition numbers above may be cited",
     "with this precision attached; a disagreement review pass is the upgrade path."]
open("analysis/B5_RESULTS.md","a").write("\n".join(out)+"\n")
print("\n".join(out))
