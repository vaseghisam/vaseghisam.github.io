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
EMAIL = "sam.vaseghi@wisehouse-publishing.com"
CATALOGUE_DESCRIPTION = (
    "A catalogue of research in mathematics and theoretical physics by Sam Vaseghi, "
    "with abstracts and links to archived preprints and explanatory companions."
)


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
    return f"""<footer class="site-footer">
  <div class="shell footer-grid">
    <p><strong>Sam Vaseghi</strong><br>Wisehouse Science Communication Lab<br>Wisehouse AB · Sweden</p>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p><a href="https://github.com/vaseghisam">GitHub</a> · <a href="https://orcid.org/0009-0006-4105-1949">ORCID</a><br><span class="muted">Catalogue prepared 2 November 2026</span></p>
  </div>
</footer>"""


def card(paper: dict) -> str:
    href = f"/papers/{quote(paper['slug'])}/"
    abstract = paper["abstract"]
    teaser = abstract[:250].rsplit(" ", 1)[0] + "…" if len(abstract) > 250 else abstract
    pdf = paper.get("pdf")
    pdf_link = (
        f'<a href="{href}{quote(pdf)}" type="application/pdf" '
        f'aria-label="Read PDF of {esc(paper["title"])}">Read PDF</a>'
        if pdf else ""
    )
    return f"""<article class="paper-card" data-group="{esc(paper['group'])}" data-search="{esc((paper['title'] + ' ' + paper['abstract'] + ' ' + ' '.join(paper['keywords'])).lower())}">
  <div class="card-top"><span class="eyebrow">{esc(paper['group'])}</span><span class="paper-kind">{esc(paper['kind'])}</span></div>
  <h3><a href="{href}">{esc(paper['title'])}</a></h3>
  <p class="card-abstract">{esc(teaser)}</p>
  <div class="card-bottom"><span>{esc(paper.get('version', ''))} · {esc(formatted_day(paper['version_date']))}</span><div class="card-links">{pdf_link}<a href="{href}" aria-label="Details for {esc(paper['title'])}">Read paper details <span aria-hidden="true">→</span></a></div></div>
</article>"""


def homepage(papers: list[dict]) -> str:
    groups = sorted({p["group"] for p in papers})
    controls = "".join(
        f'<button type="button" class="filter" data-filter="{esc(group)}" aria-pressed="false">{esc(group)}</button>'
        for group in groups
    )
    cards = "\n".join(card(p) for p in papers)
    research_count = sum(p["kind"] == "Research preprint" for p in papers)
    companion_count = sum(p["kind"] == "Explanatory companion" for p in papers)
    companion_label = "explanatory companion" if companion_count == 1 else "explanatory companions"
    return head(
        "Sam Vaseghi | Research papers",
        CATALOGUE_DESCRIPTION,
        BASE + "/",
    ) + f"""<body>
{navigation()}
<main id="main">
  <section class="hero shell">
    <div class="hero-copy">
      <p class="eyebrow accent">Mathematics Knowledge and Connections Program</p>
      <h1>Research papers<br><em>and connections.</em></h1>
      <p class="hero-intro">{esc(CATALOGUE_DESCRIPTION)}</p>
      <div class="hero-actions"><a class="button primary" href="#papers">Explore the papers <span aria-hidden="true">↓</span></a><a class="text-link" href="{ORCID}" rel="me">View ORCID <span aria-hidden="true">↗</span></a></div>
    </div>
    <div class="hero-figure" aria-hidden="true"><div class="figure-grid"><span class="orbit orbit-a"></span><span class="orbit orbit-b"></span><span class="orbit orbit-c"></span><span class="axis axis-a"></span><span class="axis axis-b"></span><span class="figure-dot dot-a"></span><span class="figure-dot dot-b"></span><span class="figure-dot dot-c"></span></div><p>structure<br><span>across fields</span></p></div>
  </section>
  <section class="statement">
    <div class="shell statement-inner"><p class="eyebrow">The catalogue</p><p>Each entry has its own abstract page. The Zenodo links lead to the citable records and version histories.</p><span class="stat"><strong>{research_count}</strong> research preprints<br><strong>{companion_count:02}</strong> {companion_label}</span></div>
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
    <div class="shell about-grid"><h2 id="about-heading" class="eyebrow accent">About the author</h2><div><p>Sam Vaseghi conducts research in mathematics and theoretical physics at Wisehouse Science Communication Lab, Wisehouse AB, Sweden. He develops the mathematical work through the Mathematics Knowledge and Connections Program.</p><p>For the exact archived manuscript, license and version history, follow the Zenodo link on each paper page. The author’s identifier is <a href="{ORCID}" rel="me">ORCID 0009-0006-4105-1949</a>.</p></div></div>
  </section>
</main>
{footer()}
<script src="/assets/catalogue.js" defer></script>
</body></html>"""


