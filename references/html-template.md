# HTML 报告模板要求

本文件描述客诉/评论分析 HTML 报告应包含的结构和交互。生成时可自行实现样式，但必须保留这些功能。

## 页面结构

```text
Header
  产品名 / ASIN超链接 / 市场 / 分析日期 / 数据来源

Nav Tabs
  数据概览
  负面反馈 TOP10
  正面反馈 TOP10
  适配性分析（有数据时显示）
  改进建议

Modal
  用户原声列表
  星级筛选

Sections
  数据概览
  负面反馈 TOP10
  正面反馈 TOP10
  适配性分析
  改进建议矩阵
```

## 数据概览

必须包含产品基础信息卡：

```html
<div class="product-info">
  <img class="product-img" src="{产品图片或data URI}" alt="{ASIN} 产品图片">
  <div>
    <div>产品基础信息</div>
    <h3>{产品标题}</h3>
    <a href="{listing_url}" target="_blank">打开 Listing</a>
    <div class="product-meta">
      <div>品牌：{brand}</div>
      <div>ASIN：<a href="{listing_url}" target="_blank">{asin}</a></div>
      <div>链接评分：{rating}</div>
      <div>评论数：{review_count}</div>
    </div>
  </div>
</div>
```

图片规则：

- 优先使用 data URI，保证本地 HTML 可显示。
- 若使用相对图片文件，必须放在 HTML 同目录或可访问输出目录。
- 不要依赖可能被防盗链拦截的外部图片链接。

## TOP 项交互

负面和正面 TOP 列表使用相同交互：

1. 点击 TOP 行，展开详情。
2. 详情内展示：
   - 频次和占比
   - 原因分析/卖点解释
   - 建议方案
   - 二级问题/卖点标签
3. 点击二级标签，内联展开对应原声。
4. 点击“查看全部原声”，打开 Modal。
5. Modal 按星级筛选：
   - 负面：1星、2星、3星
   - 正面：4星、5星

### 原声全量与分页

- TOP 项的“查看原声”必须打开该主类下的全量评论，不得只传入示例评论。
- 每页最多显示 10 条；超过 10 条时显示上一页、下一页、当前页/总页数及筛选后的总条数。
- 切换星级筛选后回到第 1 页，分页仍基于筛选后的全量评论。

### 评论图片

- 当源数据包含图片数量和评论链接时，提取公开页面实际可见的评论图片；仅展示成功获取的图片。
- 使用内嵌 data URI，缩略图点击后打开图片预览弹窗。图片预览不依赖外部链接。
- 无法提取时不使用虚构或无关图片替代；保留原评论链接和图片数量说明。

## 数据结构建议

```javascript
const NEG_ISSUES = [
  {
    issue: "质量差/易坏",
    count: 39,
    pct: 24.8,
    cause: "...",
    suggest: "...",
    subissues: [
      { name: "无法工作", cnt: 12, kws: ["doesn't work"], detail: "..." }
    ]
  }
];

const POS_ISSUES = [
  {
    issue: "降温/风量满意",
    count: 134,
    pct: 53.2,
    cause: "...",
    suggest: "...",
    subissues: [
      { name: "降温有效", cnt: 55, kws: ["cool"], detail: "..." }
    ]
  }
];

const REVIEWS = [
  {
    id: 1,
    stars: 5,
    src: "亚马逊评论",
    date: "2026-06-13",
    title: "...",
    orig: "...",
    trans: "...",
    link: "..."
  }
];
```

## 百分比口径

必须在页面说明：

```text
TOP10 使用单评论主类归因。每条评论只计入一个最主要问题/卖点，因此各 TOP 项百分比合计约为 100%。
```

实现时：

- 先为每条评论选出一个 primary issue。
- 再按 primary issue 汇总 count。
- pct = count / 该组评论总数。
- 最后一项可用 `100 - 已累计百分比` 修正四舍五入误差。

## 样式建议

- 使用清晰的卡片布局，不嵌套卡片。
- 负面使用红/橙提示，正面使用绿/蓝提示。
- 产品图片使用 `object-fit: contain`，避免裁切。
- 移动端产品信息卡改为单列。

## 生成后自检

生成 HTML 后检查：

- JavaScript 语法无错误。
- 导航 Tab 可切换。
- 负面 TOP 百分比合计约 100%。
- 正面 TOP 百分比合计约 100%。
- ASIN 链接可点击。
- 产品图片在本地 HTML 中可显示。
- “查看全部原声”和二级标签可展开。
