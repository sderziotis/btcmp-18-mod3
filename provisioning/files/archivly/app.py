#!/usr/bin/env python3
"""
Archivly — Simulated Web Archive for OSINT Module 2
Stores timestamped snapshots of lab domains.
"""

from flask import Flask, request, render_template_string, abort
import re

app = Flask(__name__)

# ──────────────────────────────────────────────
# Archive snapshot catalogue
# ──────────────────────────────────────────────
SNAPSHOTS = {
    "www.northgate-uni.edu": [
        {"id": "20250312120000", "label": "12 Mar 2025, 12:00 UTC", "note": "Phone directory still present"},
        {"id": "20250101090000", "label": "1 Jan 2025, 09:00 UTC", "note": "Staff page includes visiting researchers"},
        {"id": "20241015140000", "label": "15 Oct 2024, 14:00 UTC", "note": "Older tech stack (Django 3.2)"},
    ],
    "www.silvercompany.com": [
        {"id": "20250201080000", "label": "1 Feb 2025, 08:00 UTC", "note": "Full staff listing including D. Orlov"},
    ],
    "www.bluefeather.com": [
        {"id": "20250310100000", "label": "10 Mar 2025, 10:00 UTC", "note": "Blog post mentions Silver Company"},
    ],
}

SNAPSHOT_CONTENT = {
    "www.northgate-uni.edu__20250312120000": {
        "title": "Department of Computer Science — Northgate University [Archive: 12 Mar 2025]",
        "html": """
<div style="background:#1a3a5c;color:#fff;padding:14px 24px;font-family:sans-serif">
  <strong>Northgate University — Department of Computer Science</strong>
</div>
<div style="padding:20px 24px; font-family:Georgia,serif; max-width:860px">
  <h2 style="color:#1a3a5c">Welcome to the CS Department</h2>
  <p>Research and teaching in AI, cybersecurity, distributed systems, and software engineering.</p>

  <h3 style="color:#1a3a5c; margin-top:24px">Staff Phone Directory</h3>
  <p style="font-size:0.85rem;color:#c00"><strong>Note:</strong> This section was removed from the live site after 12 March 2025.</p>
  <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;font-size:0.9rem;width:100%">
    <tr style="background:#254e7a;color:#fff">
      <th>Name</th><th>Role</th><th>Direct Line</th><th>Mobile</th><th>Email</th>
    </tr>
    <tr><td>Prof. Alan Whitmore</td><td>HoD</td><td>+44 161 555 4201</td><td>+44 7700 900201</td><td>a.whitmore@northgate-uni.edu</td></tr>
    <tr style="background:#f5f5f5"><td>Dr. Petra Novak</td><td>Senior Lecturer</td><td>+44 161 555 4118</td><td>+44 7700 900118</td><td>p.novak@northgate-uni.edu</td></tr>
    <tr><td>Dr. Reza Tehrani</td><td>Lecturer</td><td>+44 161 555 4207</td><td>+44 7700 900207</td><td>r.tehrani@northgate-uni.edu</td></tr>
    <tr style="background:#f5f5f5"><td>Ms. Sophie Crane</td><td>Admin</td><td>+44 161 555 4100</td><td>—</td><td>s.crane@northgate-uni.edu</td></tr>
    <tr><td>Mr. Owen Fitzgerald</td><td>SysAdmin</td><td>+44 161 555 4099</td><td>+44 7700 900099</td><td>o.fitzgerald@northgate-uni.edu</td></tr>
  </table>

  <h3 style="color:#1a3a5c; margin-top:24px">Technologies</h3>
  <p>Django 4.2 | PostgreSQL | Redis | Docker | Kubernetes | GitLab CI | Ansible | Ubuntu 24.04</p>
  <p style="font-size:0.82rem;color:#777">Internal developer portal: <code>portal.northgate-uni.edu</code> (VPN required)</p>

  <p style="font-size:0.78rem;color:#999;margin-top:20px">Page last edited: 5 March 2025 by o.fitzgerald@northgate-uni.edu</p>
</div>
"""
    },
    "www.northgate-uni.edu__20250101090000": {
        "title": "Department of Computer Science — Northgate University [Archive: 1 Jan 2025]",
        "html": """
<div style="background:#1a3a5c;color:#fff;padding:14px 24px;font-family:sans-serif">
  <strong>Northgate University — Department of Computer Science</strong>
</div>
<div style="padding:20px 24px;font-family:Georgia,serif;max-width:860px">
  <h2 style="color:#1a3a5c">Welcome to the CS Department</h2>
  <p>Staff listed as of January 2025. Visiting researchers for the current academic year:</p>
  <ul>
    <li>Yuki Matsuda (PhD Student) — y.matsuda@northgate-uni.edu</li>
    <li>Carlos Ibáñez (Research Associate) — c.ibanez@northgate-uni.edu</li>
  </ul>
  <p>Full permanent staff: Whitmore, Novak, Tehrani, Crane, Fitzgerald.</p>
</div>
"""
    },
    "www.northgate-uni.edu__20241015140000": {
        "title": "Department of Computer Science — Northgate University [Archive: Oct 2024]",
        "html": """
<div style="background:#1a3a5c;color:#fff;padding:14px 24px;font-family:sans-serif">
  <strong>Northgate University — Department of Computer Science</strong>
</div>
<div style="padding:20px 24px;font-family:Georgia,serif;max-width:860px">
  <h2 style="color:#1a3a5c">Welcome to the CS Department</h2>
  <p>Technology stack (October 2024): Django 3.2, PostgreSQL 14, Redis 6, Docker 20.10, Ansible 2.14.</p>
  <p>Upgrade to Django 4.2 and Kubernetes scheduled for December 2024.</p>
  <p>Research cluster running Ubuntu 22.04 LTS. Migration to 24.04 LTS planned.</p>
</div>
"""
    },
    "www.silvercompany.com__20250201080000": {
        "title": "Silver Company GmbH [Archive: 1 Feb 2025]",
        "html": """
<div style="background:#555;color:#fff;padding:14px 24px;font-family:sans-serif">
  <strong>Silver Company GmbH — Precision Manufacturing</strong>
</div>
<div style="padding:20px 24px;font-family:Arial,sans-serif;max-width:860px">
  <h2>Our Team</h2>
  <ul>
    <li>Marcus Hale — CEO (m.hale@silvercompany.com)</li>
    <li>Elena Voss — CTO (e.voss@silvercompany.com)</li>
    <li><strong>Dmitri Orlov</strong> — Head of Security (d.orlov@silvercompany.com) <em>[no longer listed on live site]</em></li>
    <li>Sara Kimani — Operations (s.kimani@silvercompany.com)</li>
  </ul>
</div>
"""
    },
    "www.bluefeather.com__20250310100000": {
        "title": "Blue Feather Media — Agency Blog [Archive: 10 Mar 2025]",
        "html": """
<div style="background:#2c3e50;color:#fff;padding:14px 24px;font-family:sans-serif">
  <strong>Blue Feather Media Ltd — Blog</strong>
</div>
<div style="padding:20px 24px;font-family:Arial,sans-serif;max-width:860px">
  <h2>Managing the Orlov Incident: A PR Case Study</h2>
  <p style="color:#888;font-size:0.85rem">Published 8 March 2025</p>
  <p>In late 2024, our team was engaged by a Frankfurt-based manufacturing client (Silver Company GmbH)
  to manage fallout from the departure of their Head of Security, following allegations of data misuse.
  The individual, referred to internally as "the Orlov case", had been active on multiple social platforms.</p>
  <p>This post outlines our crisis communication methodology — rapid profile monitoring,
  coordinated statement release, and stakeholder briefing.</p>
</div>
"""
    },
}

