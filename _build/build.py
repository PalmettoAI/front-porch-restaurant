#!/usr/bin/env python3
"""Builds the site's HTML pages from _build/pages/*.html.

Each page file starts with a JSON block inside <!--- ... ---> giving
title / description / path / og / schema. The shared <head>, header and
footer are added here so they stay identical on every page.

Run from the repo root:   python3 _build/build.py
To move to the real domain later, change BASE below and re-run.
(GitHub Pages ignores folders starting with "_", so this folder is never served.)
"""
import json, re, pathlib

BASE = "https://palmettoai.github.io/front-porch-restaurant/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "_build" / "pages"
VER = "6"  # bump to bust CSS/JS cache after edits

NAV = [("index.html", "Home"), ("pies.html", "Pie Shop"), ("breakfast.html", "Breakfast"), ("menu.html", "Menu")]

LOGO = """<svg viewBox="0 0 108 80" aria-hidden="true" focusable="false"><circle cx="54" cy="52" r="30" fill="#EFE3B8"/><g fill="none" stroke="#1F4E9C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M14 66h80"/><path d="M28 64V44l26-14 26 14v20"/><path d="M22 46l32-18 32 18"/><path d="M28 52h52"/><path d="M36 52v12M46 52v12M62 52v12M72 52v12"/><path d="M50 40h8v6h-8z"/><path d="M64 33v-8h5v11"/></g><g fill="#1F4E9C"><path d="M8 66c2-14 3-24 4-34l2 0c0 10 1 20 3 34z"/><path d="M13 32c-6-4-11-3-13 0 4-1 8 0 11 2-5 0-8 3-9 6 4-3 7-4 11-3-2 2-3 6-2 9 2-4 3-6 5-8 1 3 4 5 7 6-1-4-3-6-5-8 4 0 7 2 9 4-1-4-5-7-9-7 3-2 7-2 10-1-3-3-8-4-12-2 1-2 4-4 7-4-4-2-8-1-10 6z"/><path d="M95 66c2-12 2-20 3-30h2c0 10 0 18 2 30z"/><path d="M99 36c-5-3-9-2-11 1 3-1 7 0 9 2-4 0-7 2-8 5 3-2 6-3 9-2-1 2-2 5-1 7 1-3 2-5 4-6 1 2 3 4 6 5-1-3-3-5-4-7 3 0 6 1 8 3-1-3-4-5-8-6 3-1 6-1 8 0-3-2-7-3-10-2 1-2 3-3 6-3-3-2-7-1-8 5z"/></g></svg>"""

PHONE_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'
PIE_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M2 14h20l-1.6 4.2A3 3 0 0 1 17.6 20H6.4a3 3 0 0 1-2.8-1.8zM12 4c4.9 0 9 3.3 9.8 8H2.2C3 7.3 7.1 4 12 4zm-3 3.5a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm6 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/></svg>'

RESTAURANT = {
    "@type": "Restaurant",
    "@id": BASE + "#restaurant",
    "name": "Front Porch Restaurant & Pie Shop",
    "alternateName": "The Front Porch Restaurant & Pie Shop",
    "image": [BASE + "assets/img/hero.webp", BASE + "assets/img/pie-meringue.webp"],
    "logo": BASE + "assets/og/home.jpg",
    "url": BASE,
    "telephone": "+1-352-489-4708",
    "priceRange": "$10–20",
    "servesCuisine": ["American", "Southern", "Comfort Food", "Breakfast", "Pie"],
    "description": "Family owned and operated since 1986. Southern home cooking, country breakfast and homemade pies in Dunnellon, Florida.",
    "foundingDate": "1986",
    "address": {"@type": "PostalAddress", "streetAddress": "12039 N Florida Ave", "addressLocality": "Dunnellon",
                "addressRegion": "FL", "postalCode": "34434", "addressCountry": "US"},
    "geo": {"@type": "GeoCoordinates", "latitude": 29.0205, "longitude": -82.4337},
    "hasMap": "https://www.google.com/maps/search/?api=1&query=Front+Porch+Restaurant+12039+N+Florida+Ave+Dunnellon+FL+34434",
    "sameAs": ["https://www.facebook.com/p/The-Front-Porch-Restaurant-Pie-Shop-100044299162284/"],
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.4", "reviewCount": "3378", "bestRating": "5"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "07:00", "closes": "20:30"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "07:00", "closes": "20:00"}],
    "hasMenu": [BASE + "breakfast.html", BASE + "menu.html", BASE + "pies.html"],
    "acceptsReservations": "True",
    "paymentAccepted": "Cash, Credit Card, Debit Card, Contactless",
    "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True}
                       for n in ["Outdoor seating", "Live music", "Kids' menu", "Takeout", "Wheelchair accessible", "Free parking"]],
}


