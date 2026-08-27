#!/usr/bin/env python3
"""Consolidate the reframed working-paper draft in place on paper/overleaf/main.tex.

Operations (all on the repo's manuscript of record):
  1. Replace old section 2 ("The Argument") with the authoritative section 2
     (The Institution) and section 3 (Framework: A Constraint with Exit), and
     preserve the old section's operation/persistence/stakes prose as a new
     section 4 ("The requirement in operation"). Drop the "Four hypotheses"
     subsection (superseded by P1-P3); its H3 electorate readings move to the
     new exploratory Electorates section.
  2. Foreground the +11.5 out-of-design agreement in the close-elections
     section ("two independent designs, one answer"); leave a back-reference in
     the agenda section.
  3. Split "Where the requirement binds: exits and electorates" into the exit
     fork (Stage III, P2) and a separate, explicitly exploratory "Electorates
     and the cost of consent" section (C_V(theta,e_i)).
  4. Compress the origins section to a shorter institutional background,
     keeping every citation and the genealogy table.
  5. Add a Conclusion with the three-point contribution and the who-pays close.
  6. Add \\label to every section and convert hardcoded "Section N"/"Section N.M"
     cross-references to \\ref, so numbering stays correct after reordering.

Idempotent-ish: run once against the committed main.tex. Not a general tool.
"""
import re, sys

P = "paper/overleaf/main.tex"
t = open(P).read()
orig = t

def must(cond, msg):
    if not cond:
        sys.exit("ASSEMBLE FAILED: " + msg)

# ---------------------------------------------------------------- load new 2,3
sec2 = open("paper/sections/section2_institution.tex").read().rstrip() + "\n"
sec3 = open("paper/sections/section3_framework_clean.tex").read().rstrip() + "\n"
# label the new sections
sec2 = sec2.replace("\\section{The Institution: Scope, Height, and Exit}",
                    "\\section{The Institution: Scope, Height, and Exit}\\label{sec:institution}", 1)
sec3 = sec3.replace("\\section{Framework: A Constraint with Exit}",
                    "\\section{Framework: A Constraint with Exit}\\label{sec:framework}", 1)

# --------------------------------------------- extract old section 2 remnants
A = "\\section{The Argument: Consent as a Sorting Institution}"
B = "\\section{Where the Rules Came From}"
must(A in t and B in t, "old section 2 / origins markers not found")
old2 = t[t.index(A):t.index(B)]

def between(block, start, end):
    i = block.index(start) + len(start)
    j = block.index(end, i)
    return block[i:j].strip("\n")

op = between(old2, "\\subsection{The institution in operation}", "\\subsection{Four hypotheses}")
persist = between(old2, "\\subsection{Why the rules persist}", "\\subsection{The stakes}")
stakes = old2[old2.index("\\subsection{The stakes}") + len("\\subsection{The stakes}"):].strip("\n")

sec4 = (
    "\\section{The requirement in operation}\\label{sec:operation}\n"
    + op + "\n\n"
    + "\\subsection{Why the rules persist}\\label{subsec:persist}\n"
    + persist + "\n\n"
    + "\\subsection{Stakes and the scope of the claims}\n"
    + stakes + "\n"
)

# --------------------------------------------------- replace old 2 with 2+3+4
t = t.replace(old2, sec2 + "\n" + sec3 + "\n" + sec4 + "\n", 1)

# ------------------------------------------------------- label remaining secs
labels = {
    "\\section{Introduction}": "sec:intro",
    "\\section{Where the Rules Came From}": "sec:origins",
    "\\section{Data: seeing consent from statute to bond}": "sec:data",
    "\\section{Who must agree, and for what}": "sec:menu",
    "\\section{What authorisation causes: evidence from close elections}": "sec:rd",
    "\\section{What happens when a measure fails}": "sec:fail",
    "\\section{The agenda margin and the politics of the rule}": "sec:agenda",
}
for head, lab in labels.items():
    must(head in t, "section head missing: " + head)
    t = t.replace(head, head + "\\label{" + lab + "}", 1)

# subsection label for "Does the written rule govern behaviour?" (ref'd as 5.4)
t = t.replace("\\subsection{Does the written rule govern behaviour?}",
              "\\subsection{Does the written rule govern behaviour?}\\label{subsec:govern}", 1)