# ──────────────────────────────────────────────
BASE_STYLE = """
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #1a1a2e; color: #e0e0e0; }
  .topbar { display: flex; align-items: center; padding: 12px 24px; background: #16213e; border-bottom: 1px solid #0f3460; gap: 20px; }
  .logo { font-size: 1.4rem; font-weight: bold; color: #e94560; letter-spacing: -0.5px; }
  .logo span { color: #f5a623; }
  .search-wrap { flex: 1; max-width: 580px; }
  .search-wrap form { display: flex; }
  .search-wrap input[type=text] { flex: 1; padding: 7px 13px; background: #0f3460; color: #e0e0e0; border: 1px solid #0f3460; border-radius: 20px 0 0 20px; font-size: 0.9rem; outline: none; }
  .search-wrap button { padding: 7px 16px; background: #e94560; color: #fff; border: none; border-radius: 0 20px 20px 0; cursor: pointer; font-size: 0.88rem; }
  .content { max-width: 800px; padding: 20px 24px; }
  h2 { color: #f5a623; font-size: 1.1rem; margin-bottom: 16px; }
  .domain-block { background: #16213e; border: 1px solid #0f3460; border-radius: 6px; margin-bottom: 16px; padding: 16px; }
  .domain-block h3 { color: #e94560; font-size: 0.95rem; margin-bottom: 10px; }
  .snapshot-row { display: flex; align-items: center; gap: 14px; padding: 8px 0; border-bottom: 1px solid #0f3460; font-size: 0.88rem; }
  .snapshot-row:last-child { border-bottom: none; }
  .snapshot-row .ts { color: #aaa; min-width: 220px; }
  .snapshot-row .note { color: #ccc; flex: 1; font-size: 0.82rem; }
  .snapshot-row a { color: #f5a623; text-decoration: none; white-space: nowrap; }
  .snapshot-row a:hover { text-decoration: underline; }
  .home-intro { padding: 40px 24px 10px; max-width: 700px; }
  .home-intro .big-logo { font-size: 3rem; font-weight: bold; color: #e94560; }
  .home-intro .big-logo span { color: #f5a623; }
  .home-intro .sub { color: #aaa; margin-top: 6px; font-size: 0.9rem; }
  .home-form { margin-top: 20px; display: flex; gap: 10px; }
  .home-form input { flex: 1; max-width: 500px; padding: 10px 16px; background: #0f3460; color: #e0e0e0; border: 1px solid #0f3460; border-radius: 20px 0 0 20px; font-size: 0.95rem; outline: none; }
  .home-form button { padding: 10px 20px; background: #e94560; color: #fff; border: none; border-radius: 0 20px 20px 0; cursor: pointer; }
  .view-banner { background: #0f3460; border: 1px solid #e94560; border-radius: 6px; padding: 12px 16px; margin-bottom: 20px; font-size: 0.85rem; color: #ccc; }
  .view-banner strong { color: #f5a623; }
  .archived-content { background: #fff; color: #222; border-radius: 6px; overflow: hidden; }
  footer { text-align: center; padding: 20px; font-size: 0.78rem; color: #555; border-top: 1px solid #0f3460; margin-top: 40px; }
</style>
"""

