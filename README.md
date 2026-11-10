# Sam Vaseghi — research papers

A portable, static catalogue of Sam Vaseghi's research in mathematics and theoretical physics. It contains twenty-two research preprints and two explanatory companions. Each entry has a local PDF copy matched to its CC BY 4.0 Zenodo record. Zenodo holds the archival records.

## Preview and edit

Open `index.html` in a browser, or serve the repository root with `python3 -m http.server 8000`. The HTML pages use root-relative links, so a local server is preferable for full navigation. Edit `papers.json`, then run `python3 build.py` to regenerate the homepage, paper pages, sitemap and robots file. The rendered HTML is committed so the website does not depend on Python at serving time. There are no third-party runtime dependencies.

## GitHub Pages setup

1. Create a **public** repository named `vaseghisam.github.io` under the `vaseghisam` GitHub account.
2. Upload the contents of this directory to the repository root on the `main` branch.
3. In **Settings → Pages**, select **Deploy from a branch**, **main**, and **/(root)**. The site address will be `https://vaseghisam.github.io/`.

The `.nojekyll` file asks Pages to serve the already-rendered files directly. If the owner or address changes, update `BASE` in `build.py`, rebuild, and inspect canonical and sitemap URLs.

Within an extracted source snapshot, run `sha256sum -c SHA256SUMS` to check its files.

Each paper page includes scholarly citation metadata. When adding an approved local PDF, place it beside the paper's `index.html` and set the `pdf` field in `papers.json` to its filename. The build adds the full-text metadata and links from the catalogue and paper page.

## Record notes

Each entry cites the exact archived version. Before updating a copy, check the Zenodo record's DOI, license, and file checksum. The Golden–Thompson page records the reported HAL moderation status on 2 November 2026.

## Continuity

Keep a second clone of this Git repository and archive substantive site releases, including rendered HTML, source data, licensed PDF bytes and checksums. The paper archives remain at Zenodo. A second trusted administrator and optional independent mirror can be added after the owner chooses them.