# --------------------------------------------- foreground +11.5 in RD section
rd_anchor = "the same doubling appears in Census survey data, which capture the bank loans and private placements no official statement records."
must(rd_anchor in t, "RD +11.5 anchor sentence missing")
foreground = (rd_anchor + "\n\n"
    "\\textbf{Two independent designs, one answer.} A second comparison, built from an "
    "entirely different source of variation, lands on the same number. In the band of vote "
    "shares between fifty and fifty-five per cent, an identical election result authorises a "
    "Texan or Wisconsin district and refuses a Californian one, because the statutory bar "
    "differs and nothing else does. Comparing later issuance across that band estimates the "
    "rule's effect at fixed voter support at $+11.5$ points (SE 4.8), statistically "
    "indistinguishable from the threshold estimate obtained from near-winners against "
    "near-losers. The two designs share no measures, no states on the same side of the line, "
    "and no identifying assumption, yet they agree to within a point. This out-of-design "
    "agreement is the strongest single check in the paper (the cross-regime comparison is "
    "developed in Section~\\ref{sec:agenda}).")
t = t.replace(rd_anchor, foreground, 1)

# soften the now-duplicated +11.5 paragraph in the agenda section
agenda_dup = ("\\textbf{At fixed voter support, the rule alone moves outcomes.} In the band between 50\\% "
    "and 55\\%, the identical election result authorises a Texan or Wisconsin district and refuses a "
    "Californian one. Comparing issuance across that band yields an estimate of the rule's effect at "
    "fixed support, +11.5 points (SE 4.8), indistinguishable from the RD estimate obtained from an "
    "entirely different comparison. This out-of-design agreement is the strongest single check in the paper.")
agenda_new = ("\\textbf{At fixed voter support, the rule alone moves outcomes.} The cross-regime comparison "
    "in the band between 50\\% and 55\\%, where the identical election result authorises a Texan or "
    "Wisconsin district and refuses a Californian one, is the out-of-design check foregrounded in "
    "Section~\\ref{sec:rd}: the rule's effect at fixed support, $+11.5$ points (SE 4.8), is "
    "indistinguishable from the threshold estimate obtained from a wholly separate comparison.")
must(agenda_dup in t, "agenda +11.5 paragraph not matched verbatim")
t = t.replace(agenda_dup, agenda_new, 1)

# --------------------------------------------------- split fork / electorates
fork_head = "\\section{Where the requirement binds: exits and electorates}"
fork_intro = ("Everything above averages over the frame. The theory says the average is the wrong "
    "object: the effect should live where the menu is empty and die where it is rich, and it should "
    "depend on who the convened electorate is. Both predictions hold, and they are the paper's core "
    "results as much as the average is.")
must(fork_head in t, "fork section head missing")
# new fork header + reframed intro (exits only, P2)
t = t.replace(fork_head, "\\section{Where the requirement binds: the exit fork}\\label{sec:fork}", 1)
t = t.replace(fork_intro,
    "Everything above averages over the frame. The framework says the average is the wrong object. "
    "The causal effect should live where the exit menu is empty and fall to nothing where it is rich. "
    "This is prediction P2, and it is tested by stratifying the close-election design on the "
    "predetermined exit available to each type of government, the school-versus-general-purpose fork "
    "foremost. The estimates form a schedule $\\{\\tau_k\\}$ across groups that are not randomly "
    "assigned; the ordering across strata characterises where consent binds, and is read for that "
    "ordering rather than as an identified causal effect of exit itself.", 1)

# insert the Electorates section header + framing just before the electorate paragraph
elec_para = ("\\textbf{By electorate: the stable propertied public.}")
must(elec_para in t, "electorate paragraph missing")
elec_header = (
    "\\section{Electorates and the cost of consent}\\label{sec:electorates}\n"
    "The exit menu governs where the requirement binds through the outside option. A second and "
    "distinct channel runs through the electorate the voted route convenes, the cost of consent "
    "$C_V(\\theta_s,e_i)$: the same rule can be easier or harder to satisfy depending on who is "
    "convened to grant it. This section is exploratory. The pattern was read after the fact, it "
    "identifies no exit stratum, and nothing else in the paper rests on it; the two channels are kept "
    "separate because they enter the response at different points, the outside option through the "
    "exempt channel and the electorate through the price of the voted one.\n\n"
    "Two established readings of the electorate disagree in a way the split can weigh. On an "
    "assembly-cost reading, consent should be hardest where communities are divided, since social "
    "heterogeneity raises the price of every coalition (Alesina, Baqir and Easterly 1999; Alesina, "
    "Glaeser and Sacerdote 2001). On a transmission reading, a vote binds only where the electorate is "
    "durable enough that today's answer is also tomorrow's, so the requirement should matter most "
    "where the convened public is stable, propertied and homogeneous (Fischel 2001; Oliver 2001). The "
    "two disagree on the sign of social heterogeneity, which is what makes the split informative, and "
    "neither originates with this paper.\n\n")
