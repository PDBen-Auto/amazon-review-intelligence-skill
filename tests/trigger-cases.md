# Trigger Checks

## Should trigger

1. “抓取这些 ASIN 的 Amazon 评论，去重后导出 Excel 和中文 HTML 分析报告。”
2. “我已经有评论 JSON，不需要抓取，请分析差评主题、正面卖点和改进优先级。”
3. “从竞品 Amazon 评论中找出用户换品牌的原因，并把真实原声整理成产品机会假设。”

## Should not trigger

1. “只做这个品类的市场规模、销量和利润空间研究。”
2. “请分析我公司的私有客服工单，但不涉及 Amazon 评论或公开 VOC。”

## Expected routing

Amazon review collection, review-file analysis, and Amazon-derived VOC should trigger this skill. Multi-platform public voice should add or hand off to `voice-of-customer-miner`; pure market sizing, private support-ticket analysis, and utility-patent claim work should route elsewhere.
