# Amazon Reviews -> VOC Bridge

This bridge combines the Amazon-specific collection strength of this skill with the need-based, evidence-labeled reasoning used by `voice-of-customer-miner`.

## When to use

Use this reference when the user asks:

- customers最不满意什么；
- 竞品评论暴露了哪些弱点；
- 用户为什么换品牌或退货；
- 评论如何转成 JTBD、机会假设、访谈问题或 battle-card evidence。

Do not use this bridge to claim population frequency, defect rate, conversion impact, or causality. Reviews are self-selected public voice and are usually skewed toward highly satisfied or highly dissatisfied users.

## Source separation

Keep these sources separate unless the report explicitly shows a source-by-source table:

- Amazon written reviews;
- Amazon ratings without written text;
- Amazon VOC or buyer messages;
- customer support tickets;
- refunds, returns, or warranty records;
- Reddit, forums, app stores, and competitor review sites.

Do not add counts from different sources into one percentage. Use the canonical review JSON for Amazon counts and label other sources separately.

## Theme method

1. Start from the review's full text and product context.
2. Write the customer need in solution-free language, usually 4-8 words.
3. Preserve one short real verbatim and its source URL when available.
4. Mark frequency as `recurring across sources`, `concentrated in one source`, or `isolated but vivid`.
5. Separate `Fact`, `Inference`, and `Assumption`.
6. Add the decision implication and one validation question.

Example:

```text
Theme: maintain reliable fit after installation
Frequency: recurring within the Amazon sample; not a population estimate
Verbatim: "..." — review URL
Fact: the reviewer reports repeated loosening after installation
Inference: installation tolerance or fastener retention may be a trust-breaking issue
Assumption: the problem affects a meaningful share of the target segment
Validation: reproduce the installation with three vehicle/fixture variants
```

## Required VOC output

When this bridge is requested, add:

1. 3-5 need-based themes with verbatims and source labels;
2. up to 5 competitor or product weak points supported by evidence;
3. switching triggers or purchase blockers;
4. 3 opportunity hypotheses phrased as problems, not features;
5. 2-3 assumptions to validate through interviews, tests, or support data;
6. a note on review-source skew and sample limits.

## Handoff to voice-of-customer-miner

Invoke `voice-of-customer-miner` when the user wants public voice across multiple platforms or wants the result to follow its exact four-option final step. Pass:

- the canonical Amazon review JSON path;
- the target decision;
- the theme or open-sweep choice;
- any competitor set;
- the existing Amazon sample cutoff and collection limitations.

The handoff must identify Amazon reviews as one source, not as a census of all customers.
