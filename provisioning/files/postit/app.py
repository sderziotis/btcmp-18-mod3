from flask import Flask, render_template_string, abort, send_from_directory
import os

app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# ── Fake persona data ──────────────────────────────────────────────────────────
USERS = {
  "nina.cross": {
    "display": "Nina Cross", "handle": "nina.cross",
    "avatar": "NC", "color": "#7c3aed",
    "bio": "Founder @BlueFeatherMedia | PR, digital strategy, brand | London 🇬🇧 | She/her",
    "location": "London, UK", "joined": "January 2017",
    "following": 1203, "followers": 8844,
    "posts": [
      {"id":"nc1","text":"Big news coming from @BlueFeatherMedia next week. Let's just say a major manufacturing brand is about to get a serious social media glow-up 👀","ts":"2024-03-13 10:00","likes":210,"reposts":55,"comments":23,"image":None},
      {"id":"nc2","text":"The Orlov data story is a reminder: your execs' public posts ARE your attack surface. We run social OSINT audits for all new clients now. DM me.","ts":"2024-02-01 09:15","likes":433,"reposts":189,"comments":67,"image":None},
      {"id":"nc3","text":"Hot take: your company's robots.txt file is a roadmap for attackers. Hide your /admin and /backup paths BEFORE you launch. #infosec #pr","ts":"2024-01-22 15:30","likes":611,"reposts":244,"comments":88,"image":None}
    ]
  },
  "alexei.romanov": {
    "display": "Alexei Romanov", "handle": "alexei.romanov",
    "avatar": "AR", "color": "#0e7490",
    "bio": "Head of Digital @BlueFeatherMedia | Dev, data, automation | Remote 🌍 | a.romanov@bluefeather.com",
    "location": "Remote (Lisbon, PT)", "joined": "September 2019",
    "following": 567, "followers": 1788,
    "posts": [
      {"id":"ar1","text":"Rebuilt the social scheduler from scratch. Python + SQLite, runs on a single VPS. Zero cloud costs. Sometimes simple is better.","ts":"2024-03-09 20:00","likes":145,"reposts":44,"comments":19,"image":None},
      {"id":"ar2","text":"PSA: rotating your API keys every 90 days is pointless if you're committing them to a public repo first. Ask me how I know 😬","ts":"2024-02-12 09:20","likes":892,"reposts":341,"comments":103,"image":None},
      {"id":"ar3","text":"Just found an exposed .git directory on a client's staging site. Not ours thankfully. Always check /.git/config before you go live people.","ts":"2024-01-30 14:15","likes":567,"reposts":198,"comments":55,"image":None}
    ]
  },
  "tom.bekele": {
    "display": "Tom Bekele", "handle": "tom.bekele",
    "avatar": "TB", "color": "#b45309",
    "bio": "Social Media Manager @BlueFeatherMedia | Content, analytics, vibes ✌️ | London",
    "location": "London, UK", "joined": "April 2021",
    "following": 882, "followers": 3241,
    "posts": [
      {"id":"tb1","text":"Managing a manufacturing brand's PostIt this month. If you see unusually polished content from a factory, that's me 😄 #socialmediamanager","ts":"2024-03-14 12:30","likes":176,"reposts":28,"comments":14,"image":None},
      {"id":"tb2","text":"PostIt engagement tip: post between 11am-1pm Tuesday through Thursday. Algorithm loves it right now. You're welcome.","ts":"2024-03-07 11:05","likes":302,"reposts":111,"comments":37,"image":None},
      {"id":"tb3","text":"Wrapping a big content campaign for a client. 3 weeks of work, 4 posts. The client loved them. That's the job 🙂","ts":"2024-02-20 09:30","likes":98,"reposts":7,"comments":11,"image":None}
    ]
  },
  "marco.villa": {
    "display": "Marco Villa", "handle": "marco.villa",
    "avatar": "MV", "color": "#be185d",
    "bio": "Journalist & blogger | Tech, culture, travel | Rome 🇮🇹 | marco@postit.com",
    "location": "Rome, Italy", "joined": "March 2018",
    "following": 920, "followers": 6120,
    "posts": [
      {"id":"mv1","text":"Why every tech company should have a communications strategy BEFORE they get hacked, not after. New piece out now. Link in bio. #pr #infosec","ts":"2024-03-12 08:00","likes":341,"reposts":122,"comments":44,"image":None},
      {"id":"mv2","text":"Interviewed three CISOs this week. All three said the same thing: humans are the weakest link. Stop blaming the firewall.","ts":"2024-03-05 14:20","likes":289,"reposts":98,"comments":33,"image":None},
      {"id":"mv3","text":"Favorite thing about working remotely from different cities: every coffee shop is a new office. Today's office: Trastevere ☕","ts":"2024-02-22 10:05","likes":177,"reposts":21,"comments":28,"image":None}
    ]
  },
  "petra.novak": {
    "display": "Petra Novak", "handle": "petra.novak",
    "avatar": "PN", "color": "#065f46",
    "bio": "Content strategist | PostIt contributor | Prague 🇨🇿 | she/her",
    "location": "Prague, Czech Republic", "joined": "October 2020",
    "following": 430, "followers": 1540,
    "posts": [
      {"id":"pn1","text":"The brands that win on PostIt aren't the ones that post the most. They're the ones that post with intention. Quality > quantity. Always.","ts":"2024-03-10 11:30","likes":214,"reposts":87,"comments":19,"image":None},
      {"id":"pn2","text":"Working on a content audit for a new client. Found 4 years of posts with no strategy behind them. This is more common than you think.","ts":"2024-02-28 13:45","likes":98,"reposts":34,"comments":12,"image":None},
      {"id":"pn3","text":"Prague in spring > everywhere else. Controversial? Maybe. Correct? Absolutely 🌸","ts":"2024-02-15 17:00","likes":321,"reposts":42,"comments":55,"image":None}
    ]
  },
  "johnyskinny": {
    "display": "Johny Skinny", "handle": "johnyskinny",
    "avatar": "JS", "color": "#1d4ed8",
    "bio": "Beach life, cold beers, good music 🍺🌊 | Athens, Greece",
    "location": "Athens, Greece", "joined": "May 2022",
    "following": 97, "followers": 238,
    "posts": [
      {"id":"js1","text":"Beach day with the boys 🍺🌊 Sun is out, beers are cold, life is good. This is what weekends are for. #beach #athens #summer","ts":"2024-03-17 16:20","likes":61,"reposts":4,"comments":9,"image":"/static/johnyskinny_beach.jpg"},
      {"id":"js2","text":"That post-beach tiredness where you can't tell if you slept or just blinked for 2 hours 😂","ts":"2024-03-17 21:05","likes":48,"reposts":2,"comments":6,"image":None},
      {"id":"js3","text":"Varkiza or Vouliagmeni? Big debate with the crew today. Drop your vote 👇","ts":"2024-03-08 13:10","likes":33,"reposts":1,"comments":14,"image":None}
    ]
  }
}

