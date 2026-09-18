# Amazon Review Collection And Insight Skill

一个面向 Amazon 产品团队的评论采集、证据整理、VOC 洞察和产品改进 Skill。

## 一句话定位

> 不只抓评论，而是把 ASIN、原始评论、覆盖边界、Excel、离线 HTML、用户需求和产品改进假设串成一条可复核的决策链。

## GitHub 上有没有对标？

有。GitHub 上的主要对标分为四类：

- 采集 API：擅长代理、渲染、多市场和规模化数据抓取；
- 浏览器采集器：擅长用户控制浏览器、可见 DOM 和安全停止；
- AI 评论分析器：擅长情感、痛点、趋势和仪表板；
- 工作簿型 Skill：擅长事实表格、覆盖率检查和标注回写。

本 Skill 不声称在采集 API 速度、代理资源或市场数量上绝对领先。它的优势是把这些能力之后最容易缺失的决策层补齐：覆盖边界、保守去重、原声证据、产品主题、改进假设和跨 Skill 交接。

详细对标见 [`references/competitive-positioning.md`](references/competitive-positioning.md)。

## 对标仓库

| 类型 | 代表仓库 | 主要优势 |
| --- | --- | --- |
| 采集 API | [Oxylabs Amazon Scraper](https://github.com/oxylabs/amazon-scraper) | 多类 Amazon 数据和规模化 API |
| 评论采集 | [ScrapingBee Amazon Review Scraper](https://github.com/ScrapingBee/amazon-review-scraper) | 代理轮换、JS 渲染和 CSV 输出 |
| 多市场抓取 | [Omkarcloud Amazon Scraper](https://github.com/omkarcloud/amazon-scraper) | 24 个 Amazon 市场的结构化数据 |
| AI VOC | [VOC Amazon Reviews](https://github.com/mguozhen/voc-amazon-reviews) | Agent 工具、痛点、Listing 改进和 HTML Dashboard |
| 评论洞察 Skill | [Amazon Review Insights](https://github.com/SparkBayes/amazon-review-insights-skill) | 负面识别、趋势和增量更新 |
| 工作簿 Skill | [Amazon Review Workbook Skill](https://github.com/aduo6668/amazon-review-workbook-skill) | 固定格式事实工作簿和覆盖率检查 |
| 浏览器安全采集 | [amazon-full-reviews](https://github.com/magoraichuhai/amazon-full-reviews) | 用户控制浏览器和审计停止条件 |

## 我们的卖点

### 1. 采集和分析不再断开

同一个工作流可以处理：

```text
ASIN / 商品链接
  -> 采集
  -> 多源合并
  -> 保守去重
  -> 原始评论 Excel
  -> 中文 HTML 分析
  -> 需求主题和竞品弱点
  -> 产品改进与验证假设
```

### 2. 不夸大“全量”

明确区分：

- written reviews；
- star-only ratings；
- 接口返回数量；
- 浏览器可见样本；
- 分析样本；
- 真实总体发生率。

这比单纯输出一个评论数量更适合产品、研发和运营决策。

### 3. 原声和结论可追溯

每条分析结果可以回到：

- 评论 ID；
- 完整正文；
- 原评论链接；
- 采集来源；
- 日期和星级；
- 翻译与摘要的区别；
- 主问题、二级标签和主题关联。

### 4. 直接连接产品决策

输出不止是正负面情感，而是：

- 用户真正想完成的任务；
- 反复出现的失败场景；
- 竞品弱点；
- 换品牌或退货触发器；
- 产品、说明书、包装、适配、安装和 Listing 的改进方向；
- 下一步需要访谈、打样或数据验证的假设。

### 5. 低供应商锁定

支持本地接口采集、浏览器捕获、已有 JSON/CSV/XLSX、可选连接器和离线 HTML。不是只能把数据留在一个商业仪表板里。

## 适合谁

- Amazon 产品经理和产品研发团队；
- 跨境电商运营和 Listing 团队；
- 竞品研究和 VOC 团队；
- 供应链、质量和售后团队；
- 需要把评论证据交给访谈、PRD、Battle Card 或统一证据包的团队。

## 安装与调用

将仓库中的 Skill 目录复制到 Codex 用户 Skill 目录，然后调用：

```text
$amazon-review-scraper
```

常用请求：

```text
抓取这些 ASIN 的可获取文字评论，去重后导出 Excel 和中文 HTML 报告。
```

```text
我已经有评论 JSON，不需要重新抓取，请分析差评主题、正面卖点、竞品弱点和改进优先级。
```

```text
从这些竞品 Amazon 评论中找出用户换品牌的原因，并输出带原声证据的产品机会假设。
```

## 输出

- 原始采集 JSON 和状态日志；
- canonical review JSON；
- 批量 Excel：`all_reviews`、`reviews_summary`、`README`；
- 单 ASIN 精简 Excel：`Review原始数据`；
- 单文件离线 HTML 分析报告；
- VOC Snapshot；
- 可选的 `amazon-product-evidence-contract` 证据交接包。

## 重要边界

本项目不保证获取 Amazon 全部评论，不绕过 CAPTCHA、登录墙或账户安全机制，也不把评论样本当成总体故障率。评论分析是公开声音研究，应与访谈、客服数据、退货数据和正式统计结合使用。

## 本地版本

本仓库对应的本机安装目录为：

`C:\Users\SYZ\.codex\skills\amazon-review-scraper`
