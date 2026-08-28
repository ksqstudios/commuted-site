# commuted.app

Static HTML and CSS, deployed via Cloudflare Pages with GitHub auto-deploy.

## Structure

```
.
├── index.html         marketing page
├── privacy.html       privacy policy, linked from the app's About screen
├── support.html       support page and FAQ
├── styles.css         shared stylesheet
├── _headers           Cloudflare Pages cache and security headers
├── robots.txt
├── sitemap.xml
├── fonts/             Fraunces_72pt-Regular.ttf
└── images/            screenshots
```

## Fonts

Fraunces, IBM Plex Mono and Inter load from Google Fonts in each page head,
matching the other sites. Fraunces is used for the wordmark and the two
gradient card figures only; Plex Mono carries eyebrows and data; Inter does
everything else.

## Assets to drop in

| File | Size | Notes |
|---|---|---|
| `images/01.png` | ~600x1300 | Home screen, week total |
| `images/02.png` | ~600x1300 | A commute running |
| `images/03.png` | ~600x1300 | History |
| `images/04.png` | ~600x1300 | Mileage rate screen |
| `og-image.png` | 1200x630 | Open Graph preview. Run `python3 make_og.py` after apple-touch-icon.png is in place. |
| `favicon.png` | 32x32 | |
| `apple-touch-icon.png` | 180x180 | Also used as the masthead mark |

Use frameless captures for `images/`, not the App Store composites: the site
adds its own rounded corners and shadow, and the captions would be duplicated.

## Deployment

Cloudflare Pages, connected to this repo. Build command: none. Output
directory: `/`. Deploys on push to `main`.

Custom domain `commuted.app` set in Cloudflare Pages, Custom domains.

Cloudflare serves `.html` at the path-stripped URL, so `/privacy` and
`/support` work without the extension. The app's About screen links to
`/privacy`, and App Store Connect points at both.

## Analytics

None. The privacy policy says the site collects nothing, so keep it that way.