t = t.replace(elec_para, elec_header + elec_para, 1)

# ---------------------------------------------------------- convert Section N
# map (verbatim string) -> replacement, applied globally
refmap = [
    ("developed inside the argument (Section 2)", "developed in Section~\\ref{sec:operation}"),
    ("The claim that organises Sections 6 and 7", "The claim that organises Sections~\\ref{sec:rd} and~\\ref{sec:fail}"),
    ("and Section 9 reads the modern record", "and Section~\\ref{sec:agenda} reads the modern record"),
    ("Section 8 identifies the minority", "Section~\\ref{sec:electorates} identifies the minority"),
    ("the landscape and the channel (Section 5), the vote's effect at the threshold (Section 6), the response to refusal (Section 7), the adjudication between the two readings of H3 (Section 8), and the shaping of agendas and of the rules themselves (Section 9).",
     "the landscape and the channel (Section~\\ref{sec:menu}), the vote's effect at the threshold (Section~\\ref{sec:rd}), the response to refusal (Section~\\ref{sec:fail}), where the requirement binds and for whom (Sections~\\ref{sec:fork} and~\\ref{sec:electorates}), and the shaping of agendas and of the rules themselves (Section~\\ref{sec:agenda})."),
    ("the persistence mechanism of Section 2.4", "the persistence mechanism of Section~\\ref{subsec:persist}"),
    ("how borrowing is actually authorised, and by whom (Section 5); what winning or losing that vote causes (Section 6); and what happens after a refusal (Section 7). Sections 8 and 9 ask where the requirement bites hardest and how it shapes what is proposed in the first place.",
     "how borrowing is actually authorised, and by whom (Section~\\ref{sec:menu}); what winning or losing that vote causes (Section~\\ref{sec:rd}); and what happens after a refusal (Section~\\ref{sec:fail}). Sections~\\ref{sec:fork} to~\\ref{sec:electorates} ask where the requirement bites hardest and for whom, and Section~\\ref{sec:agenda} asks how it shapes what is proposed in the first place."),
    ("The causal design of Section 6 uses the subset", "The causal design of Section~\\ref{sec:rd} uses the subset"),
    ("a point Section 5.4 returns to", "a point Section~\\ref{subsec:govern} returns to"),
    ("(Section 8 confirms exactly this ordering)", "(Section~\\ref{sec:fork} confirms exactly this ordering)"),
    ("political fights over the rule should concentrate on the menu-poor class (Section 9 shows they do)",
     "political fights over the rule should concentrate on the menu-poor class (Section~\\ref{sec:agenda} shows they do)"),
    ("candidate moderators of the authorisation effect, which Section 8 tests",
     "candidate moderators of the authorisation effect, which Section~\\ref{sec:electorates} tests"),
    ("an agenda power taken up in Section 9", "an agenda power taken up in Section~\\ref{sec:agenda}"),
    ("Section 8 splits every result by type", "Section~\\ref{sec:fork} splits every result by type"),
    ("that is itself evidence for the agenda story of Section 9", "that is itself evidence for the agenda story of Section~\\ref{sec:agenda}"),
    ("catch up through re-votes, which Section 7 shows", "catch up through re-votes, which Section~\\ref{sec:fail} shows"),
    ("the pay-go bound of Section 6 closes", "the pay-go bound of Section~\\ref{sec:rd} closes"),
    ("against each class's national menu from Section 5", "against each class's national menu from Section~\\ref{sec:menu}"),
    ("and the excess of near-winners at the cutoff (Section 6) is the same behaviour seen from below",
     "and the excess of near-winners at the cutoff (Section~\\ref{sec:rd}) is the same behaviour seen from below"),
    ("the causal weight of the paper rests on the within-state designs of Section 6",
     "the causal weight of the paper rests on the within-state designs of Section~\\ref{sec:rd}"),
]
for a, b in refmap:
    must(a in t, "refmap string not found: " + a[:48])
    t = t.replace(a, b, 1)

