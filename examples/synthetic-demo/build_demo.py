#!/usr/bin/env python3
"""Build the public synthetic HTML and XLSX demo from one canonical JSON fixture."""

from __future__ import annotations

import html
import json
import shutil
import sys
from collections import Counter
from pathlib import Path


DEMO_DIR = Path(__file__).resolve().parent
ROOT = DEMO_DIR.parents[1]
DATA_PATH = DEMO_DIR / "reviews.json"
XLSX_PATH = DEMO_DIR / "amazon-review-demo.xlsx"
EXAMPLE_HTML = ROOT / "examples" / "synthetic-review-insight.html"
DOCS_DIR = ROOT / "docs"
DOCS_HTML = DOCS_DIR / "index.html"

sys.path.insert(0, str(ROOT / "scripts"))
from export_reviews import export  # noqa: E402


TOPIC_DETAILS = {
    "Mount slips": {
        "decision": "Increase grip before adding more mounting positions.",
        "action": "Prototype ribbed silicone pads and a higher-friction hinge; test vertical vents and rough-road vibration.",
    },
    "Low-speed noise": {
        "decision": "Treat low-speed sound as a quality issue, not only a motor specification.",
        "action": "Isolate the housing and rebalance the low-speed motor profile; verify cabin noise at night-use distance.",
    },
    "Power cable too short": {
        "decision": "Placement flexibility is constrained by cable reach.",
        "action": "Offer a longer cable or extension option and publish placement diagrams for front seat, headrest, and second row.",
    },
    "Instructions unclear": {
        "decision": "Power expectations are creating avoidable mismatch.",
        "action": "State 'USB powered, no internal battery' on the first instruction panel and in the listing comparison image.",
    },
    "Strong airflow": {
        "decision": "Airflow is the main reason customers keep the product.",
        "action": "Protect blade geometry and three-speed separation while improving the mount and housing.",
    },
    "Easy installation": {
        "decision": "Tool-free setup supports multi-car use.",
        "action": "Keep one-hand clip operation and validate opening force across common mounting surfaces.",
    },
    "Compact footprint": {
        "decision": "Small size reduces visibility and dashboard conflicts.",
        "action": "Preserve the current housing envelope and show sightline clearance in product images.",
    },
    "Comfortable sound level": {
        "decision": "Medium-speed sound is acceptable even though low-speed buzzing needs correction.",
        "action": "Use medium speed as the acoustic benchmark and isolate the low-speed resonance path.",
    },
    "Flexible USB power": {
        "decision": "USB compatibility expands use beyond the vehicle.",
        "action": "Retain standard USB input and clarify compatible power-bank output requirements.",
    },
}


def load_and_validate() -> dict:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if data.get("collection", {}).get("synthetic") is not True:
        raise ValueError("Demo input must be explicitly marked synthetic")
    reviews = data.get("reviews")
    if not isinstance(reviews, list) or not reviews:
        raise ValueError("Demo input must contain reviews")
    ids = [review.get("review_id") for review in reviews]
    if len(ids) != len(set(ids)) or any(not review_id for review_id in ids):
        raise ValueError("Every synthetic review must have a unique review_id")
    for review in reviews:
        if review.get("rating") not in range(1, 6):
            raise ValueError(f"Invalid rating for {review.get('review_id')}")
        if review["rating"] <= 3 and not review.get("primary_issue"):
            raise ValueError(f"Missing primary_issue for {review.get('review_id')}")
        if review["rating"] >= 4 and not review.get("primary_benefit"):
            raise ValueError(f"Missing primary_benefit for {review.get('review_id')}")
    return data


def summarize(reviews: list[dict], positive: bool) -> list[dict]:
    selected = [review for review in reviews if (review["rating"] >= 4) == positive]
    key = "primary_benefit" if positive else "primary_issue"
    counts = Counter(review[key] for review in selected)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    topics = []
    running = 0.0
    for index, (name, count) in enumerate(ordered):
        pct = round(count * 100 / len(selected), 1)
        if index == len(ordered) - 1:
            pct = round(100.0 - running, 1)
        running += pct
        details = TOPIC_DETAILS[name]
        topics.append(
            {
                "name": name,
                "count": count,
                "pct": pct,
                "decision": details["decision"],
                "action": details["action"],
                "review_ids": [review["review_id"] for review in selected if review[key] == name],
            }
        )
    if round(sum(topic["pct"] for topic in topics), 1) != 100.0:
        raise ValueError("Topic percentages must sum to 100%")
    return topics


