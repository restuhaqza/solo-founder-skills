# Quality Bar — "Enough Evidence"

**Contents**
1. What counts as evidence per assumption type
2. Gate conditions before writing the brief
3. Common ways this brief fools the founder
4. Sanity checks on the scorecard

---

## 1. What counts as evidence per assumption type

Use this to decide whether an assumption may be moved from `untested` to `supported`/`strong`. The rule throughout: **a behaviour, an amount, or a repetition — never a sentiment.**

| Type | `weak` | `supported` | `strong` |
| :-- | :-- | :-- | :-- |
| **Value** | People describe the problem unprompted | A narrow segment describes it unprompted *and* it recurs frequently | They are already paying (money or real time) to work around it |
| **Viability** | A plausible price with no test | Price stated and not refused by most of a segment | Someone pre-paid, deposited, or signed a paid pilot at that price |
| **Usability** | You explained it and they got it | They completed the core action unaided in a prototype | They returned and did it again without prompting |
| **Feasibility** | You have a rough plan | You shipped a throwaway spike of the hard part | The risky component is built and running |

## 2. Gate conditions before writing the brief

Do not emit a brief that claims validation unless:

- [ ] Every assumption in the plan has a status (no blanks).
- [ ] No **value** or **viability** assumption is `untested` — the script will block this anyway; do not override it by editing the script.
- [ ] Every `supported`/`strong` claim cites a specific behaviour, amount, or repetition.
- [ ] The **case against** names at least one real weakness. A brief with no counter-evidence is a brief that wasn't written honestly.
- [ ] The riskiest *unresolved* assumption is named, with a test that costs under a week.

## 3. Common ways this brief fools the founder

- **Interest dressed as demand.** Emails and compliments counted as validation. Fix: only money and repeated behaviour count at `strong`.
- **Anecdote as pattern.** One enthusiastic interview quoted as a trend. Fix: require the same theme from multiple people in the *same* segment.
- **Survivorship in the sample.** Interviewing only people who already like the category. Fix: include people who tried and abandoned a solution.
- **Segment blur.** Averaging across incompatible buyers. Fix: one ICP per validation pass.
- **Moving the goalposts.** Editing the scorecard thresholds until it passes. Fix: the thresholds are the point; if they block you, the evidence is telling you something.

## 4. Sanity checks on the scorecard

After running `scripts/evidence_scorecard.py`:

- If the verdict is `INSUFFICIENT EVIDENCE`, the next action is almost always **more interviews**, not more planning.
- If `coverage` is low (under ~0.5), the score is meaningless regardless of the band — you have not tested enough to have an opinion.
- If `weighted_score` is high but the **strongest evidence against** column is empty, be suspicious: you have not looked hard enough for disconfirming data.
- If `weighted_score` is low but you still feel certain, that certainty is exactly the bias this process is designed to catch. Test it.
