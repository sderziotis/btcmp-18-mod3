#!/usr/bin/env python3
"""
Searchly — Simulated Search Engine for OSINT Module 2
Supports operators: site:, filetype:, inurl:, intitle:, cache:
Pre-built index of all lab domains.
"""

from flask import Flask, request, render_template_string, abort
import re
from datetime import datetime

app = Flask(__name__)

# ──────────────────────────────────────────────
# Pre-built search index
# Each entry: title, url, snippet, domain, content (for full-text match)
# ──────────────────────────────────────────────
INDEX = [
    # ── northgate-uni.edu ──────────────────────────────────────────────────
    {
        "title": "Department of Computer Science — Northgate University",
        "url": "http://www.northgate-uni.edu/",
        "domain": "www.northgate-uni.edu",
        "snippet": "World-class research and teaching in AI, cybersecurity, distributed systems, and software engineering. Staff: Prof. Alan Whitmore, Dr. Petra Novak, Dr. Reza Tehrani.",
        "filetype": "html",
        "content": "northgate university computer science department alan whitmore petra novak reza tehrani django ansible kubernetes gitlab cybersecurity machine learning distributed systems",
    },
    {
        "title": "Staff Directory — Northgate University CS",
        "url": "http://www.northgate-uni.edu/staff.html",
        "domain": "www.northgate-uni.edu",
        "snippet": "Full staff listing: Prof. Alan Whitmore (HoD), Dr. Petra Novak, Dr. Reza Tehrani, Ms. Sophie Crane, Mr. Owen Fitzgerald (SysAdmin). Emails and office numbers listed.",
        "filetype": "html",
        "content": "staff directory alan whitmore petra novak reza tehrani sophie crane owen fitzgerald sysadmin email office northgate",
    },
    {
        "title": "Dr. Reza Tehrani — Lecturer in Software Engineering",
        "url": "http://www.northgate-uni.edu/staff/tehrani.html",
        "domain": "www.northgate-uni.edu",
        "snippet": "Lecturer in Software Engineering & Agile Methods. PhD TU Delft 2017. Research: technical debt, DevOps in regulated industries. Active on PostIt (@reza.tehrani).",
        "filetype": "html",
        "content": "reza tehrani software engineering agile postit social media phd delft technical debt devops northgate lecturer",
    },
    {
        "title": "robots.txt — Northgate University",
        "url": "http://www.northgate-uni.edu/robots.txt",
        "domain": "www.northgate-uni.edu",
        "snippet": "Disallow: /internal/ /staff-only/ /uploads/ /admin/ /db-backup/ — Note to webmaster: uploads/ should be cleared of stale files.",
        "filetype": "txt",
        "content": "robots disallow internal staff-only uploads admin db-backup webmaster stale files northgate",
    },
    {
        "title": "sitemap.xml — Northgate University",
        "url": "http://www.northgate-uni.edu/sitemap.xml",
        "domain": "www.northgate-uni.edu",
        "snippet": "XML sitemap listing all indexed pages including /uploads/budget_2024.pdf, /uploads/staff_roster.docx.bak, /uploads/requirements.txt, /internal/meeting_notes_jan2025.txt.",
        "filetype": "xml",
        "content": "sitemap northgate uploads budget staff roster requirements meeting notes internal xml",
    },
    {
        "title": "[PDF] budget_2024.pdf — Northgate University CS Dept",
        "url": "http://www.northgate-uni.edu/uploads/budget_2024.pdf",
        "domain": "www.northgate-uni.edu",
        "snippet": "CONFIDENTIAL DRAFT — CS Dept Budget AY 2024/2025. Total: £1,240,000. Staff salaries breakdown. Prepared by Sophie Crane. Approved by Prof. Whitmore. Uploaded to staff portal.",
        "filetype": "pdf",
        "content": "budget confidential northgate cs department staff salaries whitmore crane fitzgerald novak tehrani draft allocation 2024 2025 pdf",
    },
    {
        "title": "[BAK] staff_roster.docx.bak — Northgate University HR Export",
        "url": "http://www.northgate-uni.edu/uploads/staff_roster.docx.bak",
        "domain": "www.northgate-uni.edu",
        "snippet": "HR system export. Staff IDs, full names, emails, phone extensions, NI numbers, start dates. Includes visiting researchers. WARNING: UK GDPR protected data.",
        "filetype": "bak",
        "content": "staff roster hr export names emails phone ni number gdpr northgate whitmore novak tehrani crane fitzgerald matsuda ibanez bak backup",
    },
    {
        "title": "requirements.txt — Northgate University Portal",
        "url": "http://www.northgate-uni.edu/uploads/requirements.txt",
        "domain": "www.northgate-uni.edu",
        "snippet": "Python dependencies for internal portal. Django 4.2.7, psycopg2, redis, celery, gunicorn. Private PyPI mirror: pypi.internal.northgate-uni.edu. Maintainer: o.fitzgerald@northgate-uni.edu.",
        "filetype": "txt",
        "content": "requirements django psycopg2 redis celery gunicorn northgate internal pypi mirror fitzgerald sentry",
    },
    {
        "title": "Internal Meeting Notes — January 2025 — CS Dept",
        "url": "http://www.northgate-uni.edu/internal/meeting_notes_jan2025.txt",
        "domain": "www.northgate-uni.edu",
        "snippet": "All-staff meeting 30 Jan 2025. Infrastructure: Kubernetes migration, GitLab on-prem. Budget review. ACTION overdue: remove stale files from /uploads/. Tehrani mentioned internal GitLab URL on PostIt.",
        "filetype": "txt",
        "content": "meeting notes january 2025 northgate kubernetes gitlab infrastructure budget uploads stale files overdue tehrani postit internal",
    },
    {
        "title": "Research Groups — Northgate University CS",
        "url": "http://www.northgate-uni.edu/research.html",
        "domain": "www.northgate-uni.edu",
        "snippet": "CyberSec Lab (Dr. Novak), Distributed Systems Group (Prof. Whitmore), Software Quality Research Group (Dr. Tehrani). Publications and grant information.",
        "filetype": "html",
        "content": "research cybersec lab novak distributed systems whitmore software quality tehrani publications grants northgate",
    },

    # ── silvercompany.com ──────────────────────────────────────────────────
    {
        "title": "Silver Company GmbH — Precision Manufacturing, Frankfurt",
        "url": "http://www.silvercompany.com/",
        "domain": "www.silvercompany.com",
        "snippet": "Silver Company GmbH — precision engineering components, Frankfurt HQ. Contact: m.hale@silvercompany.com. Server: PHP/8.3.1, WordPress/6.4.2.",
        "filetype": "html",
        "content": "silver company precision manufacturing frankfurt hale voss orlov kimani php wordpress engineering components",
    },
    {
        "title": "robots.txt — Silver Company",
        "url": "http://www.silvercompany.com/robots.txt",
        "domain": "www.silvercompany.com",
        "snippet": "Disallow: /portal/ /internal/ /backup/ /admin/",
        "filetype": "txt",
        "content": "robots silvercompany disallow portal internal backup admin",
    },

    # ── bluefeather.com ───────────────────────────────────────────────────
    {
        "title": "Blue Feather Media Ltd — Digital PR Agency, London",
        "url": "http://www.bluefeather.com/",
        "domain": "www.bluefeather.com",
        "snippet": "Digital PR & content marketing agency based in London. Joomla! 4.3 platform. Company registration (England & Wales) in footer.",
        "filetype": "html",
        "content": "blue feather media pr agency london joomla digital content marketing",
    },
    {
        "title": "Staff Directory — Blue Feather Media (hidden page)",
        "url": "http://www.bluefeather.com/staff.html",
        "domain": "www.bluefeather.com",
        "snippet": "Full employee table with names, emails, departments, and social media links. Not linked from homepage — discovered via direct crawl.",
        "filetype": "html",
        "content": "staff directory bluefeather employees emails departments social media hidden",
    },
    {
        "title": "Blog — The Orlov Incident — Blue Feather Media",
        "url": "http://www.bluefeather.com/blog.html",
        "domain": "www.bluefeather.com",
        "snippet": "Agency blog post referencing Silver Company and 'the Orlov incident' — a cross-company PR crisis handled in 2024.",
        "filetype": "html",
        "content": "blog orlov incident silver company blue feather media crisis pr 2024",
    },

    # ── myblogspot.com ─────────────────────────────────────────────────────
    {
        "title": "Nikos Andreou — Travel Blog (Athens, Lisbon, Greek Islands)",
        "url": "http://www.myblogspot.com/",
        "domain": "www.myblogspot.com",
        "snippet": "Personal travel blog by Nikos Andreou, based in Athens. Posts cover Athens, Lisbon, and Greek islands. References PostIt social media profile.",
        "filetype": "html",
        "content": "nikos andreou travel blog athens lisbon greek islands myblogspot personal",
    },
    {
        "title": "[PDF] manifest.pdf — MyBlogSpot (hidden file)",
        "url": "http://www.myblogspot.com/static/manifest.pdf",
        "domain": "www.myblogspot.com",
        "snippet": "Hidden PDF file not linked from any page on myblogspot.com. Discovered via direct crawl of /static/ directory.",
        "filetype": "pdf",
        "content": "manifest pdf hidden static myblogspot radical content",
    },
]