def build_payload(data: dict, data_href: str, xlsx_href: str) -> dict:
    reviews = data["reviews"]
    ratings = Counter(review["rating"] for review in reviews)
    average = round(sum(review["rating"] for review in reviews) / len(reviews), 2)
    return {
        "product": data["product"],
        "collection": data["collection"],
        "reviews": reviews,
        "negative": summarize(reviews, positive=False),
        "positive": summarize(reviews, positive=True),
        "summary": {
            "review_count": len(reviews),
            "negative_count": sum(count for rating, count in ratings.items() if rating <= 3),
            "positive_count": sum(count for rating, count in ratings.items() if rating >= 4),
            "average_rating": average,
            "deduplicated_count": data["collection"]["deduplicated_records"],
        },
        "files": {"json": data_href, "xlsx": xlsx_href},
    }


def render_html(payload: dict) -> str:
    encoded = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    product_title = html.escape(payload["product"]["title"])
    description = "Runnable synthetic Amazon review intelligence demo with traceable JSON, Excel evidence, and product decisions."
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Amazon Review Intelligence Demo | Synthetic Product Case</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://pdben-auto.github.io/amazon-review-intelligence-skill/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Amazon Review Intelligence Skill">
  <meta property="og:description" content="From written Amazon reviews to traceable product decisions, Excel evidence, and offline HTML reporting.">
  <meta property="og:url" content="https://pdben-auto.github.io/amazon-review-intelligence-skill/">
  <meta property="og:image" content="https://pdben-auto.github.io/amazon-review-intelligence-skill/assets/github-social-preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <style>
    :root {{ color-scheme:light; font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif; color:#1d2734; background:#f5f7fa; line-height:1.5; }}
    * {{ box-sizing:border-box; }} body {{ margin:0; }} button,a {{ font:inherit; }} button {{ cursor:pointer; }}
    .topbar {{ background:#172331; color:#fff; border-bottom:4px solid #de9b2b; }}
    .topbar-inner {{ max-width:1180px; margin:auto; padding:22px 24px 20px; display:flex; justify-content:space-between; gap:24px; align-items:flex-end; }}
    .eyebrow {{ color:#a9bad0; font-size:12px; font-weight:700; text-transform:uppercase; }}
    h1 {{ margin:4px 0 5px; font-size:28px; line-height:1.2; letter-spacing:0; }}
    .topbar p {{ margin:0; color:#cdd6e1; max-width:720px; }}
    .synthetic {{ flex:0 0 auto; border:1px solid #e8bd72; color:#ffdc9f; padding:7px 10px; font-size:12px; font-weight:700; border-radius:4px; }}
    .shell {{ max-width:1180px; margin:auto; padding:20px 24px 48px; }}
    .toolbar {{ display:flex; justify-content:space-between; gap:16px; align-items:center; margin-bottom:18px; }}
    .tabs {{ display:flex; gap:4px; flex-wrap:wrap; }}
    .tab {{ border:1px solid #cdd5df; background:#fff; color:#334155; padding:8px 12px; border-radius:5px; font-weight:650; }}
    .tab[aria-selected="true"] {{ background:#215e78; border-color:#215e78; color:#fff; }}
    .downloads {{ display:flex; gap:8px; }}
    .download {{ color:#1d5d78; text-decoration:none; border-bottom:1px solid #1d5d78; font-size:13px; }}
    .panel[hidden] {{ display:none; }}
    .kpis {{ display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:10px; }}
    .kpi {{ background:#fff; border:1px solid #dbe1e8; border-radius:6px; padding:15px; min-height:105px; }}
    .kpi-label {{ color:#637083; font-size:12px; }} .kpi-value {{ margin-top:8px; font-size:25px; font-weight:760; }}
    .decision-grid {{ display:grid; grid-template-columns:1.35fr 1fr; gap:18px; margin-top:18px; }}
    .section {{ background:#fff; border:1px solid #dbe1e8; border-radius:6px; padding:20px; }}
    h2 {{ font-size:19px; margin:0 0 12px; }} h3 {{ font-size:15px; margin:0 0 8px; }}
    .lead {{ color:#4e5d70; margin:0; }} .note {{ color:#68768a; font-size:13px; }}
    .finding {{ border-top:1px solid #e7ebf0; padding:12px 0; }} .finding:first-of-type {{ border-top:0; padding-top:0; }}
    .finding strong {{ display:block; margin-bottom:3px; }}
    .scope-list {{ margin:0; padding-left:18px; }} .scope-list li {{ margin:7px 0; }}
    .topic-table {{ width:100%; border-collapse:collapse; background:#fff; border:1px solid #dbe1e8; }}
    .topic-table th {{ background:#27384a; color:#fff; text-align:left; font-size:12px; padding:10px; }}
    .topic-table td {{ border-top:1px solid #e6eaf0; padding:11px 10px; vertical-align:top; }}
    .topic-table td:nth-child(2),.topic-table td:nth-child(3) {{ width:78px; text-align:right; font-variant-numeric:tabular-nums; }}
    .topic-table td:last-child {{ width:110px; text-align:right; }}
    .voice-btn {{ border:1px solid #9cabbc; background:#fff; color:#24465f; border-radius:4px; padding:6px 8px; }}
    .negative .topic-table th {{ background:#773b39; }} .positive .topic-table th {{ background:#2f6756; }}
    .bar {{ width:100%; height:7px; background:#e9edf2; margin-top:7px; overflow:hidden; border-radius:2px; }}
    .bar span {{ display:block; height:100%; background:#c7544f; }} .positive .bar span {{ background:#3d8069; }}
    .action-table {{ display:grid; grid-template-columns:120px 1fr 1.2fr; border:1px solid #dbe1e8; background:#fff; }}
    .action-table > div {{ padding:12px; border-top:1px solid #e6eaf0; }}
    .action-table > div:nth-child(-n+3) {{ border-top:0; background:#27384a; color:#fff; font-weight:700; font-size:12px; }}
    .priority {{ color:#9c332f; font-weight:750; }}
    dialog {{ width:min(880px,calc(100% - 28px)); border:0; border-radius:7px; padding:0; box-shadow:0 18px 60px #18233355; }}
    dialog::backdrop {{ background:#11182799; }}
    .modal-head {{ display:flex; justify-content:space-between; align-items:flex-start; gap:16px; background:#172331; color:#fff; padding:17px 20px; }}
    .modal-head h2 {{ margin:0; }} .close {{ border:0; background:transparent; color:#fff; font-size:24px; line-height:1; }}
    .modal-controls {{ display:flex; justify-content:space-between; gap:12px; align-items:center; padding:12px 20px; border-bottom:1px solid #e2e7ed; }}
    select {{ border:1px solid #b9c3cf; border-radius:4px; padding:7px 9px; background:#fff; }}
    .voices {{ padding:0 20px; max-height:55vh; overflow:auto; }}
    .voice {{ padding:15px 0; border-bottom:1px solid #e5e9ee; }} .voice:last-child {{ border-bottom:0; }}
    .voice-meta {{ color:#6c7888; font-size:12px; margin-bottom:5px; }} .voice-title {{ font-weight:730; margin-bottom:5px; }} .voice p {{ margin:5px 0; }}
    .translation {{ color:#46566a; background:#f5f7f9; padding:9px 10px; border-left:3px solid #497a99; }}
    .pager {{ display:flex; justify-content:flex-end; gap:9px; align-items:center; padding:12px 20px 18px; }} .pager button {{ border:1px solid #aeb8c4; background:#fff; border-radius:4px; padding:6px 9px; }}
    .footer {{ margin-top:18px; color:#6a7788; font-size:12px; }}
    @media(max-width:850px) {{ .kpis {{ grid-template-columns:repeat(2,1fr); }} .decision-grid {{ grid-template-columns:1fr; }} .action-table {{ grid-template-columns:1fr; }} .action-table > div {{ border-top:0; }} .action-table > div:nth-child(-n+3) {{ display:none; }} .action-table > div:nth-child(3n+1) {{ padding-bottom:2px; color:#9c332f; font-weight:750; }} .topbar-inner,.toolbar {{ align-items:flex-start; flex-direction:column; }} }}
    @media(max-width:520px) {{ .shell,.topbar-inner {{ padding-left:14px; padding-right:14px; }} .kpis {{ grid-template-columns:1fr 1fr; }} .kpi {{ min-height:92px; }} .kpi-value {{ font-size:21px; }} .topic-table th:nth-child(4),.topic-table td:nth-child(4) {{ display:none; }} }}
  </style>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Amazon Review Intelligence Skill","applicationCategory":"BusinessApplication","operatingSystem":"Cross-platform AI agent runtime","url":"https://github.com/PDBen-Auto/amazon-review-intelligence-skill"}}</script>
</head>
<body>
  <header class="topbar"><div class="topbar-inner"><div><div class="eyebrow">Amazon Review Intelligence Skill</div><h1>{product_title}</h1><p>One synthetic evidence file transformed into an auditable Excel workbook and an interactive product-decision report.</p></div><div class="synthetic">SYNTHETIC DATA · 20 RECORDS</div></div></header>
  <main class="shell">
    <div class="toolbar"><nav class="tabs" aria-label="Report views"><button class="tab" data-tab="overview" aria-selected="true">Overview</button><button class="tab" data-tab="negative" aria-selected="false">Negative issues</button><button class="tab" data-tab="positive" aria-selected="false">Positive drivers</button><button class="tab" data-tab="actions" aria-selected="false">Product actions</button></nav><div class="downloads"><a class="download" id="jsonLink">Input JSON</a><a class="download" id="xlsxLink">Evidence Excel</a></div></div>
    <section class="panel" id="overview"><div class="kpis" id="kpis"></div><div class="decision-grid"><section class="section"><h2>Decision summary</h2><div id="findings"></div></section><aside class="section"><h2>Evidence boundary</h2><ul class="scope-list"><li>All records are synthetic and clearly labeled.</li><li>Written-review counts remain separate from listing rating totals.</li><li>Each review has one primary issue or benefit, so group percentages reconcile to 100%.</li><li>Original text and Chinese translation remain separate fields.</li></ul></aside></div></section>
    <section class="panel negative" id="negative" hidden><h2>Negative issue priorities</h2><p class="note">1-3 star records. Click a topic to inspect every supporting synthetic voice.</p><div id="negativeTable"></div></section>
    <section class="panel positive" id="positive" hidden><h2>Positive purchase drivers</h2><p class="note">4-5 star records. Product changes should protect these reasons to buy.</p><div id="positiveTable"></div></section>
    <section class="panel" id="actions" hidden><h2>Product action matrix</h2><p class="note">Actions combine observed negative friction with the positive attributes worth preserving.</p><div class="action-table" id="actionTable"><div>Priority</div><div>Product decision</div><div>Next validation</div></div></section>
    <p class="footer">Synthetic demonstration only. It contains no real Amazon ASIN, account, customer, review, or collection result. The XLSX and HTML are regenerated from the linked canonical JSON.</p>
  </main>
  <dialog id="voiceDialog"><div class="modal-head"><div><div class="eyebrow">Traceable evidence</div><h2 id="modalTitle"></h2></div><button class="close" id="closeDialog" aria-label="Close">×</button></div><div class="modal-controls"><label>Rating <select id="ratingFilter"><option value="all">All</option></select></label><span class="note" id="voiceCount"></span></div><div class="voices" id="voices"></div><div class="pager"><button id="prevPage">Previous</button><span id="pageStatus"></span><button id="nextPage">Next</button></div></dialog>
  <script>
    const APP = {encoded};
    const pageSize = 5;
    let modalReviews = [];
    let page = 1;
    let activeTopic = "";
    const byId = id => document.getElementById(id);
    const node = (tag, className, text) => {{ const el=document.createElement(tag); if(className) el.className=className; if(text!==undefined) el.textContent=text; return el; }};

    document.querySelectorAll('.tab').forEach(button => button.addEventListener('click', () => {{
      document.querySelectorAll('.tab').forEach(item => item.setAttribute('aria-selected', String(item === button)));
      document.querySelectorAll('.panel').forEach(panel => panel.hidden = panel.id !== button.dataset.tab);
    }}));

    byId('jsonLink').href = APP.files.json;
    byId('xlsxLink').href = APP.files.xlsx;
    const metrics = [
      ['Written reviews', APP.summary.review_count],
      ['Deduplicated records', APP.summary.deduplicated_count],
      ['Average rating', APP.summary.average_rating + ' / 5'],
      ['Negative sample', APP.summary.negative_count],
      ['Positive sample', APP.summary.positive_count],
    ];
    metrics.forEach(([label,value]) => {{ const card=node('div','kpi'); card.append(node('div','kpi-label',label),node('div','kpi-value',String(value))); byId('kpis').append(card); }});

    const leadingNegative = APP.negative[0];
    const leadingPositive = APP.positive[0];
    [
      ['Fix first', `${{leadingNegative.name}} appears in ${{leadingNegative.count}} of ${{APP.summary.negative_count}} negative reviews (${{leadingNegative.pct}}%).`],
      ['Protect', `${{leadingPositive.name}} appears in ${{leadingPositive.count}} of ${{APP.summary.positive_count}} positive reviews (${{leadingPositive.pct}}%).`],
      ['Product direction', 'Improve grip and low-speed refinement without increasing the compact housing or reducing medium-speed airflow.'],
    ].forEach(([title,text]) => {{ const wrap=node('div','finding'); wrap.append(node('strong','',title),node('div','lead',text)); byId('findings').append(wrap); }});

    function renderTopics(targetId, topics) {{
      const table=node('table','topic-table');
      const head=document.createElement('thead'); const row=document.createElement('tr');
      ['Primary theme','Count','Share','Decision implication','Evidence'].forEach(text => row.append(node('th','',text))); head.append(row); table.append(head);
      const body=document.createElement('tbody');
      topics.forEach(topic => {{
        const tr=document.createElement('tr'); const nameCell=document.createElement('td'); nameCell.append(node('strong','',topic.name)); const bar=node('div','bar'); const fill=node('span'); fill.style.width=topic.pct+'%'; bar.append(fill); nameCell.append(bar); tr.append(nameCell,node('td','',String(topic.count)),node('td','',topic.pct+'%'),node('td','',topic.decision));
        const action=document.createElement('td'); const button=node('button','voice-btn','View voices'); button.addEventListener('click',()=>openVoices(topic)); action.append(button); tr.append(action); body.append(tr);
      }}); table.append(body); byId(targetId).append(table);
    }}
    renderTopics('negativeTable', APP.negative);
    renderTopics('positiveTable', APP.positive);

    const actionRows = [
      ['HIGH', APP.negative[0].decision, APP.negative[0].action],
      ['HIGH', APP.negative[1].decision, APP.negative[1].action],
      ['MEDIUM', APP.negative[2].decision, APP.negative[2].action],
      ['MEDIUM', APP.negative[3].decision, APP.negative[3].action],
      ['PROTECT', APP.positive[0].decision, APP.positive[0].action],
    ];
    actionRows.forEach(([priority,decision,action]) => byId('actionTable').append(node('div','priority',priority),node('div','',decision),node('div','',action)));

    function openVoices(topic) {{
      activeTopic=topic.name; modalReviews=APP.reviews.filter(review => topic.review_ids.includes(review.review_id)); page=1;
      byId('modalTitle').textContent=topic.name;
      const filter=byId('ratingFilter'); filter.textContent=''; const all=node('option','','All'); all.value='all'; filter.append(all);
      [...new Set(modalReviews.map(review=>review.rating))].sort().forEach(rating => {{ const option=node('option','',rating+' stars'); option.value=String(rating); filter.append(option); }});
      renderVoices(); byId('voiceDialog').showModal();
    }}
    function filteredReviews() {{ const value=byId('ratingFilter').value; return value==='all' ? modalReviews : modalReviews.filter(review=>String(review.rating)===value); }}
    function renderVoices() {{
      const selected=filteredReviews(); const pages=Math.max(1,Math.ceil(selected.length/pageSize)); page=Math.min(page,pages); const slice=selected.slice((page-1)*pageSize,page*pageSize); const container=byId('voices'); container.textContent='';
      slice.forEach(review => {{ const item=node('article','voice'); item.append(node('div','voice-meta',`${{review.rating}} stars · ${{review.date}} · ${{review.review_id}}`),node('div','voice-title',review.title),node('p','',review.text),node('p','translation',review.translation_zh)); container.append(item); }});
      byId('voiceCount').textContent=selected.length+' records'; byId('pageStatus').textContent=`${{page}} / ${{pages}}`; byId('prevPage').disabled=page<=1; byId('nextPage').disabled=page>=pages;
    }}
    byId('ratingFilter').addEventListener('change',()=>{{ page=1; renderVoices(); }}); byId('prevPage').addEventListener('click',()=>{{ page--; renderVoices(); }}); byId('nextPage').addEventListener('click',()=>{{ page++; renderVoices(); }}); byId('closeDialog').addEventListener('click',()=>byId('voiceDialog').close());
  </script>
</body>
</html>'''


def main() -> None:
    data = load_and_validate()
    export(DATA_PATH, XLSX_PATH)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    docs_demo = DOCS_DIR / "demo"
    docs_demo.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DATA_PATH, docs_demo / DATA_PATH.name)
    shutil.copy2(XLSX_PATH, docs_demo / XLSX_PATH.name)

    local_payload = build_payload(data, "synthetic-demo/reviews.json", "synthetic-demo/amazon-review-demo.xlsx")
    pages_payload = build_payload(data, "demo/reviews.json", "demo/amazon-review-demo.xlsx")
    EXAMPLE_HTML.write_text(render_html(local_payload), encoding="utf-8")
    DOCS_HTML.write_text(render_html(pages_payload), encoding="utf-8")
    print(f"Built synthetic demo: {len(data['reviews'])} reviews")
    print(EXAMPLE_HTML)
    print(XLSX_PATH)


if __name__ == "__main__":
    main()
