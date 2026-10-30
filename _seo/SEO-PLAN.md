# Front Porch Restaurant & Pie Shop: SEO plan

**Client:** Front Porch Restaurant & Pie Shop, 12039 N Florida Ave, Dunnellon, FL 34434 · (352) 489-4708 · owner Michael Gray
**Written:** 2026-10-30 by PAA, adapted from the PAA SEO Playbook (`~/paa-seo-docs/SEO-PLAYBOOK.md`)
**Weekly operator:** Addie, the local LLM on Tony's Mac Studio. Instructions: `_seo/ADDIE.md`. Facts: `_seo/facts.json`.

## Goal

When someone near Dunnellon searches for breakfast, a pie or a place to eat, Front Porch shows up and they call or come in.

Michael's priorities, in order:
1. **More breakfast customers.** He said, "we are lacking in our breakfast category."
2. **More whole-pie orders.** Pies are local pickup with one day's notice.
3. Keep the lunch and supper regulars.

For a restaurant, success is measured in **calls, direction requests and pie orders**, not blog traffic. Google Business Profile (GBP) does most of the work for a restaurant. The website backs GBP up and wins the pie and holiday searches.

## Target searches

Don't promise rankings. These are the searches we're aiming at. Once Search Console has 4 weeks of data, check them against what people actually search.

| Page | Main searches | Supporting searches |
|---|---|---|
| Home | restaurants in Dunnellon FL, Southern food Dunnellon | Front Porch Dunnellon, family restaurant Dunnellon |
| breakfast.html | breakfast Dunnellon FL, breakfast near me (Dunnellon) | biscuits and gravy Dunnellon, country breakfast near Rainbow Springs |
| pies.html | pie shop Dunnellon, homemade pies near Ocala | whole pie order Dunnellon, meringue pie, Key lime pie Dunnellon |
| menu.html | Front Porch menu, lunch Dunnellon | country fried steak Dunnellon, fried chicken Dunnellon |
| (new) thanksgiving-pies.html | Thanksgiving pies Dunnellon, Thanksgiving pie order Ocala | pumpkin pie order, pecan pie order |
| (new) christmas-pies.html | Christmas pies Dunnellon | holiday pie order Ocala |
| (new) rainbow-springs-breakfast.html | breakfast near Rainbow Springs State Park, where to eat Rainbow River | breakfast before tubing Dunnellon |
| (new) about.html | Front Porch history, family restaurant since 1986 | trust page (E-E-A-T) and the target for author/business schema |

Nearby areas whose searchers drive in: Ocala, Rainbow Lakes Estates, Citrus Springs, Inglis, Crystal River, and visitors to Rainbow Springs State Park and the Rainbow River. Don't build a page for every town. Restaurant city pages for towns they're not in are thin content and they don't rank.

## Phase 0: one-time setup (before Addie runs anything)

### On the site (PAA does this in Claude Code)

| # | Item | Why | Status |
|---|---|---|---|
| 0.1 | **Buy the domain and cut over.** Fix the spelling: `frontporchrestrauntandpieshop.com` is misspelled. Change `BASE` in `_build/build.py`, add `CNAME`, set up DNS in Cloudflare, use https only. | A github.io subdomain will never rank for a local business. | Blocked on Michael |
| 0.2 | **Titles ≤ 60 characters and descriptions 140–160.** Today three of four titles are over 60 (up to 95) and every description is 169–194. | Click-through rate. PAA's own data showed titles and descriptions were the bottleneck. | To do |
| 0.3 | **Remove the self-authored `AggregateRating`** from the Restaurant schema. | Google ignores self-serving review markup on a business's own site, and our playbook bans it (Part D). The 4.4★ line stays in the visible copy. | To do |
| 0.4 | robots.txt: allow the AI crawlers (GPTBot, ClaudeBot, PerplexityBot, …), plus the robots meta `max-image-preview:large`. | Visibility in AI answers and Discover. Free. | To do |
| 0.5 | Add `WebSite` schema, `BreadcrumbList` on inner pages, and `llms.txt`. | Site name in search results, plus GEO. | To do |
| 0.6 | Real 404 page, plus a 192/48px PNG favicon and apple-touch-icon. | Technical hygiene. | To do |
| 0.7 | GA4 with PAA's bot-gate loader. Key events: `phone_click`, `directions_click`, `order_click`. | Calls are the KPI, so we have to count them. | To do |
| 0.8 | Search Console: verify through Cloudflare DNS and submit the sitemap. Bing Webmaster: import from GSC and get the URL Submission API key. | Indexing, and data for Addie. | After 0.1 |
| 0.9 | **Thanksgiving pie page live by 2026-11-06.** Thanksgiving is 2026-11-26, and Google needs time to find the page. | The biggest pie-order week of the year. | Needs Michael's deadline/pickup answers |

### Off-site (a human does these, about 2 hours total)

| # | Item | Who |
|---|---|---|
| H1 | **GBP manager access for PAA.** Record the Place ID and CID. Fix the primary category (Restaurant, or Breakfast restaurant as secondary), hours, menu link → `menu.html`, an order link → `pies.html` with a UTM tag, and a "Pie shop" attribute/secondary category. | Deniz with Michael |
| H2 | Bing Places and Apple Business Connect (10 min each). These feed ChatGPT/Copilot and Siri/Apple Maps. | Deniz |
| H3 | **NAP check, character for character:** "Front Porch Restaurant & Pie Shop · 12039 N Florida Ave, Dunnellon, FL 34434 · (352) 489-4708" on Yelp, TripAdvisor, Facebook, Nextdoor, the Dunnellon Area Chamber of Commerce and the Ocala/Marion County visitor listing. Add each profile URL to the schema's `sameAs`. | Deniz |
| H4 | **Photos.** GBP and the site still use public Google-listing photos. Ask Michael for 10 phone photos of breakfast plates, whole pies and the porch. **Current staff only. No former staff in any photo.** | Michael |
| H5 | Review link: a `/review` short link to the GBP write-review URL, plus a table tent or receipt line: "Loved your pie? Tell Google." | Deniz + Michael |
| H6 | Answer the open questions in `facts.json → unknown_ask_michael`: holiday deadlines, catering, seasonal flavors. | Michael |

