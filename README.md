# commuted.app

Static HTML and CSS, deployed via Cloudflare Pages with GitHub auto-deploy.

## Structure

```
.
├── index.html         marketing page
├── privacy.html       privacy policy, linked from the app's About screen
├── support.html       support page and FAQ
├── event/duo.html     1.1 In-App Event page (deep link target)
├── styles.css         shared stylesheet
├── scripts.js         the hero's commute and the cost bar
├── _headers           Cloudflare Pages cache and security headers
├── robots.txt
├── sitemap.xml
└── images/            screenshots and the iPhone Duo image
```

## Design

The road at first light: the top of each page is asphalt running to signal
teal, the app's own arc, and below it cream paper. Archivo, narrowed like
road signage, for everything set; DM Mono for figures and labels; Fraunces
only inside the copy of the app's home screen, where the app uses it.

`scripts.js` runs the home page: the hero's copy of the app records one leg
by itself and then lets the visitor start and stop commutes, and the cost
bar fills fuel first, then the rest of what a car costs.

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