# the two-line roadmap in old stakes still mentions "Section 8" for the H3 adjudication:
t = t.replace("the adjudication between the two readings of H3 (Section~\\ref{sec:electorates})",
              "the adjudication between the two readings of the electorate (Section~\\ref{sec:electorates})", 1)

# ------------------------------------------------- compress the origins section
# Replace the three long thematic paragraphs with tighter versions (all
# citations retained). Matched verbatim against the committed text.
orig_p1 = ("Written by nameable coalitions. These rules do not have anonymous origins. Florida's "
    "constitution once stated who the consenting public was in so many words: freeholders, property "
    "owners, the only electors permitted to vote on bonds [V: article and date]. California's "
    "two-thirds requirement and debt limit entered together in the 1879 constitution, the work of a "
    "convention dominated by taxpayer and anti-corporate coalitions; Kentucky's tax-rate limits and "
    "voter-assent requirement are Sections 157 and 158 of the 1891 constitution, a taxpayer "
    "convention's settlement. The wave itself was a response to identifiable events: eleven states "
    "replaced their constitutions between 1842 and 1852 after the state debt crisis, rewriting debt "
    "procedure and corporate chartering together (Wallis 2005), and the municipal defaults after 1873 "
    "pushed the same settlement one tier down (Dove 2014; Hillhouse 1936). The referendum itself "
    "entered this history as a promoter's tool before it became a taxpayer's shield: mid-century "
    "county votes were the instrument by which communities granted railroad aid, and when the aid "
    "soured, the federal courts forced payment over state objection (Gelpcke v. Dubuque 1863) and the "
    "constitutional response converted the enabling device into a barrier (Cole 2023 [V]). In several "
    "Southern states the authoring conventions' disenfranchising purposes were explicit, and the "
    "fiscal articles carried them [V: Kousser; Alabama 1901]. The coalitions, in short, are in the "
    "record: taxpayers, creditors made cautious, and property holders whose names some texts preserved.")
new_p1 = ("Written by nameable coalitions. These rules do not have anonymous origins. California's "
    "two-thirds requirement and debt limit entered together in the taxpayer and anti-corporate "
    "convention of 1879; Kentucky's voter-assent requirement is Sections 157 and 158 of its 1891 "
    "taxpayer constitution; Florida's text once named the consenting public outright, the freeholders "
    "who alone could vote on bonds [V: article and date]. The wave answered identifiable events: "
    "eleven states rewrote their constitutions between 1842 and 1852 after the state debt crisis, "
    "recasting debt procedure and corporate chartering together (Wallis 2005), and the municipal "
    "defaults after 1873 carried the settlement one tier down (Dove 2014; Hillhouse 1936). The "
    "referendum was a promoter's tool before it was a taxpayer's shield: county votes granted "
    "railroad aid, and when the aid soured and the federal courts forced payment over state objection "
    "(Gelpcke v. Dubuque 1863), the constitutional response turned the enabling device into a barrier "
    "(Cole 2023 [V]). In several Southern states the authoring conventions' disenfranchising purposes "
    "were explicit, and the fiscal articles carried them [V: Kousser; Alabama 1901].")
must(orig_p1 in t, "origins p1 not matched")
t = t.replace(orig_p1, new_p1, 1)

orig_p3 = ("Leaking from birth. The exits are not modern corrosion; they are nearly as old as the gates. "
    "Within decades of the 1879 settlement, California courts had constructed the special fund "
    "doctrine, under which obligations payable solely from project revenues are not ``debt'' within "
    "the constitutional meaning, and the lease exceptions followed [V: Offner-Dean line]. Florida's "
    "first judicial exit opened within a few years of the freeholder clause itself [V: State v. City "
    "of Miami]. By 1958 a signed Yale Law Journal article could describe public building authorities, "
    "matter-of-factly, as ``the costly subversion of state constitutions'' (Morris 1958). Legislatures "
    "wrote the leak into the statutes directly: Iowa's code authorises ``essential corporate purpose'' "
    "borrowing with no election while requiring sixty per cent approval for ``general corporate "
    "purposes,'' the scope line drawn in purpose language inside a single chapter (Iowa Code "
    "\\S\\S384.24 to 384.26). Kentucky ran the whole sequence in one state: the 1891 gates, a century "
    "of doctrinal exits through holding companies and revenue devices, formal amendment ratifying what "
    "practice had built, and a measurable endpoint, for in the modern corpus Kentucky's voters "
    "authorise essentially none of the state's local borrowing, the lowest value on the consent map "
    "(Figure~\\ref{fig:map}). The oldest strong gate and the emptiest modern ballot are the same case. "
    "That is this section's thesis in one state, and it is why the persistence mechanism of "
    "Section~\\ref{subsec:persist} is historical before it is contemporary: the rules never "
    "accumulated the reform pressure that would have moved them, because from nearly the beginning, "
    "everyone who could leave, left.")
