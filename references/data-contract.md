# 工作 JSON

UTF-8，顶层对象包含 product、collection、reviews。product 包含 asin、requested_asin、actual_asin、marketplace、title、brand、listing_url、rating、ratings_count、written_reviews_count、image；无法获取则 null。collection 记录时间、渠道、限制、停止原因、筛选和数量。

reviews 数组字段：review_id、review_url、title、text（不截断）、rating（整数1–5或null）、date（ISO或null）、date_raw、author、variant、verified_purchase（true/false/null）、helpful_votes、image_urls、media_urls、source、summary_zh、primary_issue。分析可添加 translation_zh、secondary_issues；内部序号使用清洗后数组顺序，从1开始。排序建议星级升序，同星级日期降序，未知日期排后。

Excel 的来源列由 product.marketplace 生成为 Amazon XX Review，技术来源保留工作记录。summary_zh 是中文摘要；translation_zh 是忠实译文，不得互称。非英语全文仍存 text。报告通过序号关联主题原声，绝不只保留代表样本。