# ── Timeline: merged & sorted posts ───────────────────────────────────────────
def get_timeline():
  all_posts = []
  for handle, user in USERS.items():
    for p in user["posts"]:
      all_posts.append({**p, "author": user["display"], "handle": handle,
                         "avatar": user["avatar"], "color": user["color"]})
  return sorted(all_posts, key=lambda x: x["ts"], reverse=True)

# ── Base template ──────────────────────────────────────────────────────────────
BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} — PostIt</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Segoe UI',Arial,sans-serif;background:#fdf4ff;color:#1e1b2e}
    a{text-decoration:none;color:inherit}
    .topbar{background:#6d28d9;color:#fff;padding:0 24px;display:flex;align-items:center;height:56px;position:sticky;top:0;z-index:100;box-shadow:0 2px 8px rgba(109,40,217,0.35)}
    .topbar .logo{font-size:1.7rem;font-weight:800;letter-spacing:-1px;margin-right:32px}
    .topbar .logo span{color:#c4b5fd}
    .topbar nav a{color:#fff;margin-right:18px;font-size:0.92rem;opacity:0.88}
    .topbar nav a:hover{opacity:1;text-decoration:underline}
    .topbar .search{background:rgba(255,255,255,0.18);border:none;border-radius:20px;padding:6px 16px;color:#fff;font-size:0.9rem;width:200px}
    .topbar .search::placeholder{color:#ddd6fe}
    .layout{max-width:1100px;margin:28px auto;display:grid;grid-template-columns:260px 1fr 280px;gap:20px;padding:0 12px}
    .sidebar-card{background:#fff;border-radius:10px;padding:18px;margin-bottom:14px;box-shadow:0 1px 4px rgba(109,40,217,0.08);border:1px solid #ede9fe}
    .sidebar-card h4{font-size:0.83rem;color:#7c3aed;text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px}
    .user-pill{display:flex;align-items:center;gap:10px;margin-bottom:10px;cursor:pointer}
    .user-pill:hover .uname{text-decoration:underline;color:#7c3aed}
    .avatar{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:0.85rem;flex-shrink:0}
    .uname{font-weight:600;font-size:0.92rem}
    .uhandle{font-size:0.78rem;color:#a78bfa}
    .post-card{background:#fff;border-radius:10px;padding:18px;margin-bottom:14px;box-shadow:0 1px 4px rgba(109,40,217,0.08);border:1px solid #ede9fe}
    .post-header{display:flex;align-items:center;gap:12px;margin-bottom:10px}
    .post-meta{flex:1}
    .post-meta .name{font-weight:700;font-size:0.95rem}
    .post-meta .handle{font-size:0.8rem;color:#a78bfa}
    .post-meta .ts{font-size:0.78rem;color:#c4b5fd;margin-left:6px}
    .post-body{font-size:0.95rem;line-height:1.55;margin-bottom:12px}
    .post-img{width:100%;max-height:340px;object-fit:cover;border-radius:8px;margin-bottom:12px}
    .post-actions{display:flex;gap:22px;font-size:0.82rem;color:#a78bfa}
    .post-actions span{cursor:pointer}
    .post-actions span:hover{color:#7c3aed}
    .profile-hero{background:#fff;border-radius:10px;overflow:hidden;margin-bottom:14px;box-shadow:0 1px 4px rgba(109,40,217,0.08);border:1px solid #ede9fe}
    .profile-banner{height:120px;background:linear-gradient(135deg,#6d28d9,#a78bfa)}
    .profile-info{padding:16px 20px 20px}
    .profile-avatar{width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:1.4rem;margin-top:-36px;border:3px solid #fff}
    .profile-info h2{margin-top:8px;font-size:1.2rem}
    .profile-info .bio{font-size:0.88rem;color:#555;margin:4px 0 8px}
    .profile-info .meta{font-size:0.82rem;color:#a78bfa;margin-bottom:6px}
    .profile-stats{display:flex;gap:20px;font-size:0.88rem}
    .profile-stats span strong{color:#1e1b2e}
    .trending-item{margin-bottom:10px;font-size:0.88rem}
    .trending-item .tag{color:#7c3aed;font-weight:600}
    .trending-item .count{color:#c4b5fd;font-size:0.78rem}
  </style>
</head>
<body>
<div class="topbar">
  <a href="/" class="logo">Post<span>It</span></a>
  <nav>
    <a href="/">Home</a>
    <a href="/people">People</a>
    <a href="/trending">Trending</a>
  </nav>
  <input class="search" placeholder="Search PostIt…">
</div>
{% block content %}{% endblock %}
</body>
</html>
"""

HOME_TMPL = BASE.replace("{% block content %}{% endblock %}", """
<div class="layout">
  <div class="left-col">
    <div class="sidebar-card">
      <h4>Who to follow</h4>
      {% for handle, u in users.items() %}
      <a href="/profile/{{ handle }}" class="user-pill">
        <div class="avatar" style="background:{{ u.color }}">{{ u.avatar }}</div>
        <div><div class="uname">{{ u.display }}</div><div class="uhandle">@{{ u.handle }}</div></div>
      </a>
      {% endfor %}
    </div>
  </div>
  <div class="feed">
    {% for post in timeline %}
    <div class="post-card">
      <div class="post-header">
        <a href="/profile/{{ post.handle }}"><div class="avatar" style="background:{{ post.color }}">{{ post.avatar }}</div></a>
        <div class="post-meta">
          <a href="/profile/{{ post.handle }}"><span class="name">{{ post.author }}</span></a>
          <span class="handle">@{{ post.handle }}</span>
          <span class="ts">· {{ post.ts }}</span>
        </div>
      </div>
      <div class="post-body">{{ post.text }}</div>
      {% if post.image %}<img class="post-img" src="{{ post.image }}" alt="post image">{% endif %}
      <div class="post-actions">
        <span>&#128172; {{ post.comments }}</span>
        <span>&#128257; {{ post.reposts }}</span>
        <span>&#10084; {{ post.likes }}</span>
      </div>
    </div>
    {% endfor %}
  </div>
  <div class="right-col">
    <div class="sidebar-card">
      <h4>Trending</h4>
      <div class="trending-item"><div class="tag">#pr</div><div class="count">201 posts</div></div>
      <div class="trending-item"><div class="tag">#infosec</div><div class="count">134 posts</div></div>
      <div class="trending-item"><div class="tag">#digitalstrategy</div><div class="count">98 posts</div></div>
      <div class="trending-item"><div class="tag">#beach</div><div class="count">72 posts</div></div>
      <div class="trending-item"><div class="tag">#content</div><div class="count">61 posts</div></div>
      <div class="trending-item"><div class="tag">#summer</div><div class="count">55 posts</div></div>
    </div>
  </div>
</div>
""")

PROFILE_TMPL = BASE.replace("{% block content %}{% endblock %}", """
<div class="layout">
  <div class="left-col">
    <div class="sidebar-card">
      <h4>People</h4>
      {% for handle, u in users.items() %}
      <a href="/profile/{{ handle }}" class="user-pill">
        <div class="avatar" style="background:{{ u.color }}">{{ u.avatar }}</div>
        <div><div class="uname">{{ u.display }}</div><div class="uhandle">@{{ u.handle }}</div></div>
      </a>
      {% endfor %}
    </div>
  </div>
  <div class="feed">
    <div class="profile-hero">
      <div class="profile-banner"></div>
      <div class="profile-info">
        <div class="profile-avatar" style="background:{{ user.color }}">{{ user.avatar }}</div>
        <h2>{{ user.display }}</h2>
        <div class="bio">{{ user.bio }}</div>
        <div class="meta">📍 {{ user.location }} &nbsp;·&nbsp; Joined {{ user.joined }}</div>
        <div class="profile-stats">
          <span><strong>{{ user.following }}</strong> Following</span>
          <span><strong>{{ user.followers }}</strong> Followers</span>
        </div>
      </div>
    </div>
    {% for post in posts %}
    <div class="post-card">
      <div class="post-header">
        <div class="avatar" style="background:{{ user.color }}">{{ user.avatar }}</div>
        <div class="post-meta">
          <span class="name">{{ user.display }}</span>
          <span class="handle">@{{ user.handle }}</span>
          <span class="ts">· {{ post.ts }}</span>
        </div>
      </div>
      <div class="post-body">{{ post.text }}</div>
      {% if post.image %}<img class="post-img" src="{{ post.image }}" alt="post image">{% endif %}
      <div class="post-actions">
        <span>&#128172; {{ post.comments }}</span>
        <span>&#128257; {{ post.reposts }}</span>
        <span>&#10084; {{ post.likes }}</span>
      </div>
    </div>
    {% endfor %}
  </div>
  <div class="right-col"></div>
</div>
""")

PEOPLE_TMPL = BASE.replace("{% block content %}{% endblock %}", """
<div style="max-width:860px;margin:28px auto;padding:0 12px">
  <h2 style="margin-bottom:18px;color:#6d28d9">People on PostIt</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px">
    {% for handle, u in users.items() %}
    <a href="/profile/{{ handle }}" style="display:block">
      <div class="sidebar-card" style="display:flex;align-items:center;gap:14px;cursor:pointer">
        <div class="avatar" style="background:{{ u.color }};width:52px;height:52px;font-size:1.1rem">{{ u.avatar }}</div>
        <div>
          <div style="font-weight:700">{{ u.display }}</div>
          <div style="font-size:0.8rem;color:#a78bfa">@{{ u.handle }}</div>
          <div style="font-size:0.78rem;color:#c4b5fd;margin-top:4px">{{ u.followers }} followers</div>
        </div>
      </div>
    </a>
    {% endfor %}
  </div>
</div>
""")

@app.route("/static/<path:filename>")
def static_files(filename):
  return send_from_directory(STATIC_DIR, filename)

@app.route("/")
def home():
  return render_template_string(HOME_TMPL, title="Home", users=USERS, timeline=get_timeline())

@app.route("/people")
def people():
  return render_template_string(PEOPLE_TMPL, title="People", users=USERS)

@app.route("/profile/<handle>")
def profile(handle):
  user = USERS.get(handle)
  if not user:
    abort(404)
  return render_template_string(PROFILE_TMPL, title=user["display"], user=user,
                                 users=USERS, posts=user["posts"])

@app.route("/trending")
def trending():
  return home()

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5001)
