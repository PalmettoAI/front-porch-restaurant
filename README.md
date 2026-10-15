# Front Porch Restaurant & Pie Shop — website

Client site for Front Porch Restaurant & Pie Shop, 12039 N Florida Ave, Dunnellon, FL 34434 · (352) 489-4708.
Built by Palmetto AI Automation. Hosted on GitHub Pages: https://palmettoai.github.io/front-porch-restaurant/

## Pages
| File | What it is |
|---|---|
| `index.html` | Home |
| `pies.html` | Pie Shop: whole-pie ordering for local pickup (the main ask) |
| `breakfast.html` | Full breakfast menu, built to rank for "breakfast Dunnellon" |
| `menu.html` | Lunch & supper menu |

Menu prices come from the restaurant's current printed menu, which shows **cash prices**.

## Turning on online ordering (SkyTab / Shift4)
Open `assets/site.js` and paste the SkyTab online-ordering link into `ORDER_URL` at the top:

```js
var ORDER_URL = "https://...";
```

Every "Order" button switches from "Call to order" to the online link. No other edits are needed.

## Editing pages
The HTML pages are **generated**. Edit the source in `_build/pages/*.html` (and the shared header, footer and SEO in `_build/build.py`), then run:

```
python3 _build/build.py
```

GitHub Pages ignores `_build/` because the folder name starts with an underscore, so it is never served.

**Moving to the real domain:** change `BASE` in `_build/build.py`, re-run the build, and add a `CNAME` file.

## Assets
- `assets/site.css` and `assets/site.js` are shared by every page. After editing either one, bump `VER` in `build.py` so browsers load the new copy.
- `assets/img/*.webp` are the optimized photos. `assets/og/*.jpg` are the 1200×630 social share cards; their template is `_build/og.html`.
- Photos come from public Google listing images. Swap in the owner's own photos when we get them, especially breakfast shots.