HOME_TMPL = BASE_STYLE + """
<div class="home-intro">
  <div class="big-logo">Archiv<span>ly</span></div>
  <div class="sub">Browse cached snapshots of indexed websites.</div>
  <div class="home-form">
    <form action="/browse" method="get">
      <input type="text" name="domain" placeholder="Enter domain, e.g. www.northgate-uni.edu" autofocus>
      <button type="submit">Browse</button>
    </form>
  </div>
</div>
<div class="content">
  <h2>Available Archives</h2>
  {% for domain, snaps in snapshots.items() %}
  <div class="domain-block">
    <h3>{{ domain }} <span style="font-size:0.78rem;color:#aaa">({{ snaps|length }} snapshot{{ 's' if snaps|length != 1 else '' }})</span></h3>
    {% for s in snaps %}
    <div class="snapshot-row">
      <span class="ts">{{ s.label }}</span>
      <span class="note">{{ s.note }}</span>
      <a href="/view/{{ domain }}/{{ s.id }}">View snapshot →</a>
    </div>
    {% endfor %}
  </div>
  {% endfor %}
</div>
<footer>Archivly — Simulated Web Archive &nbsp;|&nbsp; For educational use only</footer>
"""

VIEW_TMPL = BASE_STYLE + """
<div class="topbar">
  <div class="logo">Archiv<span>ly</span></div>
  <div class="search-wrap">
    <form action="/browse" method="get">
      <input type="text" name="domain" placeholder="Enter domain..." value="{{ domain|e }}">
      <button type="submit">Browse</button>
    </form>
  </div>
</div>
<div class="content" style="max-width:900px">
  <div class="view-banner">
    <strong>Archived snapshot</strong> of <code>{{ domain }}</code> &nbsp;|&nbsp;
    Captured: <strong>{{ label }}</strong> &nbsp;|&nbsp;
    <a href="/" style="color:#f5a623">← All archives</a>
  </div>
  <div class="archived-content">{{ html|safe }}</div>
</div>
<footer>Archivly — Simulated Web Archive &nbsp;|&nbsp; For educational use only</footer>
"""

@app.route("/")
def home():
    return render_template_string(HOME_TMPL, snapshots=SNAPSHOTS)

@app.route("/browse")
def browse():
    domain = request.args.get("domain", "").strip()
    snaps = SNAPSHOTS.get(domain, [])
    if not snaps:
        return render_template_string(
            HOME_TMPL + "<div class='content'><p style='color:#e94560'>No snapshots found for <strong>" + domain + "</strong>.</p></div>",
            snapshots=SNAPSHOTS
        )
    return render_template_string(HOME_TMPL, snapshots={domain: snaps})

@app.route("/view/<path:domain>/<snap_id>")
def view_snap(domain, snap_id):
    key = f"{domain}__{snap_id}"
    snap_meta = next(
        (s for s in SNAPSHOTS.get(domain, []) if s["id"] == snap_id),
        None
    )
    content = SNAPSHOT_CONTENT.get(key)
    if not content or not snap_meta:
        abort(404)
    return render_template_string(
        VIEW_TMPL,
        domain=domain,
        label=snap_meta["label"],
        html=content["html"]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=False)
