# Indian Consumer Academy: building and iterating a consumer-education channel

**Guhan Purushothaman · Creator & Product Builder · Product and audience case study**

[Instagram channel](https://www.instagram.com/indianconsumeracademy/) · [One-page PDF](indian-consumer-academy.pdf)

**6,120 followers · 4 posts listed on the public profile · Snapshot: 11 November 2026.** These are audience totals, not a measured growth rate. [Snapshot source](evidence/instagram-public-snapshot.json).

## 1. Audience problem and content hypothesis

Everyday purchases hide complicated economics and supply-chain choices: why does a candy still cost one rupee, and why is medicine packaged differently in India and the US? The product premise is to make these mechanisms understandable without specialist knowledge. Familiar questions, visible cause and effect, and an early payoff guide the content.

## 2. Evidence that guided iteration

Production review identified a slow, visually sparse candy opening and details that were hard to read on a phone. A separate review caught an animation that accidentally implied the price had fallen back. These are qualitative review findings, not audience-retention measurements. They provided concrete reasons to revise the work.

## 3. What changed and why

| Issue | Product decision | Purpose |
|---|---|---|
| The opening did not make the central question immediately visible. | Rebuilt it around a stocked shop, rising price wheels and one unchanged candy price. | Establish the viewer's question before explaining the mechanism. |
| A thin transaction path was difficult to read at phone size. | Replaced it with a row of available coins and an empty change slot. | Prioritize comprehension over visual complexity. |
| A moving price fragment made the price appear to revert. | Kept the new price visible while illustrating the missing change separately. | Preserve factual meaning while improving the presentation. |

## 4. AI-assisted execution and experiment design

I owned the workflow from audience questions and research to creative briefs, production and publishing. With Claude, I developed reusable React/TypeScript components and a Remotion production pipeline, linking animation to measured narration timing and adding automated visual-quality checks. Briefs, prototypes and acceptance checks made the work reviewable throughout delivery.

One concrete release check: the saved verification report for a branding-only update compares **11,574 frames** of the lossless master and records **zero pixel-sample changes outside the approved lettering regions**, with audio packets and timing preserved. This demonstrates precise change scope and release validation. [Verification summary](evidence/consumer-branding-qa-summary.json).

For the medicine-packaging film, I developed three title-and-thumbnail directions: a direct comparison, a hidden supply-chain explanation, and an unexpected tie. Each expresses a different viewer motivation; previews were prepared at phone-feed sizes. The board proposes a watch-time-based platform comparison. It is evidence of experiment design, not a completed test or a winning variant.

## 5. Results and lessons

The channel has a real audience of **6,120 followers**, alongside a documented sequence of creative alternatives, review findings and product revisions. The work demonstrates product ownership, requirements definition, hypothesis development, prioritization, AI-assisted development, release validation and technical communication. The next measurement step is to connect published versions to watch time, completion, saves/shares per reached account and follows, keeping topic and distribution differences visible.

**Measurement boundary:** no private Insights export or controlled comparison was available in the reviewed materials. This case does not attribute follower growth to a specific revision or claim a retention lift. The product framing is a retrospective synthesis of the repository's actual decisions.

[Decision evidence and provenance](evidence/consumer-education-decisions.md) · [Product portfolio](../product-work.md)
