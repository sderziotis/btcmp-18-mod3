from flask import Flask, render_template_string, abort, send_from_directory
import os

app = Flask(__name__)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

POSTS = [
  {
    "slug": "lisbon-hidden-gems",
    "title": "Lisbon's Hidden Gems: Beyond the Tourist Trail",
    "author": "Nikos Andreou",
    "date": "March 18, 2024",
    "category": "Europe",
    "excerpt": "Everyone knows Belém and Alfama, but Lisbon has so much more to offer if you're willing to get lost.",
    "body": """Everyone knows Belém Tower and the winding streets of Alfama. But spend a week in Lisbon and you start finding the places the guidebooks forgot. Mouraria, the city's oldest neighbourhood, hides some of the best tascas I've ever eaten in. Order whatever the owner recommends — you won't regret it.

I spent three mornings walking the Tagus waterfront before the crowds arrived. The light at 7am on the river is something photographers chase for years. Bring a good camera and comfortable shoes.

Getting around: the famous trams are charming but packed. The metro is cheap, fast and underused by tourists. A 24-hour pass costs almost nothing and takes you everywhere that matters.

My favourite discovery: the Jardim do Torel, a small hilltop garden most visitors walk straight past. On a clear day you can see halfway across the city.""",
    "image": None,
    "tags": ["lisbon", "portugal", "travel", "europe"]
  },
  {
    "slug": "athens-weekend-guide",
    "title": "48 Hours in Athens: The Local's Version",
    "author": "Nikos Andreou",
    "date": "March 5, 2024",
    "category": "Greece",
    "excerpt": "Skip the Plaka tourist traps. Here's how locals actually spend a weekend in the Greek capital.",
    "body": """Athens gets dismissed as a stopover city. People spend one day at the Acropolis and fly out. That's a mistake.

Saturday morning: walk Monastiraki flea market before 9am, when it's still locals selling actual antiques rather than souvenir shops. Grab a coffee at one of the tiny kafeneions on the side streets — proper Greek coffee, not the chain stuff.

Afternoon: Exarchia neighbourhood for lunch. The neighbourhood has a reputation, but honestly it's one of the most interesting parts of the city. Good bookshops, better food, great people watching.

Evening: head to Koukaki, the area just south of the Acropolis. It's where young Athenians actually eat and drink. The rooftop bars with Parthenon views are packed but worth it for the sunset hour.

Sunday: if the weather's good, escape the city. Vouliagmeni beach is 25 minutes by bus and a completely different world from the city centre. The water in early spring is cold but the scenery is stunning.

One thing I keep coming back to: Athens rewards people who slow down. It's not a city you understand in a day.""",
    "image": None,
    "tags": ["athens", "greece", "weekend", "travel"]
  },
  {
    "slug": "solo-travel-packing-list",
    "title": "My Carry-On Only Packing List After 50+ Trips",
    "author": "Nikos Andreou",
    "date": "February 20, 2024",
    "category": "Tips",
    "excerpt": "After years of over-packing and under-packing, I finally cracked the formula for carry-on only travel.",
    "body": """It took me embarrassingly long to figure this out. I used to check bags for a long weekend. Now I do two weeks in a 40L backpack.

The shift happened after a delayed luggage incident in Frankfurt that cost me a full day of a work trip. Never again.

The key insight: you wear far less than you think. On any trip I end up rotating 3-4 outfits regardless of how many I pack. So pack those 3-4 outfits and nothing else.

What actually makes the difference:
- A lightweight merino wool base layer (wears multiple days, dries overnight)
- One pair of shoes that works for walking and going out
- Packing cubes — game changer for organisation
- A small laundry bag and travel detergent for anything longer than 5 days

What I always leave behind now: "just in case" items, extra shoes, full-size toiletries, and anything I haven't worn in the past month.

The weight limit I set myself: 7kg total. Everything has to fit. If it doesn't, something gets cut.""",
    "image": None,
    "tags": ["packing", "tips", "carry-on", "travel"]
  },
  {
    "slug": "greek-islands-off-season",
    "title": "Greek Islands in Winter: What Nobody Tells You",
    "author": "Nikos Andreou",
    "date": "February 3, 2024",
    "category": "Greece",
    "excerpt": "The islands in winter are quiet, cheap, and completely different from the summer crowds — and I prefer them this way.",
    "body": """Most people think the Greek islands shut down in winter. Some do. But the bigger ones — Rhodes, Corfu, Crete — stay alive year round, just at a different pace.

I spent a January week on Rhodes last year. The old town, normally heaving with tourists, was almost empty. I walked the medieval walls with maybe a dozen other people. The restaurants that stay open are the ones locals actually eat at — the tourist traps close for the season.

Prices: roughly half what you'd pay in summer for accommodation. Flights are similarly reduced. It's the same sea, same light, same food.

What changes: some beaches are inaccessible or closed, boat trips are weather-dependent, and you'll need a jacket in the evenings. Small prices to pay.

The real benefit nobody mentions: you actually get to talk to people. Locals have time in winter. Shopkeepers, taverna owners, the guy who rents you a scooter — they'll tell you things about their island that no travel guide covers.

My recommendation for first-timers: Crete in November. The weather is still warm enough, the olive harvest is happening, and the island feels completely authentic.""",
    "image": None,
    "tags": ["greece", "islands", "winter", "rhodes", "crete"]
  },
  {
    "slug": "airport-hacks-frequent-flyer",
    "title": "Airport Hacks from a Frequent Flyer",
    "author": "Nikos Andreou",
    "date": "January 15, 2024",
    "category": "Tips",
    "excerpt": "I fly roughly twice a month for work. Here's what I've learned about making airports less painful.",
    "body": """Flying twice a month for work will teach you things about airports that casual travellers never learn.

The most valuable: time your arrival correctly. Not too early, not too late. For European short-haul, 75 minutes before departure is the sweet spot if you have no checked bags. The security queue is the only real variable.

Speaking of security: the fast track lanes are often not worth the money at smaller airports where the main queue moves quickly. At Heathrow, Athens, or Frankfurt — absolutely worth it.

The lounges nobody tells you about: many airports have pay-per-entry lounges that cost less than a meal and a beer in the terminal. A day pass to a Priority Pass lounge is typically €25-35 and includes food, drink, wifi, and somewhere quiet to sit. Easily worth it on a long connection.

My current carry-on setup for work trips: laptop in a sleeve not a bag (faster through security), all liquids in an accessible outer pocket, boarding pass on phone with the app already open before I join the queue.

The rule I never break: download everything I need before I fly. Podcasts, offline maps, any documents. Airport wifi is unreliable and expensive data roaming is a habit I broke years ago.""",
    "image": None,
    "tags": ["airports", "tips", "flying", "travel hacks"]
  },
]

BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} — MyBlogSpot</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:Georgia,'Times New Roman',serif;background:#fafaf8;color:#2c2c2c}
    a{text-decoration:none;color:inherit}
    .topbar{background:#2c2c2c;color:#fafaf8;padding:0 40px;height:60px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
    .topbar .logo{font-size:1.5rem;font-weight:700;letter-spacing:2px;color:#f5c842}
    .topbar nav a{color:#ccc;margin-left:24px;font-size:0.88rem;font-family:'Segoe UI',sans-serif;letter-spacing:0.05em;text-transform:uppercase}
    .topbar nav a:hover{color:#f5c842}
    .hero-bar{background:#f5c842;padding:60px 40px;text-align:center}
    .hero-bar h2{font-size:2rem;color:#2c2c2c;font-weight:700}
    .hero-bar p{color:#555;margin-top:8px;font-family:'Segoe UI',sans-serif;font-size:1rem}
    .layout{max-width:1050px;margin:50px auto;display:grid;grid-template-columns:1fr 300px;gap:40px;padding:0 20px}
    .post-card{border-bottom:1px solid #e8e4dc;padding-bottom:32px;margin-bottom:32px}
    .post-card .cat{font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;color:#f5c842;background:#2c2c2c;padding:3px 10px;border-radius:2px;font-family:'Segoe UI',sans-serif;display:inline-block;margin-bottom:10px}
    .post-card h2{font-size:1.5rem;margin-bottom:8px;line-height:1.3}
    .post-card h2 a:hover{color:#b8960a}
    .post-card .meta{font-size:0.82rem;color:#999;font-family:'Segoe UI',sans-serif;margin-bottom:12px}
    .post-card .excerpt{font-size:0.97rem;line-height:1.65;color:#444}
    .post-card .read-more{display:inline-block;margin-top:14px;font-size:0.85rem;font-family:'Segoe UI',sans-serif;color:#b8960a;border-bottom:1px solid #b8960a}
    .sidebar-box{background:#fff;border:1px solid #e8e4dc;padding:22px;margin-bottom:28px;border-radius:4px}
    .sidebar-box h4{font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;color:#999;font-family:'Segoe UI',sans-serif;margin-bottom:14px;border-bottom:1px solid #e8e4dc;padding-bottom:8px}
    .tag-cloud a{display:inline-block;background:#f0ede6;color:#555;font-size:0.8rem;padding:4px 10px;margin:3px;border-radius:2px;font-family:'Segoe UI',sans-serif}
    .tag-cloud a:hover{background:#f5c842;color:#2c2c2c}
    .about-text{font-size:0.88rem;line-height:1.6;color:#555;font-family:'Segoe UI',sans-serif}
    .post-full{max-width:720px;margin:50px auto;padding:0 20px}
    .post-full h1{font-size:2rem;margin-bottom:10px;line-height:1.3}
    .post-full .meta{font-size:0.85rem;color:#999;font-family:'Segoe UI',sans-serif;margin-bottom:30px;padding-bottom:16px;border-bottom:1px solid #e8e4dc}
    .post-full .body p{margin-bottom:18px;line-height:1.8;font-size:1rem}
    .post-full .tags{margin-top:30px;padding-top:16px;border-top:1px solid #e8e4dc}
    .post-full .tags a{display:inline-block;background:#f0ede6;color:#555;font-size:0.8rem;padding:4px 10px;margin:3px;border-radius:2px;font-family:'Segoe UI',sans-serif}
    .back-link{display:inline-block;margin-bottom:24px;font-size:0.85rem;font-family:'Segoe UI',sans-serif;color:#b8960a}
    footer{background:#2c2c2c;color:#888;text-align:center;padding:24px;font-size:0.82rem;font-family:'Segoe UI',sans-serif;margin-top:60px}
  </style>
</head>
<body>
<div class="topbar">
  <a href="/" class="logo">MyBlogSpot</a>
  <nav>
    <a href="/">Home</a>
    <a href="/category/europe">Europe</a>
    <a href="/category/greece">Greece</a>
    <a href="/category/tips">Tips</a>
    <a href="/about">About</a>
  </nav>
</div>
{% block content %}{% endblock %}
<footer>&copy; 2024 MyBlogSpot &nbsp;|&nbsp; A personal travel journal</footer>
</body>
</html>
"""

HOME_TMPL = BASE.replace("{% block content %}{% endblock %}", """
<div class="hero-bar">
  <h2>Travel Stories & Notes from the Road</h2>
  <p>Personal travel writing — cities, islands, airports, and everything in between.</p>
</div>
<div class="layout">
  <div class="main">
    {% for post in posts %}
    <div class="post-card">
      <span class="cat">{{ post.category }}</span>
      <h2><a href="/post/{{ post.slug }}">{{ post.title }}</a></h2>
      <div class="meta">By {{ post.author }} &nbsp;·&nbsp; {{ post.date }}</div>
      <div class="excerpt">{{ post.excerpt }}</div>
      <a href="/post/{{ post.slug }}" class="read-more">Read more →</a>
    </div>
    {% endfor %}
  </div>
  <div class="sidebar">
    <div class="sidebar-box">
      <h4>About</h4>
      <p class="about-text">Personal travel notes from Nikos Andreou. Writing about places I've been, things I've learned, and occasionally opinions nobody asked for.</p>
    </div>
    <div class="sidebar-box">
      <h4>Tags</h4>
      <div class="tag-cloud">
        <a href="#">greece</a><a href="#">europe</a><a href="#">athens</a>
        <a href="#">tips</a><a href="#">packing</a><a href="#">islands</a>
        <a href="#">lisbon</a><a href="#">winter</a><a href="#">airports</a>
        <a href="#">portugal</a>
      </div>
    </div>
    <div class="sidebar-box">
      <h4>Categories</h4>
      <p class="about-text" style="line-height:2">
        <a href="/category/greece" style="color:#b8960a">Greece</a><br>
        <a href="/category/europe" style="color:#b8960a">Europe</a><br>
        <a href="/category/tips" style="color:#b8960a">Tips &amp; Hacks</a>
      </p>
    </div>
  </div>
</div>
""")

POST_TMPL = BASE.replace("{% block content %}{% endblock %}", """
<div class="post-full">
  <a href="/" class="back-link">← Back to all posts</a>
  <span class="cat" style="background:#2c2c2c;color:#f5c842;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;padding:3px 10px;border-radius:2px;font-family:Segoe UI,sans-serif;display:inline-block;margin-bottom:10px">{{ post.category }}</span>
  <h1>{{ post.title }}</h1>
  <div class="meta">By {{ post.author }} &nbsp;·&nbsp; {{ post.date }}</div>
  <div class="body">
    {% for paragraph in post.body.split('\\n\\n') %}
    <p>{{ paragraph }}</p>
    {% endfor %}
  </div>
  <div class="tags">
    {% for tag in post.tags %}<a href="#">#{{ tag }}</a>{% endfor %}
  </div>
</div>
""")

ABOUT_TMPL = BASE.replace("{% block content %}{% endblock %}", """
<div class="post-full">
  <h1>About</h1>
  <div class="meta" style="margin-bottom:20px">MyBlogSpot — a personal travel journal</div>
  <div class="body">
    <p>Hi, I'm Nikos. I travel a lot — mostly for work, sometimes for myself. This blog started as a way to keep notes I could actually find later. It turned into something I update regularly.</p>
    <p>I'm based in Athens, Greece, though you'll often find me in London, Lisbon, or somewhere between the two. I write about places honestly: what's worth your time, what isn't, and what the guidebooks get wrong.</p>
    <p>If something here is useful to you, great. If you want to get in touch, find me on PostIt.</p>
  </div>
</div>
""")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

@app.route("/")
def home():
    return render_template_string(HOME_TMPL, title="Home", posts=POSTS)

@app.route("/post/<slug>")
def post(slug):
    p = next((p for p in POSTS if p["slug"] == slug), None)
    if not p:
        abort(404)
    return render_template_string(POST_TMPL, title=p["title"], post=p)

@app.route("/about")
def about():
    return render_template_string(ABOUT_TMPL, title="About")

@app.route("/category/<cat>")
def category(cat):
    filtered = [p for p in POSTS if p["category"].lower() == cat.lower()]
    return render_template_string(HOME_TMPL, title=cat.title(), posts=filtered)

@app.route("/static/manifest.pdf")
def manifest():
    return send_from_directory(STATIC_DIR, "manifest.pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
