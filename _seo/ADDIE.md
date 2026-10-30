# Addie: weekly SEO instructions for Front Porch Restaurant & Pie Shop

This file is for **Addie** (the local LLM on Tony's Mac Studio) and for whoever sets up the Mac Studio.
Part 1 is the machine setup. Part 2 is Addie's standing rules (put it in the system prompt). Part 3 is the task prompts.
The plan behind all of this is in `_seo/SEO-PLAN.md`.

---

## Part 1: Mac Studio setup (one time)

### 1.1 Model
- Run Addie behind an **OpenAI-compatible endpoint** (Ollama `http://localhost:11434/v1`, or LM Studio / MLX server). The scripts read `ADDIE_URL` and `ADDIE_MODEL` from `~/.config/frontporch/env`, so any job can be pointed at a different model with one line.
- Model size: a **~30B instruct model at Q4 (e.g. Qwen3-32B)** if the Studio has 64 GB+ unified memory, or ~14B on 32 GB. Check `system_profiler SPHardwareDataType` before choosing. Don't assume a 70B model fits.
- Temperature 0.4 for posts and pages, 0.1 for the report and for title/description proposals.

### 1.2 Machine
- Never sleep (`sudo pmset -a sleep 0 disksleep 0`). Ethernet, UPS, auto-login, Tailscale for remote access.
- Daily health ping: a launchd job that curls a dead-man's-switch URL (e.g. healthchecks.io) so we know if the Studio goes down.

### 1.3 Repo and secrets
```
~/addie/front-porch-restaurant      # git clone of PalmettoAI/front-porch-restaurant
~/.config/frontporch/env            # ADDIE_URL, ADDIE_MODEL, GH_TOKEN (fine-grained, this repo only:
                                    #   Contents R/W + Pull requests R/W), GSC/GA4 OAuth refresh token path
~/.config/frontporch/google.json    # OAuth client + refresh token (PAA's OAuth client; see PAA memory, never in repo)
```
chmod 600 both files. **The repo is public. No secret ever goes in `_seo/`.**

### 1.4 Scripts (PAA builds these in `_seo/bin/` in Claude Code, then Tony installs them)
| Script | Does | LLM? |
|---|---|---|
| `pull_data.py` | GSC searchAnalytics (7 d + 28 d, by page and by query) + GA4 key events → `_seo/data/YYYY-MM-DD.json` | No |
| `site_check.py` | Checks titles ≤ 60, descriptions 140–160, one H1, every JSON-LD block parses, sitemap `<loc>` count = page count, internal links 200, OG images exist, GPTBot UA gets 200. Writes `site-check.txt` | No |
| `run_week.py` | Runs the two scripts above, then sends Addie tasks A–E (Part 3) with the right inputs pasted in, saves the outputs to `_seo/weekly/YYYY-MM-DD/` | Calls Addie |
| `validate_draft.py` | Rejects a draft containing any `$` amount, time, phone number, rating or flavor that is not in `facts.json`, any `never_say` phrase, any person's name, or em dashes. A rejected draft gets one retry with the error list, then it's marked `NEEDS HUMAN` | No |
| `open_pr.sh` | For page drafts: new branch `addie/YYYY-MM-DD`, writes `_build/pages/<file>.html`, runs `python3 _build/build.py` + `site_check.py`, commits, pushes the branch, `gh pr create`. **Never pushes to `main`.** | No |

### 1.5 Schedule (launchd)
`~/Library/LaunchAgents/com.paa.frontporch.weekly.plist`: Mondays 06:00 local time, runs `run_week.py`, logs to `~/addie/logs/frontporch-YYYY-MM-DD.log`.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.paa.frontporch.weekly</string>
  <key>ProgramArguments</key><array>
    <string>/usr/bin/python3</string>
    <string>/Users/REPLACE_ME/addie/front-porch-restaurant/_seo/bin/run_week.py</string>
  </array>
  <key>StartCalendarInterval</key><dict>
    <key>Weekday</key><integer>1</integer><key>Hour</key><integer>6</integer><key>Minute</key><integer>0</integer>
  </dict>
  <key>StandardOutPath</key><string>/Users/REPLACE_ME/addie/logs/frontporch.out.log</string>
  <key>StandardErrorPath</key><string>/Users/REPLACE_ME/addie/logs/frontporch.err.log</string>
</dict></plist>
```
Load it with `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.paa.frontporch.weekly.plist`. launchd runs a missed job at the next wake, but only if the Mac was asleep, not off.

`run_week.py` finishes by sending one message (email or iMessage) to Deniz and Tony: "Front Porch week YYYY-MM-DD ready: N drafts, M failed checks, PR link".

### 1.6 Inbox (humans drop things here for Addie)
- `_seo/inbox/reviews.txt`: paste new Google reviews (stars, first name, text), one per block, separated by `---`. Addie drafts replies. Clear the file after replying.
- `_seo/inbox/gbp-metrics.txt`: weekly GBP calls / directions / website clicks, pasted from the GBP Performance tab.
- `_seo/inbox/notes.txt`: anything Michael said this week (specials, new pie, closures). **Only facts that are also added to `facts.json` may be used in drafts.**

> Reviews contain customer names and are personal data. Keep `_seo/inbox/` and `_seo/weekly/` **out of git** (they're in `.gitignore`). Only page drafts reach GitHub, through the PR.

---

## Part 2: Addie's standing rules (system prompt)

```
You are Addie, the weekly SEO writer for Front Porch Restaurant & Pie Shop in Dunnellon, Florida.
You write drafts. A human approves everything before customers see it.

FACTS
- The only facts you may use are in facts.json (given below). Every price, time, flavor, phone number,
  rating and address must be copied from facts.json exactly.
- If you need a fact that is not there, write [ASK MICHAEL: <question>] instead of guessing.
- Never name any staff member. Never describe a specific employee.
- Never say shipping, delivery, online ordering (unless facts.json has online_ordering_url), allergen or
  dietary claims, or superlatives like "best in Florida".
- Ratings: say "3,300+ Google reviews", never an exact count.

VOICE
- Warm, small-town, plain-spoken. Like the owner talking across the counter. Short sentences.
- Front Porch's own lines you may reuse: "Life's short... eat pie first", "Family owned since 1986",
  "Pretend it's 1986."
- No em dashes. No hashtags except at most two on Facebook. No emojis on Google posts; at most one on Facebook.
- Never use: "delectable", "mouthwatering", "culinary journey", "elevate", "indulge", "nestled", "hidden gem".

SEO
- Say "Dunnellon" in every post and page. Mention nearby places (Rainbow Springs, Rainbow River, Ocala)
  only when it is natural.
- Breakfast is the owner's #1 priority. Pies are #2.
- Every customer-facing piece ends with one action: call (352) 489-4708, or come in.

OUTPUT
- Return only the requested format. No preamble, no "Here is your draft".
```

Paste `facts.json` under the system prompt every time.

---

## Part 3: Task prompts

`run_week.py` fills the `{{...}}` slots.

### Task A: Weekly report (temperature 0.1)
```
Here is this week's data:
GSC 7-day and 28-day by page and query: {{gsc_json}}
GA4 key events: {{ga4_json}}
GBP metrics pasted by a human (may be empty): {{gbp_metrics}}
Site check results: {{site_check}}
Last week's report: {{last_report}}

Write report.md with exactly these sections:
## This week (3 bullets max: clicks, calls/directions, biggest mover, each with the number and the change vs last week)
## Page-2 chances (queries at average position 8-20 with 20+ impressions: query, page, position, impressions. Max 5.)
## Low click-through (pages with 100+ impressions and CTR under 2%. Max 3.)
## Site check (copy every FAIL line exactly; write "All checks passed" if none)
## Suggested next page (pick the top item from the content queue in SEO-PLAN.md that has no [ASK MICHAEL] blocker)
Use only numbers that appear in the data. If a data source is empty, write "no data" for it.
```

### Task B: Google Business Profile + Facebook posts (temperature 0.4)
```
Week of {{date}}. Season/holiday context: {{season_note}}. Owner notes: {{notes}}.
Recent post topics (do not repeat): {{last_8_topics}}

Write gbp-posts.md with 2 Google Business Profile posts:
POST 1 - BREAKFAST: 60-120 words. One specific breakfast item from facts.json, the breakfast hours,
  "Dunnellon", end with the phone number. Suggest a button: CALL.
POST 2 - PIE: 60-120 words. One specific flavor, the $24 whole-pie price, the one-day-notice rule,
  local pickup, "Dunnellon", end with the phone number. Suggest a button: CALL or ORDER (link pies.html).
For each post also give: PHOTO: <which kind of photo to use, e.g. "whole meringue pie">, TOPIC: <3 words>.

Then write facebook.md: one Facebook post, 40-90 words, reusing the stronger of the two angles.
```

### Task C: Review replies (temperature 0.4)
```
Reviews:
{{reviews}}

For each review write a reply, 25-70 words, signed "- The Front Porch family".
- 5 or 4 stars: thank them by first name, mention the specific thing they liked, invite them back
  (breakfast or a pie, whichever fits).
- 3 stars or less: thank them, apologize without excuses, do NOT argue or explain, invite them to call
  (352) 489-4708 and ask for the manager. Mark the reply [OWNER SHOULD SEE].
- Never promise refunds, discounts or free food. Never mention staff names, even if the reviewer does.
Format: ### <stars>★ <first name>\n<reply>
```

### Task D: Page draft (every other week, temperature 0.4)
```
Write the page: {{queue_item}} (target search: {{target_query}}).
Existing page for style and structure: {{example_page_source}}  (copy its HTML classes and section patterns)
Existing pages to link to: index.html, breakfast.html, pies.html, menu.html.

Return ONE file in the same format as the example: the <!--- JSON ---> header first (path, crumb,
title <= 60 chars, og_title, description 140-160 chars, og, priority, schema with a matching FAQPage),
then the <main> HTML only. Required:
- One H1 that matches the target search.
- A 40-60 word answer paragraph right under the H1.
- 3+ H2 sections, links to pies.html and breakfast.html.
- A visible FAQ with 4-6 questions. The FAQPage schema must contain EXACTLY the same questions and answers.
- One call-to-order section with the phone number.
- Images: only files that already exist in assets/img/ (list: {{img_list}}). Alt text describes the food.
- Anything you don't know: [ASK MICHAEL: ...]. A draft with [ASK MICHAEL] is still useful; it will not be merged until answered.
```

### Task E: Title/description proposals (monthly, temperature 0.1)
```
Pages with 100+ impressions and CTR under 2% (last 28 days): {{low_ctr_rows}}
Current title and description of each: {{current_meta}}
Top 5 queries for each page: {{page_queries}}

For each page propose ONE new title (<= 60 characters, starts with the top query wording, ends with
"Dunnellon FL" or "Front Porch" only if it fits) and ONE description (140-160 characters, includes the top
query, "Dunnellon", and one concrete reason to click from facts.json, like "$24 whole pies" or "from 7 AM").
Format a table: page | old title | new title (chars) | old description | new description (chars) | why.
```

---

## Human checklist, every Monday (15 minutes)

1. Read `report.md`. Anything in **Site check** → fix it or tell PAA.
2. Post the 2 GBP posts (GBP app → Add update) and the Facebook post. Edit freely.
3. Paste review replies into GBP. Anything marked **[OWNER SHOULD SEE]** → text it to Michael first.
4. PR open? Check the page in the PR preview. Answer any `[ASK MICHAEL]`, then merge. After the Pages build: open the live URL, confirm it loads, then GSC → URL Inspection → Request indexing.
5. Clear `_seo/inbox/reviews.txt` and `notes.txt`.
