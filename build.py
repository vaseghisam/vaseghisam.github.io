#!/usr/bin/env python3
"""Render the portable publication catalogue from papers.json."""

from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
BASE = "https://vaseghisam.github.io"
AUTHOR = "Sam Vaseghi"
ORCID = "https://orcid.org/0009-0006-4105-1949"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def formatted_day(value: str) -> str:
    return date.fromisoformat(value).strftime("%-d %B %Y")


def head(title: str, description: str, canonical: str, extra: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="stylesheet" href="/assets/style.css">
  {extra}
</head>
"""


def navigation(active: str = "") -> str:
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="shell nav-row">
    <a class="brand" href="/" aria-label="Sam Vaseghi, home"><span class="brand-mark" aria-hidden="true">SV<span>.</span></span><span>Sam Vaseghi<small>Research papers</small></span></a>
    <nav aria-label="Main navigation">
      <a {'aria-current="page"' if active == "papers" else ''} href="/#papers">Papers</a>
      <a {'aria-current="page"' if active == "about" else ''} href="/#about">About</a>
      <a href="{ORCID}" rel="me">ORCID <span aria-hidden="true">↗</span></a>
    </nav>
  </div>
</header>"""


def footer() -> str:
    return """<footer class="site-footer">
  <div class="shell footer-grid">
    <p><strong>Sam Vaseghi</strong><br>Wisehouse Science Communication Lab<br>Wisehouse AB · Sweden</p>
    <p>Preprints and explanatory work are linked to their Zenodo records. A repository deposit or submission is not a journal acceptance.</p>
    <p><a href="https://github.com/vaseghisam">GitHub</a> · <a href="https://orcid.org/0009-0006-4105-1949">ORCID</a><br><span class="muted">Catalogue prepared 2 November 2026</span></p>
  </div>
</footer>"""


def card(paper: dict) -> str:
    href = f"/papers/{quote(paper['slug'])}/"
    abstract = paper["abstract"]
    teaser = abstract[:250].rsplit(" ", 1)[0] + "…" if len(abstract) > 250 else abstract
    return f"""<article class="paper-card" data-group="{esc(paper['group'])}" data-search="{esc((paper['title'] + ' ' + paper['abstract'] + ' ' + ' '.join(paper['keywords'])).lower())}">
  <div class="card-top"><span class="eyebrow">{esc(paper['group'])}</span><span class="paper-kind">{esc(paper['kind'])}</span></div>
  <h3><a href="{href}">{esc(paper['title'])}</a></h3>
  <p class="card-abstract">{esc(teaser)}</p>
  <div class="card-bottom"><span>{esc(paper.get('version', ''))} · {esc(formatted_day(paper['version_date']))}</span><a href="{href}" aria-label="Details for {esc(paper['title'])}">Read paper details <span aria-hidden="true">→</span></a></div>
</article>"""


def homepage(papers: list[dict]) -> str:
    groups = sorted({p["group"] for p in papers})
    controls = "".join(
        f'<button type="button" class="filter" data-filter="{esc(group)}" aria-pressed="false">{esc(group)}</button>'
        for group in groups
    )
    cards = "\n".join(card(p) for p in papers)
    return head(
        "Sam Vaseghi | Research papers",
        "Research preprints and mathematical expositions by Sam Vaseghi, with stable Zenodo records.",
        BASE + "/",
    ) + f"""<body>
{navigation()}
<main id="main">
  <section class="hero shell">
    <div class="hero-copy">
      <p class="eyebrow accent">Mathematics Knowledge and Connections Program</p>
      <h1>Research papers<br><em>and connections.</em></h1>
      <p class="hero-intro">A catalogue of mathematical research preprints by Sam Vaseghi, with abstracts and links to the archived versions. It also includes an explanatory companion and a related physics preprint.</p>
      <div class="hero-actions"><a class="button primary" href="#papers">Explore the papers <span aria-hidden="true">↓</span></a><a class="text-link" href="{ORCID}" rel="me">View ORCID <span aria-hidden="true">↗</span></a></div>
    </div>
    <div class="hero-figure" aria-hidden="true"><div class="figure-grid"><span class="orbit orbit-a"></span><span class="orbit orbit-b"></span><span class="orbit orbit-c"></span><span class="axis axis-a"></span><span class="axis axis-b"></span><span class="figure-dot dot-a"></span><span class="figure-dot dot-b"></span><span class="figure-dot dot-c"></span></div><p>structure<br><span>across fields</span></p></div>
  </section>
  <section class="statement">
    <div class="shell statement-inner"><p class="eyebrow">The catalogue</p><p>Each entry has its own abstract page. Zenodo holds the citable record and version history; this site makes the papers easier to browse together.</p><span class="stat"><strong>13</strong> MKCP research preprints<br><strong>01</strong> explanatory companion<br><strong>01</strong> related physics preprint</span></div>
  </section>
  <section id="papers" class="papers-section shell" aria-labelledby="papers-heading">
    <div class="section-heading"><div><p class="eyebrow accent">Publications</p><h2 id="papers-heading">Browse the papers</h2></div><p>Public preprint records are listed here. Repository hosting does not indicate peer review.</p></div>
    <div class="browse-tools">
      <label class="search-label" for="paper-search">Search title, abstract or keyword<input id="paper-search" type="search" placeholder="Search the catalogue…" autocomplete="off"></label>
      <div class="filters" role="group" aria-label="Filter by subject"><button type="button" class="filter selected" data-filter="all" aria-pressed="true">All subjects</button>{controls}</div>
      <p class="result-count" id="result-count" aria-live="polite">{len(papers)} entries</p>
    </div>
    <div class="paper-grid" id="paper-grid">{cards}</div>
    <p class="no-results" id="no-results" hidden>No papers match this search.</p>
  </section>
  <section id="about" class="about-section" aria-labelledby="about-heading">
    <div class="shell about-grid"><div><p class="eyebrow accent">About the author</p><h2 id="about-heading">Sam Vaseghi</h2></div><div><p>Sam Vaseghi develops mathematical research through the Mathematics Knowledge and Connections Program at Wisehouse Science Communication Lab, Wisehouse AB, Sweden. This catalogue collects the program’s public preprints, an explanatory companion, and one related physics preprint.</p><p>For the exact archived manuscript, license and version history, follow the Zenodo link on each paper page. The author’s identifier is <a href="{ORCID}" rel="me">ORCID 0009-0006-4105-1949</a>.</p></div></div>
  </section>
</main>
{footer()}
<script src="/assets/catalogue.js" defer></script>
</body></html>"""


def paper_page(paper: dict) -> str:
    url = f"{BASE}/papers/{paper['slug']}/"
    doi = paper.get("doi")
    title = paper["title"]
    publication_meta = f'<meta name="citation_publication_date" content="{paper["version_date"][:4]}">'
    doi_meta = f'<meta name="citation_doi" content="{esc(doi)}">' if doi else ""
    pdf = paper.get("pdf")
    pdf_meta = f'<meta name="citation_pdf_url" content="{esc(url + pdf)}">' if pdf else ""
    extra = f'<meta name="citation_title" content="{esc(title)}"><meta name="citation_author" content="Sam Vaseghi">{publication_meta}{doi_meta}{pdf_meta}'
    version = f'Version {esc(paper["version"])}' if paper.get("version") else "Explanatory companion"
    citation_type = "Explanatory companion" if paper["kind"] == "Explanatory companion" else "Preprint"
    if doi:
        cite = f'Sam Vaseghi. {title}. {citation_type}, 2026. https://doi.org/{doi}'
    else:
        cite = f'Sam Vaseghi. {title}. {citation_type}, 2026. See the linked Zenodo record for its current citation.'
    record_label = paper.get("record_label", "Read the Zenodo record")
    pdf_button = f'<a class="button secondary" href="{esc(pdf)}" type="application/pdf">Read PDF copy <span aria-hidden="true">↗</span></a>' if pdf else ""
    note = f'<p class="record-note">{esc(paper["status_note"])}</p>' if paper.get("status_note") else ""
    keyword_tags = "".join(f"<span>{esc(k)}</span>" for k in paper["keywords"])
    return head(f"{title} | Sam Vaseghi", paper["abstract"][:160], url, extra) + f"""<body>
{navigation("papers")}
<main id="main">
  <article class="article-shell shell">
    <p class="breadcrumb"><a href="/#papers">All papers</a><span aria-hidden="true">/</span>{esc(paper['group'])}</p>
    <header class="article-heading"><p class="eyebrow accent">{esc(paper['kind'])} · {esc(paper['group'])}</p><h1>{esc(title)}</h1><p class="byline">Sam Vaseghi <span aria-hidden="true">·</span> Wisehouse Science Communication Lab</p></header>
    <div class="article-layout">
      <div class="article-main"><h2>Abstract</h2><p class="abstract">{esc(paper['abstract'])}</p><h2>Keywords</h2><div class="keywords">{keyword_tags}</div><div class="citation"><h2>Citation</h2><p>{esc(cite)}</p></div></div>
      <aside class="article-aside" aria-label="Paper details"><p class="eyebrow">Paper record</p><dl><div><dt>Type</dt><dd>{esc(paper['kind'])}</dd></div><div><dt>Version</dt><dd>{version}</dd></div><div><dt>Version record date</dt><dd>{esc(formatted_day(paper['version_date']))}</dd></div>{f'<div><dt>DOI</dt><dd><a href="https://doi.org/{esc(doi)}">{esc(doi)}</a></dd></div>' if doi else ''}</dl><div class="aside-actions"><a class="button primary" href="{esc(paper['record'])}">{esc(record_label)} <span aria-hidden="true">↗</span></a>{pdf_button}</div>{note}</aside>
    </div>
    <p class="back-link"><a href="/#papers">← Back to all papers</a></p>
  </article>
</main>
{footer()}
</body></html>"""


def main() -> None:
    papers = json.loads((ROOT / "papers.json").read_text(encoding="utf-8"))
    assert len(papers) == 15
    assert len({p["slug"] for p in papers}) == len(papers)
    (ROOT / "index.html").write_text(homepage(papers), encoding="utf-8")
    for paper in papers:
        directory = ROOT / "papers" / paper["slug"]
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(paper_page(paper), encoding="utf-8")
    urls = [BASE + "/"] + [BASE + f"/papers/{p['slug']}/" for p in papers]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{esc(u)}</loc></url>\n" for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print(f"Rendered {len(papers)} paper pages and homepage.")


if __name__ == "__main__":
    main()
