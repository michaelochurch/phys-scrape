# Referee agent — the two reruns, and a disclosure

Agents 7 and 9 crashed on the 64k output-token ceiling: both generated
commentary until they ran out of room, without reaching a conclusion. They
were relaunched at 21:26:54 and 21:30:33 UTC with modified prompts.

## Disclosure: the reruns carried a hint

The relaunches were meant to add only a length cap. They also each added a
clause to the "check the algebra" paragraph — and **each clause names the
class of the paper's own gold error.**

| Paper | Gold error | Clause added to the rerun prompt |
|---:|---|---|
| 7 | `m\|φ\|²` should be `m²\|φ\|²` in Eq. (1) — a **dimensional** slip | "...and to whether the quoted symbols have the **dimensions** they should" |
| 9 | "should the 2 be replaced by N?" in Eq. 5.23 — a **coefficient** that must track the construction | "...and to whether **coefficients** and index ranges match what the surrounding construction requires" |

That is a steer toward the answer. Paper 7 timed out again, so it cost
nothing there. **Paper 9 scored MATCH under the hinted prompt**, and that
MATCH cannot be credited to an unaided model.

### Effect on the headline

| | Reported | Clean |
|---|---|---|
| Scored papers | 11 | 10 (paper 9 also set aside) |
| MATCH | 6 | **5** |
| PARTIAL | 1 | 1 |
| MISS | 4 | 4 |

So: **5 of 10 under the identical unhinted prompt**, not 6 of 11. The
qualitative finding is unchanged — errors with no convention defence went 5
match + 1 partial of 6, errors defensible as convention or intent went 0 of 4
— and paper 9 belonged to the no-defence group either way. The difficulty-band
breakdown was already too thin to carry weight and is now thinner: level 3
has one cleanly-scored paper left.

### How this got missed

The earlier disclosure said the reruns used "a non-identical prompt with a
1,200-word report cap", which was true and incomplete. The cap was the change
being tracked; the clause was added in the same edit and did not get named.
Diffing the two prompts against the canonical one is what surfaced it, which
is the argument for keeping this directory.

## Paper 7 rerun — diff against the canonical prompt

```diff
--- referee-agent.md (papers 1-12)
+++ this variant
@@ -2,3 +2,3 @@
 
-Read the manuscript at /tmp/eval_run/e662293c21/manuscript.tex . It is LaTeX source.
+Read the manuscript at /tmp/eval_run/633439e8dc/manuscript.tex . It is LaTeX source.
 
@@ -11,8 +11,10 @@
 
-Check the algebra yourself where you can. Re-derive intermediate steps rather than trusting the text. Pay attention to whether each equation is consistent with the ones it is derived from.
+Check the algebra yourself where you can. Re-derive intermediate steps rather than trusting the text. Pay attention to whether each equation is consistent with the ones it is derived from, and to whether the quoted symbols have the dimensions they should.
 
-For each error you find, report:
+IMPORTANT, on length: your final report must be under 1200 words. Do all the checking you need, but report only conclusions, not your working. Do not reproduce long derivations or list every equation you verified. Think privately; write briefly.
+
+For each error you find, report compactly:
 - the equation number as printed in the manuscript, or the nearest numbered equation plus where the problem sits relative to it
-- a quote of the offending expression
-- what is wrong, stated precisely
+- a short quote of the offending expression
+- what is wrong, in one or two sentences
 - what it should be instead, if you can determine that
```

## Paper 9 rerun — diff against the canonical prompt