# ──────────────────────────────────────────────
# Cache / archive snippets (for cache: operator)
# ──────────────────────────────────────────────
CACHE = {
    "www.northgate-uni.edu": {
        "snapshot_date": "12 March 2025",
        "title": "Department of Computer Science — Northgate University [CACHED]",
        "body": """
<p><em>This is a cached snapshot retrieved 12 March 2025.</em></p>
<p>The live version of this page may have changed.</p>
<hr>
<h3>Staff Phone Directory (removed from live site)</h3>
<p>This section was present in the March snapshot but has since been removed:</p>
<table border="1" cellpadding="6">
  <tr><th>Name</th><th>Direct Line</th><th>Mobile</th></tr>
  <tr><td>Prof. Alan Whitmore</td><td>+44 161 555 4201</td><td>+44 7700 900201</td></tr>
  <tr><td>Dr. Petra Novak</td><td>+44 161 555 4118</td><td>+44 7700 900118</td></tr>
  <tr><td>Dr. Reza Tehrani</td><td>+44 161 555 4207</td><td>+44 7700 900207</td></tr>
  <tr><td>Sophie Crane</td><td>+44 161 555 4100</td><td>—</td></tr>
  <tr><td>Owen Fitzgerald</td><td>+44 161 555 4099</td><td>+44 7700 900099</td></tr>
</table>
<p><small>Page last edited: 5 March 2025 by o.fitzgerald@northgate-uni.edu</small></p>
"""
    }
}

