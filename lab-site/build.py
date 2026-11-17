"""Build the static handbook and downloads using Python's standard library."""
from html import escape
from pathlib import Path
import re
from shutil import copy2
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
DOWNLOADS = DIST / "downloads"
BUNDLE = DOWNLOADS / "devsecops-lab-handbook.zip"

LABS = [
    ("Git", "Track, branch, merge, and publish a repository."),
    ("GitHub", "Review a pull request and resolve a merge conflict."),
    ("Jenkins", "Install Jenkins, then compile and deploy a Java class."),
    ("Jenkins", "Compare declarative and scripted pipeline runs."),
    ("Docker", "Work with images, containers, networks, and volumes."),
    ("Docker Hub", "Build a custom Nginx image and publish a tag."),
    ("Ansible", "Manage Nginx over SSH and deploy a test page."),
    ("Prometheus", "Scrape metrics and demonstrate an alert lifecycle."),
    ("Snyk", "Scan dependencies, upgrade a package, and rescan."),
    ("SonarQube", "Review code quality findings and rerun analysis."),
    ("Threat Dragon", "Draw a data flow and document STRIDE threats."),
    ("Terraform", "Plan, deploy, inspect, and remove Azure infrastructure."),
]


def inline(text):
    """Render the guide format's inline links and backtick code."""
    escaped = escape(text)
    return re.sub(r"\x60([^\x60]+)\x60|\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: f"<code>{m[1]}</code>" if m[1]
                  else f'<a href="{m[3]}">{m[2]}</a>', escaped)


def read_guide(slug):
    title, meta, body = (ROOT / "guides" / f"{slug}.md").read_text(encoding="utf-8").split("\n", 2)
    return title.removeprefix("# "), meta.removeprefix("> "), body


def render_blocks(body, starter):
    sections = []
    blocks = []
    for block in re.split(r"(~~~[^\n]*\n[\s\S]*?\n~~~)", body.strip()):
        if block.startswith("~~~"):
            label, _, code = block[3:-4].partition("\n")
            blocks.append(code_block(label, code))
        else:
            render_text(block, starter, sections, blocks)
    return sections, "\n".join(blocks)


def render_text(text, starter, sections, blocks):
    for block in re.split(r"\n{2,}", text.strip()):
        if block.startswith("## "):
            heading, _, remainder = block.partition("\n")
            title = heading.removeprefix("## ")
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            sections.append((slug, title))
            blocks.append(f'<h2 id="{slug}">{escape(title)}</h2>')
            block = remainder
        while block:
            line, _, remainder = block.partition("\n")
            if line.startswith("@file "):
                path = line.removeprefix("@file ")
                blocks.append(code_block(path, (starter / path).read_text(encoding="utf-8").rstrip("\n")))
                block = remainder
            elif line.startswith("- "):
                items = "".join(f"<li>{inline(item[2:])}</li>" for item in block.splitlines())
                blocks.append(f"<ul>{items}</ul>")
                break
            else:
                prose = re.split(r"\n(?=@file )", block, maxsplit=1)
                blocks.append(f"<p>{inline(prose[0])}</p>")
                block = prose[1] if len(prose) > 1 else ""


def code_block(label, text):
    label = escape(label)
    return (f'<figure class="code"><figcaption><span>{label}</span>'
            f'<button type="button" data-copy hidden aria-label="Copy {label}">Copy</button>'
            f'</figcaption><pre tabindex="0" role="region" aria-label="{label}">'
            f'<code>{escape(text)}</code></pre></figure>')


def page(title, content, current):
    links = []
    for href, label in [("index.html", "Lab index"), ("setup.html", "Windows setup")]:
        active = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{active}>{label}</a>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · DevSecOps Labs</title>
<link rel="stylesheet" href="site.css">
<script defer src="site.js"></script>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="top"><div class="wrap top-inner">
<a class="brand" href="index.html"><span aria-hidden="true">&gt;_</span> DevSecOps Labs</a>
<nav aria-label="Primary navigation">{"".join(links)}</nav>
</div></header>
<main class="wrap">{content}</main>
<footer class="wrap footer"><a href="index.html">Lab index</a><a href="setup.html">Windows setup</a></footer>
</body>
</html>"""


def index_page(offline=False):
    cards = []
    for number, (tool, summary) in enumerate(LABS, 1):
        slug = f"{number:02}"
        title, meta, _ = read_guide(slug)
        cards.append(f"""<li class="lab-card" data-keywords="{escape(meta)}">