```diff
--- referee-agent.md (papers 1-12)
+++ this variant
@@ -2,3 +2,3 @@
 
-Read the manuscript at /tmp/eval_run/e662293c21/manuscript.tex . It is LaTeX source.
+Read the manuscript at /tmp/eval_run/62ac0ca949/manuscript.tex . It is LaTeX source. It is long; read it in sections if you need to.
 
@@ -11,8 +11,10 @@
 
-Check the algebra yourself where you can. Re-derive intermediate steps rather than trusting the text. Pay attention to whether each equation is consistent with the ones it is derived from.
+Check the algebra yourself where you can. Re-derive intermediate steps rather than trusting the text. Pay attention to whether each equation is consistent with the ones it is derived from, and to whether coefficients and index ranges match what the surrounding construction requires.
 
-For each error you find, report:
+IMPORTANT, on length: your final report must be under 1200 words. Do all the checking you need, but report only conclusions, not your working. Do not reproduce long derivations or list every equation you verified. Think privately; write briefly.
+
+For each error you find, report compactly:
 - the equation number as printed in the manuscript, or the nearest numbered equation plus where the problem sits relative to it
-- a quote of the offending expression
-- what is wrong, stated precisely
+- a short quote of the offending expression
+- what is wrong, in one or two sentences
 - what it should be instead, if you can determine that
```

## Full text, paper 7 rerun

```text
You are a careful referee for a theoretical physics journal.

Read the manuscript at /tmp/eval_run/633439e8dc/manuscript.tex . It is LaTeX source.

Constraints, and these matter:
- Read that one file and nothing else. Do not read any other file on this machine and do not explore the filesystem.
- Do not use web search and do not fetch any URL.
- Work only from the manuscript's own content and your own physics knowledge.

Your task: find substantive errors in the physics or the mathematics. A substantive error is a wrong equation, a wrong sign, a missing or spurious factor, an invalid algebraic step, a dimensional inconsistency, a claim that contradicts another part of the same paper, or a derivation that does not follow from what precedes it. Typography, grammar, notation preferences, missing citations, and requests for more explanation are NOT errors: do not report them.

Check the algebra yourself where you can. Re-derive intermediate steps rather than trusting the text. Pay attention to whether each equation is consistent with the ones it is derived from, and to whether the quoted symbols have the dimensions they should.

IMPORTANT, on length: your final report must be under 1200 words. Do all the checking you need, but report only conclusions, not your working. Do not reproduce long derivations or list every equation you verified. Think privately; write briefly.

For each error you find, report compactly:
- the equation number as printed in the manuscript, or the nearest numbered equation plus where the problem sits relative to it
- a short quote of the offending expression
- what is wrong, in one or two sentences
- what it should be instead, if you can determine that
- your confidence: high, medium, or low

Report only what you can argue for. If you find nothing you can defend, say so plainly: that is an acceptable answer. Do not pad the list with weak observations.

End with a one-line summary naming the equation numbers you are most confident about.
```

## Full text, paper 9 rerun

```text
You are a careful referee for a theoretical physics journal.

Read the manuscript at /tmp/eval_run/62ac0ca949/manuscript.tex . It is LaTeX source. It is long; read it in sections if you need to.

Constraints, and these matter:
- Read that one file and nothing else. Do not read any other file on this machine and do not explore the filesystem.
- Do not use web search and do not fetch any URL.
- Work only from the manuscript's own content and your own physics knowledge.

Your task: find substantive errors in the physics or the mathematics. A substantive error is a wrong equation, a wrong sign, a missing or spurious factor, an invalid algebraic step, a dimensional inconsistency, a claim that contradicts another part of the same paper, or a derivation that does not follow from what precedes it. Typography, grammar, notation preferences, missing citations, and requests for more explanation are NOT errors: do not report them.

Check the algebra yourself where you can. Re-derive intermediate steps rather than trusting the text. Pay attention to whether each equation is consistent with the ones it is derived from, and to whether coefficients and index ranges match what the surrounding construction requires.

IMPORTANT, on length: your final report must be under 1200 words. Do all the checking you need, but report only conclusions, not your working. Do not reproduce long derivations or list every equation you verified. Think privately; write briefly.

For each error you find, report compactly:
- the equation number as printed in the manuscript, or the nearest numbered equation plus where the problem sits relative to it
- a short quote of the offending expression
- what is wrong, in one or two sentences
- what it should be instead, if you can determine that
- your confidence: high, medium, or low

Report only what you can argue for. If you find nothing you can defend, say so plainly: that is an acceptable answer. Do not pad the list with weak observations.

End with a one-line summary naming the equation numbers you are most confident about.
```
