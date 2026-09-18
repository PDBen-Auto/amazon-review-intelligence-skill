# 采集适配

## Woot（仅 US，第三方可用性需当次确认）
```bash
python scripts/amazon_review_scraper.py B012345678 --mode max --output work/woot.json
python scripts/review_dedup_merge.py --woot work/woot.json -o work/unified.json
```
脚本通过 https://www.woot.com/review/Reviews/{ASIN} 请求 Reviews / PagingNext。basic 为一个组合，full 为星级拆分，max 为星级和排序组合；这些是抓取策略，不是评论数量保证。脚本保留 collection_events、coverage=unknown；检查异常和实际响应。首次失败先探测原因，不循环重复全部组合；必要时切换来源。

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
