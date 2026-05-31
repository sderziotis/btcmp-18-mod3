# btcmp-18 — Lab Environment

## Overview

This lab environment uses **xubuntu-noble-x86_64** as the base image for all machines.

---

## Topology

| Host | Network | CIDR | IP |
|------|---------|------|----|
| inv1 | network-2 | 192.168.0.0/24 | 192.168.0.10 |
| lab1 | network-3 | 192.168.10.0/24 | 192.168.10.10 |
| fs1  | network-3 | 192.168.10.0/24 | 192.168.10.20 |

All simulated web properties resolve to **lab1 (192.168.10.10)** via `/etc/hosts` entries injected on both machines.
Case files are served by **fs1 (192.168.10.20)** via Apache.

---

## Machines

### INV1 — Investigator Workstation
**User:** `user` / `Password123` (sudo enabled)

**Software:** Python3, pip, pipx, Node.js, npm, Git, build-essential, wget, curl, jq, unzip, zip, Firefox, Chromium, ExifTool, ffmpeg, ImageMagick, Sherlock, dirb

**Notes:**
- Sherlock: `sherlock <username>` from terminal. A shell alias is configured so Sherlock always loads the custom sites file automatically:
  ```
  alias sherlock='sherlock --json /usr/local/lib/python3.12/dist-packages/sherlock_project/resources/custom_sites.json'
  ```
- Sherlock uses `custom_sites.json` and searches only the custom domains listed below.
- `/etc/hosts` has been modified so all custom domains resolve to `192.168.10.10` and the file server resolves to `192.168.10.20`.

---

### LAB1 — Server Machine
**User:** `user` / `btcmp18@admin` (sudo enabled)

**Software:** Python3, pip, pipx, Node.js, npm, PHP 8.3, php-cli, php-fpm, Git, build-essential, Apache2, wget, curl, jq, unzip, zip, rsync, net-tools, dnsutils, openssl, OpenSSH Server, SQLite3, cron, Flask, Gunicorn

**Services enabled at boot:** Apache2, OpenSSH, cron, Famebook (systemd, port 5000), PostIt (systemd, port 5001), MyBlogSpot (systemd, port 5002), Searchly (systemd, port 5010), Archivly (systemd, port 5011)

---

### FS1 — File Server
**User:** `user` / `btcmp18@admin` (sudo enabled)

**Software:** Apache2

**Services enabled at boot:** Apache2

**Serves the following paths:**
- `http://192.168.10.20/case01/` — scenario files for Case 01
- `http://192.168.10.20/case22/` — scenario files for Case 22
- `http://192.168.10.20/module6/` — scenario files for Module 6

Root (`/`) is denied — only the aliased paths above are accessible.

---

## Simulated Web Properties

All domains resolve to `192.168.10.10` (lab1) via `/etc/hosts` on both machines.

### www.northgate-uni.edu — University CS Department
- **Stack:** Apache2 virtual host, static HTML
- **Persona:** Department of Computer Science, Northgate University — fictional institution, Manchester
---

### www.searchly.com — Simulated Search Engine
- **Stack:** Flask app (systemd service on port 5010) + Apache2 reverse proxy
- **Persona:** Generic web search engine — minimal Google-style UI
- **Supports operators:** `site:`, `filetype:`, `inurl:`, `intitle:`, `cache:`

**Routes:**
- `/` — search homepage
- `/search?q=<query>` — results page

**To restart manually:** `sudo systemctl restart searchly`

---

### www.archivly.com — Simulated Web Archive
- **Stack:** Flask app (systemd service on port 5011) + Apache2 reverse proxy
- **Persona:** Dark-themed web archive — similar in concept to the Wayback Machine


**Routes:**
- `/` — homepage listing all archived domains
- `/browse?domain=<domain>` — list snapshots for a domain
- `/view/<domain>/<snapshot_id>` — view a specific snapshot

**To restart manually:** `sudo systemctl restart archivly`

---

### www.silvercompany.com — Corporate Site #1
- **Stack:** Apache2 virtual host, static HTML
- **Persona:** Silver Company GmbH — precision manufacturing, Frankfurt HQ

---

### www.bluefeather.com — Corporate Site #2
- **Stack:** Apache2 virtual host, static HTML
- **Persona:** Blue Feather Media Ltd — digital PR agency, London
---

### www.famebook.com — Social Media Platform #1
- **Stack:** Flask app (systemd service on port 5000) + Apache2 reverse proxy
- **Static files:** `/opt/famebook/static/` — served via Flask `send_from_directory`

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

**Routes:**
- `/` — main feed
- `/people` — all profiles grid
- `/profile/<handle>` — individual profile page

**To restart manually:** `sudo systemctl restart postit`

---

### www.myblogspot.com — Personal Travel Blog
- **Stack:** Flask app (systemd service on port 5002) + Apache2 reverse proxy
- **Persona:** Nikos Andreou's personal travel blog — Athens, Lisbon, Greek islands, travel tips


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

`/etc/hosts` entries are injected on **both** inv1 and lab1:

```
192.168.10.10  www.silvercompany.com silvercompany.com
192.168.10.10  www.bluefeather.com bluefeather.com
192.168.10.10  www.famebook.com famebook.com
192.168.10.10  www.postit.com postit.com
192.168.10.10  www.myblogspot.com myblogspot.com
192.168.10.10  www.northgate-uni.edu northgate-uni.edu
192.168.10.10  www.searchly.com searchly.com
192.168.10.10  www.archivly.com archivly.com
192.168.10.20  www.fileserver.com fileserver.com
```

---

## Notes
- PHP defaults to **8.3** as provided by Ubuntu 24.04 repos.
- Famebook Flask app runs as `www-data` via systemd; Apache proxies port 80 → 5000.
- PostIt Flask app runs as `www-data` via systemd; Apache proxies port 80 → 5001.
- MyBlogSpot Flask app runs as `www-data` via systemd; Apache proxies port 80 → 5002.
- Searchly Flask app runs as `www-data` via systemd; Apache proxies port 80 → 5010.
- Archivly Flask app runs as `www-data` via systemd; Apache proxies port 80 → 5011.
- Northgate website is static HTML served by Apache; Django is faked via HTTP headers only — no Django runtime installed.
- fs1 serves case files only; root (`/`) is access-denied. All content is under named aliases.