# ──────────────────────────────────────────────
# Query parser
# ──────────────────────────────────────────────
def parse_query(raw):
    ops = {"site": None, "filetype": None, "inurl": None, "intitle": None, "cache": None}
    terms = []
    for token in raw.strip().split():
        m = re.match(r'^(site|filetype|inurl|intitle|cache):(.+)$', token, re.IGNORECASE)
        if m:
            ops[m.group(1).lower()] = m.group(2).lower()
        else:
            terms.append(token.lower())
    return ops, terms

def match_result(entry, ops, terms):
    if ops["site"] and ops["site"] not in entry["domain"].lower():
        return False
    if ops["filetype"] and ops["filetype"] != entry.get("filetype", ""):
        return False
    if ops["inurl"] and ops["inurl"] not in entry["url"].lower():
        return False
    if ops["intitle"] and ops["intitle"] not in entry["title"].lower():
        return False
    if terms:
        haystack = (entry["title"] + " " + entry["snippet"] + " " + entry.get("content", "")).lower()
        if not all(t in haystack for t in terms):
            return False
    return True

# ──────────────────────────────────────────────
# HTML template
# ──────────────────────────────────────────────
BASE_STYLE = """
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #fff; color: #202124; }
  .topbar { display: flex; align-items: center; padding: 10px 24px; border-bottom: 1px solid #dfe1e5; gap: 20px; }
  .logo { font-size: 1.6rem; font-weight: bold; color: #4a90d9; letter-spacing: -1px; }
  .logo span { color: #e06c2f; }
  .search-wrap { flex: 1; max-width: 600px; }
  .search-wrap form { display: flex; }
  .search-wrap input[type=text] { flex: 1; padding: 8px 14px; border: 1px solid #dfe1e5; border-radius: 24px 0 0 24px; font-size: 0.95rem; outline: none; }
  .search-wrap input[type=text]:focus { border-color: #4a90d9; }
  .search-wrap button { padding: 8px 18px; background: #4a90d9; color: #fff; border: none; border-radius: 0 24px 24px 0; cursor: pointer; font-size: 0.9rem; }
  .tabs { padding: 4px 24px 0; border-bottom: 1px solid #dfe1e5; }
  .tabs a { display: inline-block; padding: 8px 14px; text-decoration: none; color: #555; font-size: 0.88rem; border-bottom: 3px solid transparent; }
  .tabs a.active { color: #4a90d9; border-bottom-color: #4a90d9; }
  .content { max-width: 700px; padding: 18px 24px; }
  .result-count { font-size: 0.82rem; color: #70757a; margin-bottom: 18px; }
  .result { margin-bottom: 26px; }
  .result .url { font-size: 0.78rem; color: #006621; margin-bottom: 2px; }
  .result .title a { font-size: 1.05rem; color: #1a0dab; text-decoration: none; }
  .result .title a:hover { text-decoration: underline; }
  .result .snippet { font-size: 0.88rem; color: #4d5156; margin-top: 4px; line-height: 1.5; }
  .result .ops { font-size: 0.78rem; color: #70757a; margin-top: 4px; }
  .result .ops a { color: #70757a; text-decoration: none; margin-right: 10px; }
  .result .ops a:hover { text-decoration: underline; }
  .no-results { color: #666; padding: 30px 0; }
  .home-center { text-align: center; padding: 80px 20px 30px; }
  .home-logo { font-size: 4rem; font-weight: bold; color: #4a90d9; letter-spacing: -2px; }
  .home-logo span { color: #e06c2f; }
  .home-form { margin-top: 24px; display: flex; justify-content: center; }
  .home-form input[type=text] { width: 500px; padding: 12px 18px; border: 1px solid #dfe1e5; border-radius: 24px 0 0 24px; font-size: 1rem; outline: none; }
  .home-form button { padding: 12px 22px; background: #4a90d9; color: #fff; border: none; border-radius: 0 24px 24px 0; cursor: pointer; font-size: 0.95rem; }
  .operators-hint { font-size: 0.78rem; color: #888; margin-top: 14px; }
  .operators-hint code { background: #f1f3f4; padding: 1px 5px; border-radius: 3px; }
  .cache-banner { background: #fff8e1; border: 1px solid #f9c74f; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px; font-size: 0.88rem; }
  .cache-content { background: #fafafa; border: 1px solid #ddd; padding: 20px; border-radius: 4px; font-size: 0.9rem; line-height: 1.6; }
  footer { text-align: center; padding: 20px; font-size: 0.78rem; color: #999; border-top: 1px solid #eee; margin-top: 40px; }
</style>
"""