new_p3 = ("Leaking from birth. The exits are nearly as old as the gates. Within decades of the 1879 "
    "settlement, California courts had built the special fund doctrine, under which obligations "
    "payable solely from project revenues are not ``debt'' in the constitutional sense, and the lease "
    "exceptions followed [V: Offner-Dean line]; Florida's first judicial exit opened within a few "
    "years of the freeholder clause [V: State v. City of Miami]. By 1958 a signed Yale Law Journal "
    "article could call public building authorities ``the costly subversion of state constitutions'' "
    "(Morris 1958). Legislatures wrote the leak into statute directly: Iowa authorises ``essential "
    "corporate purpose'' borrowing with no election while requiring sixty per cent approval for "
    "``general corporate purposes,'' the scope line drawn in purpose language inside a single chapter "
    "(Iowa Code \\S\\S384.24 to 384.26). Kentucky ran the whole sequence in one state: the 1891 gates, "
    "a century of doctrinal exits, formal amendment ratifying what practice had built, and a "
    "measurable endpoint, for in the modern corpus its voters authorise essentially none of the "
    "state's local borrowing, the lowest value on the consent map (Figure~\\ref{fig:map}). The oldest "
    "strong gate and the emptiest modern ballot are the same case, which is why the persistence "
    "mechanism of Section~\\ref{subsec:persist} is historical before it is contemporary: the rules "
    "never accumulated the reform pressure that would have moved them, because from nearly the "
    "beginning, everyone who could leave, left.")
must(orig_p3 in t, "origins p3 not matched")
t = t.replace(orig_p3, new_p3, 1)

# ------------------------------------------------------------- add Conclusion
concl = (
    "\\section{Conclusion}\\label{sec:conclusion}\n"
    "The oldest fiscal referendum in American law turns out to protect far less than it sorts. "
    "Read across every state and every type of local government, the requirement to obtain voter "
    "consent for debt does not decide whether the local state borrows. It decides which borrowing "
    "must gather consent, through which instrument, on what timetable, and at whose expense. Its "
    "incidence is uneven in a way its scope and height alone cannot predict, because two governments "
    "facing the identical rule confront it across entirely different choice sets.\n\n"
    "Three claims follow, and the paper is organised to establish each. First, a formal constraint "
    "operates over a choice set, so its incidence cannot be read from its stringency alone: the same "
    "century-old provision is a gate for a school district and a formality for a city, and the "
    "difference is the outside option, not the text. Second, that outside option is a match between "
    "economics and institutions, the chargeability of a good and the legal menu of exempt forms open "
    "to the government that provides it, so a formally neutral rule acquires a structured and "
    "predictable incidence: it binds on the unchargeable core of the local state and falls slack on "
    "everything that can bill its users. Third, the design observes the behavioural response function "
    "and not merely whether the constrained act occurs: the requirement's work is visible before any "
    "vote, in the channel chosen and the ballot shaped, and after any refusal, in the queue of "
    "re-submissions, so that a refused measure is far more often delayed and re-routed than denied.\n\n"
    "The distributive stakes are the other half of the finding. The requirement sorts who is governed "
    "and, by the same act, who pays. The consenting public is the electorate whose approval the law "
    "requires, convened on terms that skew old and propertied; the paying public is the one the rule "
    "creates by leaving it out, the ratepayers, tenants and users who service the exempt forms of "
    "debt and hold a vote over none of it. The freeholder franchise struck from the general ballot "
    "survives, lawfully, in the exit. A requirement written to let a community refuse the debt it "
    "would have to repay now works mainly to decide which debts its voters ever see, and which are "
    "carried, unseen and unvoted, by whoever cannot leave its jurisdiction.\n\n")
# insert immediately before the References section
must("\\section*{References}" in t, "References marker missing")
t = t.replace("\\section*{References}", concl + "\\section*{References}", 1)

open(P, "w").write(t)
print("assembled OK; length %d -> %d chars" % (len(orig), len(t)))
