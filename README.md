# btcmp-18-mod3 — Lab Environment

## Overview

This lab environment uses **xubuntu-noble-x86_64** as the base image for both machines.

---

## Topology

| Host | Network | CIDR | IP |
|------|---------|------|----|
| inv1 | network-2 | 192.168.0.0/24 | 192.168.0.10 |
| lab1 | network-3 | 192.168.10.0/24 | 192.168.10.10 |

All simulated web properties resolve to **lab1 (192.168.10.10)** via `/etc/hosts` entries injected on both machines.

---

## Machines

### INV1 — Investigator Workstation
**User:** `user` / `Password123` (sudo enabled)

**Software:** Python3, pip, pipx, Node.js, npm, Git, build-essential, wget, curl, jq, unzip, zip, Firefox, Chromium, ExifTool, ffmpeg, ImageMagick, Tor Browser, SpiderFoot v3.5, Sherlock, dirb

**Notes:**
- Tor Browser is installed via `torbrowser-launcher` — user must run it once to complete download and setup.
- SpiderFoot v3.5: `python3 sf.py -l 127.0.0.1:5001` from `/opt/spiderfoot`
- Sherlock: `sherlock <username>` from terminal. A shell alias is configured so Sherlock always loads the custom sites file automatically:
  ```
  alias sherlock='sherlock --json /usr/local/lib/python3.12/dist-packages/sherlock_project/resources/custom_sites.json'
  ```
- A `case01/` folder is placed on the Desktop containing scenario files.

**Customizations:**
- Sherlock uses `custom_sites.json` and searches only the custom domains listed below.
- `/etc/hosts` has been modified so all custom domains resolve to `192.168.10.10`.

---

### LAB1 — Server Machine
**User:** `user` / `btcmp18@admin` (sudo enabled)

**Software:** Python3, pip, pipx, Node.js, npm, PHP 8.3, php-cli, php-fpm, Git, build-essential, Apache2, wget, curl, jq, unzip, zip, rsync, net-tools, dnsutils, openssl, OpenSSH Server, SQLite3, cron, Flask, Gunicorn

**Services enabled at boot:** Apache2, OpenSSH, cron, Famebook (systemd, port 5000), PostIt (systemd, port 5001), MyBlogSpot (systemd, port 5002)

---

## Simulated Web Properties

All domains resolve to `192.168.10.10` (lab1) via `/etc/hosts` on both machines.

### www.silvercompany.com — Corporate Site #1
- **Stack:** Apache2 virtual host, static HTML
- **Persona:** Silver Company GmbH — precision manufacturing, Frankfurt HQ
- **OSINT breadcrumbs:**
  - Staff names, emails, and job titles on the homepage (`m.hale@`, `e.voss@`, `d.orlov@`, `s.kimani@`)
  - `robots.txt` exposes: `/portal/`, `/internal/`, `/backup/`, `/admin/`
  - Server headers leak: `X-Powered-By: PHP/8.3.1`, `X-Generator: WordPress/6.4.2`
  - Company registration number, VAT ID, and phone in footer
  - Job listings reveal internal tech stack (Ansible, Kubernetes, GitLab CI, FreeRTOS, STM32)

### www.bluefeather.com — Corporate Site #2
- **Stack:** Apache2 virtual host, static HTML
- **Persona:** Blue Feather Media Ltd — digital PR agency, London
- **OSINT breadcrumbs:**
  - Homepage does **not** list staff — team section removed
  - Hidden staff directory at `/staff.html` (not linked from the homepage) contains full employee table with names, emails, departments, and social media links
  - `robots.txt` exposes: `/wp-admin/`, `/client-reports/`, `/.git/`
  - Server headers leak: `X-Generator: Joomla! 4.3`
  - Blog post references Silver Company and "the Orlov incident" — cross-site link
  - Company number (England & Wales) in footer


### www.famebook.com — Social Media Platform #1
- **Stack:** Flask app (systemd service on port 5000) + Apache2 reverse proxy
- **Static files:** `/opt/famebook/static/` — served via Flask `send_from_directory`
- **Personas & cross-links:**

**Routes:**
- `/` — main feed (all posts, chronological)
- `/people` — all profiles grid
- `/profile/<handle>` — individual profile page

**To restart manually:** `sudo systemctl restart famebook`

---

### www.postit.com — Social Media Platform #2
- **Stack:** Flask app (systemd service on port 5001) + Apache2 reverse proxy
- **Theme:** Purple/violet — visually distinct from Famebook
- **Static files:** `/opt/postit/static/` — served via Flask `send_from_directory`
- **Personas & cross-links:**

**Routes:**
- `/` — main feed
- `/people` — all profiles grid
- `/profile/<handle>` — individual profile page

**To restart manually:** `sudo systemctl restart postit`

---

### www.myblogspot.com — Personal Travel Blog
- **Stack:** Flask app (systemd service on port 5002) + Apache2 reverse proxy
- **Persona:** Nikos Andreou's personal travel blog — Athens, Lisbon, Greek islands, travel tips
- **Hidden file:** `/static/manifest.pdf` — not linked anywhere on the site; contains only "RADICAL CONTENT". 
- **About page:** mentions Athens as home base and refers visitors to PostIt — no email listed

**Routes:**
- `/` — home / post list
- `/post/<slug>` — individual post
- `/about` — about page
- `/category/<cat>` — filtered by category
- `/static/manifest.pdf` — hidden PDF

**To restart manually:** `sudo systemctl restart myblogspot`

---

## Sherlock Custom Sites (`custom_sites.json`)

Located at `/usr/local/lib/python3.12/dist-packages/sherlock_project/resources/custom_sites.json` on inv1.

---

## DNS / Domain Resolution Strategy

`/etc/hosts` entries are injected on **both** machines:

```
192.168.10.10  www.silvercompany.com silvercompany.com
192.168.10.10  www.bluefeather.com bluefeather.com
192.168.10.10  www.famebook.com famebook.com
192.168.10.10  www.postit.com postit.com
192.168.10.10  www.myblogspot.com myblogspot.com
```

---

## Notes
- PHP defaults to **8.3** as provided by Ubuntu 24.04 repos.
- Famebook Flask app runs as `www-data` via systemd; Apache proxies port 80 → 5000.
- PostIt Flask app runs as `www-data` via systemd; Apache proxies port 80 → 5001.
- MyBlogSpot Flask app runs as `www-data` via systemd; Apache proxies port 80 → 5002.
- SpiderFoot version pinned to **v3.5** (`/opt/spiderfoot`).
- The `case01/` folder is placed on the inv1 Desktop at `/home/user/Desktop/case01/`.