def head(m):
    url = BASE + ("" if m["path"] == "index.html" else m["path"])
    og = BASE + "assets/og/" + m["og"]
    graph = [RESTAURANT] + m.get("schema", [])
    if m["path"] != "index.html":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": m["crumb"], "item": url}]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    preload = f'<link rel="preload" as="image" href="{m["preload"]}" fetchpriority="high" />\n' if m.get("preload") else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{m["title"]}</title>
<meta name="description" content="{m["description"]}" />
<meta name="theme-color" content="#1F4E9C" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Front Porch Restaurant &amp; Pie Shop" />
<meta property="og:title" content="{m["og_title"]}" />
<meta property="og:description" content="{m["description"]}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{og}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{m["og_title"]}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{m["og_title"]}" />
<meta name="twitter:description" content="{m["description"]}" />
<meta name="twitter:image" content="{og}" />
{preload}<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&amp;family=Bitter:wght@400;700;800&amp;family=Yellowtail&amp;display=swap" />
<link rel="stylesheet" href="assets/site.css?v={VER}" />
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
<script type="application/ld+json">
{ld}
</script>
{m.get("style", "")}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    cur = ' aria-current="page"'
    links = "\n".join(
        f'    <a href="{p}"{cur if p == active else ""}>{label}</a>' for p, label in NAV)
    return f"""<div class="topbar">
  <div class="wrap">
    <span class="status"><span class="dot" aria-hidden="true"></span><span data-status>Tue–Sat 7 AM–8:30 PM · Sun 7 AM–8 PM · Closed Mon</span></span>
    <span>12039 N Florida Ave, Dunnellon · <a href="tel:+13524894708">(352) 489-4708</a></span>
  </div>
</div>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Front Porch Restaurant and Pie Shop, home">
      {LOGO}
      <span><b>Front Porch</b><small>Restaurant &amp; Pie Shop</small></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav id="site-nav" class="nav" aria-label="Main">
{links}
    <a class="btn btn-pie" href="pies.html#order">{PIE_ICON}Order Pies</a>
    </nav>
  </div>
</header>
"""


FOOTER = f"""<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <p class="foot-tag">Life’s short… eat pie first!</p>
        <p>Family owned and operated since 1986. Southern home cooking, country breakfast and pies baked every morning in Dunnellon, Florida.</p>
      </div>
      <div>
        <h2>Visit</h2>
        <p>12039 N Florida Ave<br />Dunnellon, FL 34434</p>
        <p><a href="tel:+13524894708">(352) 489-4708</a></p>
        <p><a href="https://www.google.com/maps/dir/?api=1&amp;destination=Front+Porch+Restaurant+12039+N+Florida+Ave+Dunnellon+FL+34434">Get directions</a></p>
      </div>
      <div>
        <h2>Hours</h2>
        <ul>
          <li>Tue–Sat · 7 AM–8:30 PM</li>
          <li>Sunday · 7 AM–8 PM</li>
          <li>Monday · Closed</li>
          <li>Breakfast till 11 (11:30 Sat &amp; Sun)</li>
        </ul>
      </div>
      <div>
        <h2>Explore</h2>
        <ul>
          <li><a href="pies.html">Order pies for pickup</a></li>
          <li><a href="breakfast.html">Breakfast menu</a></li>
          <li><a href="menu.html">Lunch &amp; supper menu</a></li>
          <li><a href="https://www.facebook.com/p/The-Front-Porch-Restaurant-Pie-Shop-100044299162284/" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© <span id="year">2026</span> Front Porch Restaurant &amp; Pie Shop · Dunnellon, FL</span>
      <span>Menu prices shown are cash prices and may change.</span>
    </div>
  </div>
</footer>
<div class="mobile-bar" aria-label="Quick actions">
  <a class="btn btn-blue" href="tel:+13524894708">{PHONE_ICON}Call</a>
  <a class="btn btn-pie" href="pies.html#order">{PIE_ICON}Order Pies</a>
</div>
<script src="assets/site.js?v={VER}" defer></script>
</body>
</html>
"""


def build():
    urls = []
    for f in sorted(PAGES.glob("*.html")):
        src = f.read_text()
        mt = re.match(r"\s*<!---(.*?)--->\s*", src, re.S)
        meta = json.loads(mt.group(1))
        body = src[mt.end():]
        body = body.replace("{{PHONE_ICON}}", PHONE_ICON).replace("{{PIE_ICON}}", PIE_ICON)
        out = head(meta) + header(meta["path"]) + body + FOOTER
        (ROOT / meta["path"]).write_text(out)
        if meta.get("sitemap", True):
            urls.append((BASE + ("" if meta["path"] == "index.html" else meta["path"]), meta.get("priority", "0.8")))
        print("built", meta["path"])
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{u}</loc><priority>{p}</priority></url>" for u, p in urls]
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")


if __name__ == "__main__":
    build()