<a href="{slug}.html">
<span class="lab-meta"><span>Lab {slug}</span><span>{tool}</span></span>
<h3>{escape(title)}</h3><p>{escape(summary)}</p><span class="open">Open lab <span aria-hidden="true">↗</span></span>
</a></li>""")
    download = ('<a class="button" href="downloads/devsecops-lab-handbook.zip" download>'
                'Download offline handbook <span aria-hidden="true">↓</span></a>') if not offline else ""
    return f"""<section class="hero">
<div class="hero-copy">
<h1 id="content" tabindex="-1">DevSecOps lab<br class="wide-only"> handbook</h1>
<p>Twelve practicals for Windows and WSL2. Follow the steps, copy commands, and check the results during your demo.</p>
<div class="actions"><a class="button primary" href="setup.html">Set up Windows <span aria-hidden="true">→</span></a>
{download}</div>
</div>
<aside class="demo-panel">
<h2>Prepare for your demo</h2>
<ol><li>Open a lab and check its prerequisites.</li><li>Download its starter files, where provided.</li><li>Follow the steps, then jump to <strong>Show the professor</strong>.</li></ol>
</aside>
</section>
<section>
<div class="index-head"><h2>Lab index</h2>
<search hidden><label for="filter">Find a lab</label>
<input id="filter" type="search" placeholder="e.g. Docker or 08"></search></div>
<p id="no-results" hidden>No labs match your search.</p>
<ul class="lab-grid">""" + "\n".join(cards) + "</ul></section>"


def guide_page(slug):
    title, meta, body = read_guide(slug)
    starter = ROOT / "starters" / f"lab-{slug}"
    sections, content = render_blocks(body, starter)
    lab = slug != "setup"
    number = f'<p class="eyebrow">Practical {slug} / 12</p>' if lab else ""
    actions = []
    if starter.is_dir():
        actions.append(f'<a class="button primary" download href="downloads/lab-{slug}.zip">Download lab {slug} starter ZIP <span aria-hidden="true">↓</span></a>')
    if lab:
        actions.append('<a class="button" href="#show-the-professor">Show the professor <span aria-hidden="true">↘</span></a>')
    files = ""
    if starter.is_dir():
        paths = sorted(p.relative_to(starter).as_posix() for p in starter.rglob("*") if p.is_file())
        names = "".join(f"<li><code>{escape(path)}</code></li>" for path in paths)
        files = f'<details class="file-list"><summary>Files in lab-{slug}/</summary><ul>{names}</ul></details>'
    toc = "".join(f'<li><a href="#{key}">{escape(label)}</a></li>' for key, label in sections)
    return title, f"""<header class="guide-header">
{number}<h1 id="content" tabindex="-1">{escape(title)}</h1>
<p class="prereq">{escape(meta)}</p>
<div class="actions">{"".join(actions)}</div>{files}
</header>
<div class="guide-layout">
<nav class="toc" aria-label="On this page"><h2>On this page</h2><ul>{toc}</ul></nav>
<article class="guide">{content}</article>
</div>"""


def make_archive(path, files, relative_to):
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        for file in sorted(files):
            archive.write(file, file.relative_to(relative_to).as_posix())


def build():
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    for asset in (ROOT / "web").iterdir():
        copy2(asset, DIST / asset.name)
    (DIST / "index.html").write_text(page("Lab index", index_page(), "index.html"), encoding="utf-8")
    for slug in ["setup", *(f"{n:02}" for n in range(1, len(LABS) + 1))]:
        title, content = guide_page(slug)
        filename = f"{slug}.html"
        (DIST / filename).write_text(page(title, content, filename), encoding="utf-8")
    for folder in sorted((ROOT / "starters").iterdir()):
        files = [p for p in folder.rglob("*") if p.is_file()]
        make_archive(DOWNLOADS / f"{folder.name}.zip", files, folder.parent)
    with ZipFile(BUNDLE, "w", ZIP_DEFLATED) as archive:
        archive.writestr("index.html", page("Lab index", index_page(offline=True), "index.html"))
        for file in sorted(DIST.rglob("*")):
            if file.is_file() and file not in {BUNDLE, DIST / "index.html"}:
                archive.write(file, file.relative_to(DIST).as_posix())
    print(f"Built {len(LABS)} labs and downloads in {DIST}")


if __name__ == "__main__":
    build()