## Phase 1: the weekly loop (Addie, every Monday)

Addie is a local model, so the work is split this way: **scripts handle every fact, number and check, and Addie only writes words.** Addie never pushes to the live site. Everything Addie makes is a draft that a human approves.

| When | Job | Who does it | Output |
|---|---|---|---|
| Mon 06:00 | Pull GSC (7 and 28 days, by page and query) and GA4 (calls, directions, order clicks) | script `pull_data.py` | `_seo/data/YYYY-MM-DD.json` |
| Mon 06:05 | Site check: titles, descriptions, H1, JSON-LD parses, sitemap count, links return 200, OG images exist, GPTBot gets 200 | script `site_check.py` | `_seo/weekly/YYYY-MM-DD/site-check.txt` |
| Mon 06:10 | **Weekly report**: 5 lines covering what moved, page-2 queries (positions 8–20), low-CTR pages and site-check failures | Addie (Task A) | `report.md` |
| Mon 06:15 | **2 GBP post drafts**: one breakfast, one pie. Breakfast is always one of the two. | Addie (Task B) | `gbp-posts.md` |
| Mon 06:20 | **Review reply drafts** for every new review in `_seo/inbox/reviews.txt` | Addie (Task C) | `review-replies.md` |
| Mon 06:25 | **1 Facebook post draft** reusing the week's pie or breakfast angle | Addie (Task B) | `facebook.md` |
| Every other Mon | **One page**: a new page from the content queue, or a refresh of an existing page | Addie (Task D) → `validate_draft.py` → `open_pr.sh` | GitHub pull request on branch `addie/YYYY-MM-DD` |
| 1st Mon of month | **Title/description proposals** for pages with ≥ 100 impressions and CTR under 2% | Addie (Task E) → PR | pull request |
| Mon 09:00 | **Human review (15 min)**: read the report, post the GBP/FB drafts, paste review replies into GBP, merge or close the PR, then run Request Indexing in GSC on any merged page | Deniz or Tony | — |

Every draft goes through `validate_draft.py` before a human sees it. The script rejects any price, time, phone number, rating or flavor that isn't in `facts.json`, any staff name, and any banned phrase from `facts.json → never_say`. Local models invent prices. This check stops that in code, not by trusting the model (PAA playbook, Part D: "put the rules in code").

## Content queue (Task D works top to bottom; humans can reorder)

1. `thanksgiving-pies.html`: order deadline, pickup days, the classics (pumpkin, pecan, apple), call to order. **Needs the H6 answers first. Do not draft it with guessed dates.**
2. `rainbow-springs-breakfast.html`: "Breakfast before the Rainbow River." For tourists, with drive time and what's on the plate. (Plan the drive-time line now; check it in Google Maps before publishing.)
3. `about.html`: since 1986, family owned, the no-WiFi chalkboard, Michael's own words if he gives us a quote.
4. `christmas-pies.html`: live by 2026-12-01.
5. Refresh `breakfast.html`: add the 3 most-asked breakfast questions as a visible FAQ (visible text must match the schema).
6. Refresh `pies.html`: one section per signature pie (meringue, Key lime, pecan).
7. Seasonal pie page once Michael names the seasonal flavors.

Every new page follows the playbook template: an H1 that matches the search → a 40–60 word answer paragraph → H2 sections → links to pies.html and breakfast.html → a visible FAQ (4–6 questions) → one call-to-order CTA. Each page also gets its own OG card, a sitemap entry and a `llms.txt` entry. No em dashes.

## Phase 2: monthly and quarterly

- **Monthly (1st Monday):** title/description rewrites (Task E). One new GBP photo set from Michael. Check that review replies are current.
- **Quarterly:** geo-grid rank check for "breakfast Dunnellon" and "pie shop Dunnellon" (PAA seo-maps agent). Re-verify NAP on Bing, Apple and Yelp. Send Michael a one-page report.
- **6 months after cutover:** cadence review. Increase, hold or decrease page output based on the GSC trend.

## What we measure

Record a baseline on cutover day, then track weekly:
- GBP: calls, direction requests, website clicks (from the GBP Performance tab; a human pastes them into `_seo/inbox/gbp-metrics.txt` until API access exists)
- GSC: clicks and average position for the target searches
- GA4: `phone_click`, `order_click`, `directions_click`
- Pie orders per week (ask Michael for a tally, especially Thanksgiving and Christmas)

## Hosting and safety rules

- The site stays on GitHub Pages behind Cloudflare. The Mac Studio only writes drafts and opens pull requests. If the Mac Studio is off, the site is unaffected.
- The Mac Studio uses a **fine-grained PalmettoAI token limited to this one repo** (contents + pull requests). Secrets live in `~/.config/frontporch/` on the Mac and never in the repo. This repo is public.
- Nothing is "live" until it's merged, built and loaded in a browser at the live URL.
- Customer-facing text (posts, replies, pages) always gets a human check. Addie never posts to GBP or Facebook directly.