HOME_TMPL = BASE_STYLE + """
<div class="home-center">
  <div class="home-logo">Search<span>ly</span></div>
  <div style="color:#888; font-size:0.9rem; margin-top:6px;">The web, indexed and searchable.</div>
  <div class="home-form">
    <form action="/search" method="get">
      <input type="text" name="q" placeholder="Search or use operators: site:, filetype:, inurl:, intitle:, cache:" autofocus>
      <button type="submit">Search</button>
    </form>
  </div>
  <div class="operators-hint">
    Supported operators:
    <code>site:northgate-uni.edu</code>
    <code>filetype:pdf</code>
    <code>inurl:uploads</code>
    <code>intitle:budget</code>
    <code>cache:www.northgate-uni.edu</code>
  </div>
</div>
<footer>Searchly — Simulated Search Engine &nbsp;|&nbsp; For educational use only</footer>
"""

RESULTS_TMPL = BASE_STYLE + """
<div class="topbar">
  <div class="logo">Search<span>ly</span></div>
  <div class="search-wrap">
    <form action="/search" method="get">
      <input type="text" name="q" value="{{ query|e }}" autofocus>
      <button type="submit">&#128269;</button>
    </form>
  </div>
</div>
<div class="tabs">
  <a href="/search?q={{ query|urlencode }}" class="active">All</a>
</div>
<div class="content">
  <div class="result-count">About {{ count }} result(s) for <strong>{{ query|e }}</strong></div>
  {% if results %}
    {% for r in results %}
    <div class="result">
      <div class="url">{{ r.url }}</div>
      <div class="title"><a href="{{ r.url }}" target="_blank">{{ r.title }}</a></div>
      <div class="snippet">{{ r.snippet }}</div>
      <div class="ops">
        <a href="/search?q=cache:{{ r.domain }}">Cached</a>
        <a href="/search?q=site:{{ r.domain }}">More from {{ r.domain }}</a>
      </div>
    </div>
    {% endfor %}
  {% else %}
    <div class="no-results">
      <p>No results found for <strong>{{ query|e }}</strong>.</p>
      <p style="margin-top:10px; font-size:0.85rem; color:#888">Try different keywords or operators: <code>site:</code>, <code>filetype:</code>, <code>inurl:</code>, <code>intitle:</code></p>
    </div>
  {% endif %}
</div>
<footer>Searchly — Simulated Search Engine &nbsp;|&nbsp; For educational use only</footer>
"""

