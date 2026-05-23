from flask import Flask, render_template_string, abort, send_from_directory
import os

app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# ── Fake persona data ──────────────────────────────────────────────────────────
USERS = {
  "marcus.hale": {
    "display": "Marcus Hale", "handle": "marcus.hale",
    "avatar": "MH", "color": "#1a2e44",
    "bio": "CEO @SilverCompany | Aerospace & Manufacturing | Frankfurt 🇩🇪 | m.hale@silvercompany.com",
    "location": "Frankfurt, Germany", "joined": "March 2019",
    "following": 312, "followers": 4821,
    "posts": [
      {"id":"mh1","text":"Proud to announce Silver Company's expansion into the Greek market. Signing ceremony next Thursday in Athens. Big week ahead! #manufacturing #expansion","ts":"2024-03-15 09:41","likes":87,"reposts":14,"comments":6,"image":None},
      {"id":"mh2","text":"Great meeting with @elena.voss and the R&D team today. The Q3 prototype is ahead of schedule. Can't say more yet 👀 #aerospace","ts":"2024-03-10 16:22","likes":54,"reposts":9,"comments":3,"image":None},
      {"id":"mh3","text":"If you're not using Ansible for infra automation in 2024 you're leaving money on the table. Simple as that.","ts":"2024-02-28 11:05","likes":120,"reposts":33,"comments":18,"image":None},
      {"id":"mh4","text":"Coffee with @nina.cross from @BlueFeatherMedia — excited about the new comms strategy they're putting together for us.","ts":"2024-02-14 08:30","likes":41,"reposts":5,"comments":2,"image":None}
    ]
  },
  "elena.voss": {
    "display": "Elena Voss", "handle": "elena.voss",
    "avatar": "EV", "color": "#2e6da4",
    "bio": "CTO @SilverCompany | Embedded systems, robotics, defense tech | Warsaw 🇵🇱 | e.voss@silvercompany.com",
    "location": "Warsaw, Poland", "joined": "July 2020",
    "following": 198, "followers": 2103,
    "posts": [
      {"id":"ev1","text":"Just pushed the v2.4 firmware to staging. FreeRTOS + STM32 combo is rock solid this iteration. Shoutout to the Warsaw team 🔥","ts":"2024-03-12 21:14","likes":66,"reposts":11,"comments":4,"image":None},
      {"id":"ev2","text":"Reminder: company VPN policy updated. ALL remote connections must go through the Frankfurt gateway from April 1st. Check your config files. #security","ts":"2024-03-08 10:00","likes":29,"reposts":47,"comments":12,"image":None},
      {"id":"ev3","text":"Interview tip: if you don't know what a race condition is, please don't apply for senior embedded roles 🙂","ts":"2024-02-20 13:45","likes":234,"reposts":78,"comments":41,"image":None}
    ]
  },
  "dmitri.orlov": {
    "display": "Dmitri Orlov", "handle": "dmitri.orlov",
    "avatar": "DO", "color": "#3d5a80",
    "bio": "Head of Ops @SilverCompany | Supply chain, logistics, Athens office | d.orlov@silvercompany.com",
    "location": "Athens, Greece", "joined": "November 2018",
    "following": 444, "followers": 1092,
    "posts": [
      {"id":"do1","text":"Athens warehouse is finally fully operational. Took 6 months but we got there. Capacity: 12,000 sq/m. Next step — Thessaloniki. #logistics","ts":"2024-03-11 14:22","likes":38,"reposts":7,"comments":5,"image":None},
      {"id":"do2","text":"Anyone else annoyed that the IT team reset everyone's passwords without notice? Had to call the helpdesk at 7am. Not a great start to Monday.","ts":"2024-03-04 07:58","likes":92,"reposts":3,"comments":29,"image":None},
      {"id":"do3","text":"Wrapping up Q4 supplier audits. Three vendors flagged. Will be a fun conversation with procurement next week 😬","ts":"2024-02-18 18:10","likes":15,"reposts":2,"comments":8,"image":None}
    ]
  },
  "nina.cross": {
    "display": "Nina Cross", "handle": "nina.cross",
    "avatar": "NC", "color": "#0d3b6e",
    "bio": "Founder @BlueFeatherMedia | PR, digital strategy, brand | London 🇬🇧 | n.cross@bluefeather.com | She/her",
    "location": "London, UK", "joined": "January 2017",
    "following": 1203, "followers": 8844,
    "posts": [
      {"id":"nc1","text":"Big news coming from @BlueFeatherMedia next week. Let's just say a major manufacturing brand is about to get a serious social media glow-up 👀","ts":"2024-03-13 10:00","likes":210,"reposts":55,"comments":23,"image":None},
      {"id":"nc2","text":"The Orlov data story is a reminder: your execs' public posts ARE your attack surface. We run social OSINT audits for all new clients now. DM me.","ts":"2024-02-01 09:15","likes":433,"reposts":189,"comments":67,"image":None},
      {"id":"nc3","text":"Hot take: your company's robots.txt file is a roadmap for attackers. Hide your /admin and /backup paths BEFORE you launch. #infosec #pr","ts":"2024-01-22 15:30","likes":611,"reposts":244,"comments":88,"image":None}
    ]
  },
  "tom.bekele": {
    "display": "Tom Bekele", "handle": "tom.bekele",
    "avatar": "TB", "color": "#1565c0",
    "bio": "Social Media Manager @BlueFeatherMedia | Content, analytics, vibes ✌️ | London | t.bekele@gmail.com",
    "location": "London, UK", "joined": "April 2021",
    "following": 882, "followers": 3241,
    "posts": [
      {"id":"tb1","text":"Managing @SilverCompany's Famebook page this month. If you see unusually polished content from a manufacturing firm, that's me 😄 #socialmediamanager","ts":"2024-03-14 12:30","likes":176,"reposts":28,"comments":14,"image":None},
      {"id":"tb2","text":"Famebook engagement tip: post between 11am-1pm Tuesday through Thursday. Algorithm loves it right now. You're welcome.","ts":"2024-03-07 11:05","likes":302,"reposts":111,"comments":37,"image":None},
      {"id":"tb3","text":"Using the API key I got from @alexei.romanov to schedule posts now. Game changer for batch content. Whoever built this API deserves a raise.","ts":"2024-02-25 16:44","likes":88,"reposts":12,"comments":9,"image":None}
    ]
  },
  "alexei.romanov": {
    "display": "Alexei Romanov", "handle": "alexei.romanov",
    "avatar": "AR", "color": "#145a32",
    "bio": "Head of Digital @BlueFeatherMedia | Dev, data, automation | Remote 🌍 | a.romanov@bluefeather.com",
    "location": "Remote (Lisbon, PT)", "joined": "September 2019",
    "following": 567, "followers": 1788,
    "posts": [
      {"id":"ar1","text":"Rebuilt the social scheduler from scratch. Python + SQLite, runs on a single VPS. Zero cloud costs. Sometimes simple is better.","ts":"2024-03-09 20:00","likes":145,"reposts":44,"comments":19,"image":None},
      {"id":"ar2","text":"PSA: rotating your API keys every 90 days is pointless if you're committing them to a public repo first. Ask me how I know 😬","ts":"2024-02-12 09:20","likes":892,"reposts":341,"comments":103,"image":None},
      {"id":"ar3","text":"Just found an exposed .git directory on a client's staging site. Not ours thankfully. Always check /.git/config before you go live people.","ts":"2024-01-30 14:15","likes":567,"reposts":198,"comments":55,"image":None}
    ]
  },
  "sara.dimitriou": {
    "display": "Sara Dimitriou", "handle": "sara.dimitriou",
    "avatar": "SD", "color": "#6a0572",
    "bio": "HR Manager @SilverCompany | People, culture, wellbeing | Athens 🇬🇷 | s.dimitriou@silvercompany.com | she/her",
    "location": "Athens, Greece", "joined": "February 2020",
    "following": 310, "followers": 892,
    "posts": [
      {"id":"sd1","text":"We're hiring! 3 open roles at @SilverCompany Athens — ops coordinator, warehouse supervisor, and junior logistics analyst. DM me or check our website. #hiring","ts":"2024-03-14 09:00","likes":55,"reposts":31,"comments":10,"image":None},
      {"id":"sd2","text":"Team lunch today to celebrate the warehouse opening. 40 people, souvlaki, and way too much sun ☀️ Proud of this team.","ts":"2024-03-11 15:45","likes":112,"reposts":8,"comments":17,"image":None},
      {"id":"sd3","text":"Reminder to all Athens staff: mandatory security awareness training deadline is March 31st. Not optional. Check your inbox. #security","ts":"2024-03-01 10:15","likes":18,"reposts":22,"comments":5,"image":None}
    ]
  },
  "luca.ferrari": {
    "display": "Luca Ferrari", "handle": "luca.ferrari",
    "avatar": "LF", "color": "#b5451b",
    "bio": "Freelance photographer & traveller | Milan 🇮🇹 | luca.ferrari@gmail.com | Capturing the world one frame at a time 📷",
    "location": "Milan, Italy", "joined": "June 2018",
    "following": 740, "followers": 5610,
    "posts": [
      {"id":"lf1","text":"Just back from a week in the Dolomites. No Wi-Fi, no meetings, just peaks and silence. Highly recommended 🏔️ #travel #photography","ts":"2024-03-13 19:30","likes":388,"reposts":61,"comments":42,"image":None},
      {"id":"lf2","text":"Golden hour in Santorini never gets old. Shot this on the A7IV, single exposure, zero edits. Nature does all the work. #photography #greece","ts":"2024-03-02 20:05","likes":512,"reposts":94,"comments":58,"image":None},
      {"id":"lf3","text":"To every brand that DMs me 'we'd love to collab, we just can't pay': I see you. Stop it.","ts":"2024-02-10 11:20","likes":1204,"reposts":430,"comments":177,"image":None}
    ]
  },
  "johny.skinny": {
    "display": "Johny Skinny", "handle": "johny.skinny",
    "avatar": "JS", "color": "#2d6a4f",
    "bio": "Just a guy who loves hiking, good vibes and cold beers 🍺🏔️ | Athens, Greece | recruit@bluefeather.com",
    "location": "Athens, Greece", "joined": "August 2021",
    "following": 183, "followers": 412,
    "posts": [
      {"id":"js1","text":"Weekend escape to the mountains ⛰️ Nothing beats fresh air and silence after a long week in the city. Already planning the next trip. #hiking #mountains #nature","ts":"2024-03-16 18:45","likes":74,"reposts":6,"comments":11,"image":"/static/johnyskinny_mountains.jpg"},
      {"id":"js2","text":"Anyone else feel like Mondays hit harder after a mountain weekend? Worth it though 😅 #mondayblues","ts":"2024-03-18 08:10","likes":43,"reposts":3,"comments":7,"image":None},
      {"id":"js3","text":"Found a great trail near Parnitha yesterday. 3 hours up, 2 down, zero phone signal. Peak digital detox 🌿","ts":"2024-03-05 17:30","likes":29,"reposts":4,"comments":3,"image":None}
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
  <title>{{ title }} — Famebook</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Segoe UI',Arial,sans-serif;background:#f0f2f5;color:#1c1e21}
    a{text-decoration:none;color:inherit}
    .topbar{background:#1877f2;color:#fff;padding:0 24px;display:flex;align-items:center;height:56px;position:sticky;top:0;z-index:100;box-shadow:0 2px 6px rgba(0,0,0,0.2)}
    .topbar .logo{font-size:1.7rem;font-weight:800;letter-spacing:-1px;margin-right:32px}
    .topbar .logo span{color:#c0d8ff}
    .topbar nav a{color:#fff;margin-right:18px;font-size:0.92rem;opacity:0.9}
    .topbar nav a:hover{opacity:1;text-decoration:underline}
    .topbar .search{background:rgba(255,255,255,0.18);border:none;border-radius:20px;padding:6px 16px;color:#fff;font-size:0.9rem;width:200px}
    .topbar .search::placeholder{color:#c8dcf8}
    .layout{max-width:1100px;margin:28px auto;display:grid;grid-template-columns:260px 1fr 280px;gap:20px;padding:0 12px}
    .sidebar-card{background:#fff;border-radius:10px;padding:18px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
    .sidebar-card h4{font-size:0.83rem;color:#888;text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px}
    .user-pill{display:flex;align-items:center;gap:10px;margin-bottom:10px;cursor:pointer}
    .user-pill:hover .uname{text-decoration:underline;color:#1877f2}
    .avatar{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:0.85rem;flex-shrink:0}
    .uname{font-weight:600;font-size:0.92rem}
    .uhandle{font-size:0.78rem;color:#888}
    .post-card{background:#fff;border-radius:10px;padding:18px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
    .post-header{display:flex;align-items:center;gap:12px;margin-bottom:10px}
    .post-meta{flex:1}
    .post-meta .name{font-weight:700;font-size:0.95rem}
    .post-meta .handle{font-size:0.8rem;color:#888}
    .post-meta .ts{font-size:0.78rem;color:#aaa;margin-left:6px}
    .post-body{font-size:0.95rem;line-height:1.55;margin-bottom:12px}
    .post-img{width:100%;max-height:340px;object-fit:cover;border-radius:8px;margin-bottom:12px}
    .post-actions{display:flex;gap:22px;font-size:0.82rem;color:#888}
    .post-actions span{cursor:pointer}
    .post-actions span:hover{color:#1877f2}
    .profile-hero{background:#fff;border-radius:10px;overflow:hidden;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
    .profile-banner{height:120px;background:linear-gradient(135deg,#1877f2,#42b0ff)}
    .profile-info{padding:16px 20px 20px}
    .profile-avatar{width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:1.4rem;margin-top:-36px;border:3px solid #fff}
    .profile-info h2{margin-top:8px;font-size:1.2rem}
    .profile-info .bio{font-size:0.88rem;color:#555;margin:4px 0 8px}
    .profile-info .meta{font-size:0.82rem;color:#888;margin-bottom:6px}
    .profile-stats{display:flex;gap:20px;font-size:0.88rem}
    .profile-stats span strong{color:#1c1e21}
    .trending-item{margin-bottom:10px;font-size:0.88rem}
    .trending-item .tag{color:#1877f2;font-weight:600}
    .trending-item .count{color:#aaa;font-size:0.78rem}
  </style>
</head>
<body>
<div class="topbar">
  <a href="/" class="logo">f<span>amebook</span></a>
  <nav>
    <a href="/">Home</a>
    <a href="/people">People</a>
    <a href="/trending">Trending</a>
  </nav>
  <input class="search" placeholder="Search Famebook…">
</div>
{% block content %}{% endblock %}
</body>
</html>
"""

POST_PARTIAL = """
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
      <div class="trending-item"><div class="tag">#manufacturing</div><div class="count">142 posts</div></div>
      <div class="trending-item"><div class="tag">#infosec</div><div class="count">89 posts</div></div>
      <div class="trending-item"><div class="tag">#hiking</div><div class="count">67 posts</div></div>
      <div class="trending-item"><div class="tag">#expansion</div><div class="count">54 posts</div></div>
      <div class="trending-item"><div class="tag">#aerospace</div><div class="count">47 posts</div></div>
      <div class="trending-item"><div class="tag">#photography</div><div class="count">38 posts</div></div>
      <div class="trending-item"><div class="tag">#digitalstrategy</div><div class="count">33 posts</div></div>
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
  <h2 style="margin-bottom:18px;color:#1a1a2e">People on Famebook</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px">
    {% for handle, u in users.items() %}
    <a href="/profile/{{ handle }}" style="display:block">
      <div class="sidebar-card" style="display:flex;align-items:center;gap:14px;cursor:pointer">
        <div class="avatar" style="background:{{ u.color }};width:52px;height:52px;font-size:1.1rem">{{ u.avatar }}</div>
        <div>
          <div style="font-weight:700">{{ u.display }}</div>
          <div style="font-size:0.8rem;color:#888">@{{ u.handle }}</div>
          <div style="font-size:0.78rem;color:#aaa;margin-top:4px">{{ u.followers }} followers</div>
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
  app.run(host="0.0.0.0", port=5000)
