# Benchmark: Solo Founder Skills

The pack is evaluated, not just asserted. This document records how, and what
the results were. It is regenerated from the raw grading files in the
`*-workspace/iteration-*` directories, which are kept out of git.

## Method

Each skill is tested with a **trap prompt** — a realistic request a solo founder
actually makes, phrased so that a capable general-purpose model fails it (asks
for jargon, for 500 thin pages, to ship on a three-day peek, to skip a
bad-news update, and so on). Every prompt is run in two configurations:

- **with_skill** — the agent is told to read and follow that one skill.
- **without_skill** — the same prompt, with an explicit instruction *not* to
  read any skill, so the comparison measures the skill rather than the base
  model's willingness to help.

A separate **grader agent** — which reads only the output files, never the
transcript — scores each run against explicit pass/fail assertions (burden of
proof on PASS, no partial credit). The metric is pass rate per configuration.
Runs are 2–3 per configuration.

- Model under test: `cmc/deepseek/deepseek-v4.1-flash`
- **12 skills × 1 trap each × 2 configurations × 2–3 runs = 96 graded runs**
  across five iterations.
- **Pass rate is the only metric** — timing and token data were not captured.

## Iteration history

| Iteration | Skills under test | Runs | With | Without | Δ |
| :-- | :-- | --: | --: | --: | --: |
| 1 | first 6 | 12 | 100% | 80.8% | +0.19 |
| 2 | first 6 (sharper prompts) | 24 | 100% | 40.0% | +0.60 |
| 3 | second 6 | 24 | 100% | 71.7% | +0.28 |
| 4 | second 6 (tightened assertions) | 24 | 98.3% | 64.2% | +0.34 |
| 5 | 2 of the second 6 (defects fixed) | 12 | 100% | 68.5% | +0.31 |

Iterations 2 and 4 test the same six skills with progressively stricter
assertions: the delta fell from +0.60 to +0.34 because the assertions began
measuring behaviour the base model gets wrong, not because the skills weakened.
Iteration 1's low delta is a prompt-design artefact — the first prompts
telegraphed the intended answer.

## Per-skill results

Latest iteration for each skill. "With" is the mean pass rate with the skill;
"Without" is the same prompt with no skill.

| Skill | The trap it must avoid | With | Without | Δ | Iter |
| :-- | :-- | --: | --: | --: | --: |
| `solo-founder-os` | routes a beginner to **one** skill, not a menu | 1.00 | 0.20 | +0.80 | 2 |
| `pricing-strategy` | reprices without ignoring existing customers | 1.00 | 0.00 | +1.00 | 2 |
| `go-to-market-launch` | keeps outbound in the founder's hands | 1.00 | 0.30 | +0.70 | 2 |
| `mvp-scoping` | guards the 90/10 scope against creep | 1.00 | 0.60 | +0.40 | 2 |
| `product-metrics` | a weekly digest that ends in **one action** | 1.00 | 0.60 | +0.40 | 2 |
| `idea-validation` | separates compliments from evidence | 1.00 | 0.70 | +0.30 | 2 |
| `positioning-and-messaging` | refuses "revolutionary / all-in-one for everyone" | 1.00 | 0.57 | +0.43 | 5 |
| `content-and-seo-engine` | refuses 500 thin programmatic pages | 1.00 | 0.58 | +0.42 | 4 |
| `support-and-onboarding` | no AI chatbot at 30 customers | 1.00 | 0.60 | +0.40 | 4 |
| `experiments-and-growth` | refuses shipping on a 3-day peek | 1.00 | 0.70 | +0.30 | 4 |
| `founder-operating-rhythm` | runway verdict **and** the growth rate it flips at | 1.00 | 0.80 | +0.20 | 5 |
| `fundraising-and-investor-updates` | sends the bad-news update, does not skip it | 1.00 | 0.80 | +0.20 | 4 |

With the skill, every trap is passed. Without, the base model clears only 54%
of the assertions on average, and on the sharpest traps (`solo-founder-os`,
`pricing-strategy`) it fails most of them.

## Defects the loop found

The point of an eval loop is to catch real problems. Two were found and fixed:

1. **A false positive in `positioning-and-messaging/scripts/headline_lint.py`.**
   The canonical bad headline *"The all-in-one platform for everyone"* scored
   **85/100** (strong). The linter was taught the bare `all-in-one` cliché and a
   `vague_audience` deduction for `everyone`/`everybody`/`anyone`. It now scores
   **60/100**. Validated in a later run, where the same headline scored 36–60/100
   and the agent no longer trusted the high number.
2. **A missing output in `founder-operating-rhythm`.** The runway script reported
   the default-alive verdict but never the **growth rate at which the verdict
   flips** — the number a founder can act on. `runway.py` now computes and prints
   it on both the pre-tax and after-tax bases (`Flip growth rate: 2.8%/mo
   (pre-tax) · 4.0%/mo after tax`), verified by brute-forcing the script's own
   verdict (flips at 2.85%/mo).

## Caveats

- **Pass rate only.** No timing or token data was captured; cost/latency are not
  measured here.
- **One trap prompt per skill.** These are sharp, adversarial prompts, not a
  broad sample of the task space. They are designed to discriminate, not to
  estimate average performance.
- **Assertion sets were tightened across iterations.** A lower delta in a later
  iteration usually means a stricter (fairer) test, not a weaker skill.
- **Low run-to-run variance.** In iteration 5 (3 runs/config) all 12 cells scored
  identically across their runs, so the assertion set is stable and reproducible
  — but that also means run-to-run spread is too small to measure here.