CACHE_TMPL = BASE_STYLE + """
<div class="topbar">
  <div class="logo">Search<span>ly</span></div>
  <div class="search-wrap">
    <form action="/search" method="get">
      <input type="text" name="q" value="{{ query|e }}">
      <button type="submit">&#128269;</button>
    </form>
  </div>
</div>
<div class="content" style="max-width:800px">
  <div class="cache-banner">
    <strong>&#128190; Cached snapshot</strong> of <code>{{ domain }}</code> retrieved on <strong>{{ date }}</strong>.
    The live version may have changed. <a href="http://{{ domain }}/" target="_blank">View live page →</a>
  </div>
  <h2 style="font-size:1.1rem; margin-bottom:12px; color:#1a3a5c">{{ title }}</h2>
  <div class="cache-content">{{ body|safe }}</div>
</div>
<footer>Searchly — Simulated Search Engine &nbsp;|&nbsp; For educational use only</footer>
"""

# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.route("/")
def home():
    return render_template_string(HOME_TMPL)

@app.route("/search")
def search():
    raw = request.args.get("q", "").strip()
    if not raw:
        return home()

    ops, terms = parse_query(raw)

    # Handle cache: operator
    if ops["cache"]:
        domain = ops["cache"]
        snap = CACHE.get(domain)
        if snap:
            return render_template_string(
                CACHE_TMPL,
                query=raw,
                domain=domain,
                date=snap["snapshot_date"],
                title=snap["title"],
                body=snap["body"]
            )
        else:
            # No cache for this domain
            results = []
            return render_template_string(
                RESULTS_TMPL,
                query=raw,
                results=results,
                count=0
            )

    results = [e for e in INDEX if match_result(e, ops, terms)]
    return render_template_string(
        RESULTS_TMPL,
        query=raw,
        results=results,
        count=len(results)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=False)
