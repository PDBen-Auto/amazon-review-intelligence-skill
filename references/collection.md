# 采集适配

## Woot（仅 US，第三方可用性需当次确认）
```bash
python scripts/amazon_review_scraper.py B012345678 --woot-offer-url https://home.woot.com/offers/example-product --mode basic --output work/woot_probe.json
python scripts/amazon_review_scraper.py B012345678 --woot-offer-url https://home.woot.com/offers/example-product --mode max --output work/woot.json
python scripts/review_dedup_merge.py --woot work/woot.json -o work/unified.json
```
先通过 Woot 当前商品页或公开搜索找到 `/offers/` URL，核对页面内 `offerItems[].Asin` 与目标 ASIN 完全一致。页面提供 `offerId` 和实际子域名；评论接口为 `https://{subdomain}.woot.com/review/Reviews/{ASIN}?offerid={offerId}&filter=0&isVerified=false&sort=0&page=1`，后续按响应 `PagingNext` 翻页。`itemid` 在页面的评论链接中，但本次抓包的 JSON 请求未携带它。不能拿别的商品的 offerId 试探目标 ASIN。Woot 未上架目标商品时记为 `woot_mapping_missing`，改用 Amazon 评论页或获准连接器。basic 为一个组合，full 为星级拆分，max 为星级与页面验证的排序值 `0`（Top）、`1`（Most Recent）组合；这些是抓取策略，不是评论数量保证。404、结构错误或 HTTP 失败记为 `woot_failed`，不得写成成功采集 0 条。

页面的 `Show more reviews` 加载下一批评论，对应接口返回的 `PagingNext` 游标。每页通常 10 条；采集器持续用该游标请求，直到为空或达到每组合的 12 页上限。不能把第一页或页面初始可见条数当总数；到达上限时覆盖率仍为 unknown。页面的 `read more` 只展开长正文；本次抓包确认接口 `Text` 已包含完整正文，直接保留其全部字符，不按页面显示长度截断。若未来接口正文变短，应再用页面展开并核对。

扩量优先用 `full` 的五个星级分组，并用完整正文、日期、评分、作者做保守去重。需要最近评论或额外覆盖时，再比较 `max` 中 Most Recent 排序的净新增量。分页中途超时应保留已取到的完整页，状态写 `partial` 并记录失败筛选和页码；批量采集保留上次有效 JSON，将本次部分结果留在 `.pending.json`，不得标为完成。Woot 响应 `TotalReviews=-1` 时不能据此推算书面评论总量，页面 ratings 数量也不是 written reviews 总量。

## Sorftime（可选，不是安装包内服务）
发现实际产品评论工具后读取参数。按它支持的站点、日期与分页能力抓取；记录返回窗口和上限，不写死“全部”。保存返回的原始数组。旧版合并器支持字段：标题、评论、评星、评论日期（YYYYMMDD）、评论产品的属性。若实际 schema 不同，先做字段映射，不直接套用。
```bash
python scripts/review_dedup_merge.py --woot work/woot.json --sorftime work/sorftime.json -o work/unified.json
```
该合并器使用保守精确匹配。没有作者/日期的跨源相同评论可能保留为疑似重复，须审核；它不声称完成模糊去重。导出前保留真实原链接、ID、站点及原始日期。

## 浏览器补充
使用可用浏览器工具与相应技能。从 Listing/评论页抓取完整可见正文、ID、作者、日期、星级、规格、Verified、Helpful、链接和图片字段。展开“Read more”后再记录正文；无法展开则标记内容不完整。分页按下一页或 Show 10 more 实际链接继续。不要将页面导航短文当作评论。

## 日期和缺失值
清洗日期保留 date_raw，无法可靠解析则 date=null。应用日期条件时未知日期不冒充匹配；单独计数说明。未知布尔值用 null，不能变成 false；未知点赞数为空，不能变成零。