def paper_page(paper: dict) -> str:
    url = f"{BASE}/papers/{paper['slug']}/"
    doi = paper.get("doi")
    title = paper["title"]
    publication_date = date.fromisoformat(paper["version_date"])
    year = publication_date.year
    pdf = paper.get("pdf")
    metadata = [
        f'<meta name="citation_title" content="{esc(title)}">',
        f'<meta name="citation_author" content="{esc(AUTHOR)}">',
        f'<meta name="citation_publication_date" content="{publication_date:%Y/%m/%d}">',
    ]
    if doi:
        metadata.append(f'<meta name="citation_doi" content="{esc(doi)}">')
    if pdf:
        metadata.append(f'<meta name="citation_pdf_url" content="{esc(url + quote(pdf))}">')
    extra = "\n  ".join(metadata)
    version = f'Version {esc(paper["version"])}' if paper.get("version") else "Explanatory companion"
    citation_type = "Explanatory companion" if paper["kind"] == "Explanatory companion" else "Preprint"
    if doi:
        cite = f'{AUTHOR}. {title}. {citation_type}, {year}. https://doi.org/{doi}'
    else:
        cite = f'{AUTHOR}. {title}. {citation_type}, {year}. See the linked Zenodo record for its current citation.'
    record_label = paper.get("record_label", "Read the Zenodo record")
    pdf_button = f'<a class="button secondary" href="{quote(pdf)}" type="application/pdf">Read PDF copy <span aria-hidden="true">↗</span></a>' if pdf else ""
    license_url = paper.get("license_url")
    license_record = (
        f'<div><dt>PDF license</dt><dd><a rel="license" href="{esc(license_url)}">CC BY 4.0</a></dd></div>'
        if license_url else ""
    )
    note = f'<p class="record-note">{esc(paper["status_note"])}</p>' if paper.get("status_note") else ""
    keyword_tags = "".join(f"<span>{esc(k)}</span>" for k in paper["keywords"])
    return head(f"{title} | Sam Vaseghi", paper["abstract"][:160], url, extra) + f"""<body>
{navigation("papers")}
<main id="main">
  <article class="article-shell shell">
    <p class="breadcrumb"><a href="/#papers">All papers</a><span aria-hidden="true">/</span>{esc(paper['group'])}</p>
    <header class="article-heading"><p class="eyebrow accent">{esc(paper['kind'])} · {esc(paper['group'])}</p><h1>{esc(title)}</h1><p class="byline"><span class="citation_author">{esc(AUTHOR)}</span> <span class="byline-separator" aria-hidden="true">·</span> Wisehouse Science Communication Lab, Wisehouse AB</p></header>
    <div class="article-layout">
      <div class="article-main"><h2>Abstract</h2><p class="abstract">{esc(paper['abstract'])}</p><h2>Keywords</h2><div class="keywords">{keyword_tags}</div><div class="citation"><h2>Citation</h2><p>{esc(cite)}</p></div></div>
      <aside class="article-aside" aria-label="Paper details"><p class="eyebrow">Paper record</p><dl><div><dt>Type</dt><dd>{esc(paper['kind'])}</dd></div><div><dt>Version</dt><dd>{version}</dd></div><div><dt>Version record date</dt><dd>{esc(formatted_day(paper['version_date']))}</dd></div>{f'<div><dt>DOI</dt><dd><a href="https://doi.org/{esc(doi)}">{esc(doi)}</a></dd></div>' if doi else ''}{license_record}</dl><div class="aside-actions"><a class="button primary" href="{esc(paper['record'])}">{esc(record_label)} <span aria-hidden="true">↗</span></a>{pdf_button}</div>{note}</aside>
    </div>
    <p class="back-link"><a href="/#papers">← Back to all papers</a></p>
  </article>
</main>
{footer()}
</body></html>"""


def main() -> None:
    papers = json.loads((ROOT / "papers.json").read_text(encoding="utf-8"))
    assert papers
    assert len({p["slug"] for p in papers}) == len(papers)
    for paper in papers:
        pdf = paper.get("pdf")
        if pdf and (
            Path(pdf).name != pdf
            or not pdf.endswith(".pdf")
            or not (ROOT / "papers" / paper["slug"] / pdf).is_file()
        ):
            raise ValueError(f"{paper['slug']} must point to a PDF beside its abstract page")
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
