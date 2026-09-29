#!/usr/bin/env python3
"""Verify a rendered resume/cover-letter PDF against its markdown source.

Usage:
    python3 tools/verify_resume_pdf.py "<markdown path>" "<pdf path>"

Every expectation is derived from the markdown source, not hardcoded contact
info, so this covers both resumes and cover letters with no mode flag.

Exit code is non-zero if any FAIL-severity check fails. WARN-severity checks
are reported but do not affect the exit code.

Requires pdftotext, pdfinfo, pdftohtml (poppler-utils). No pip dependencies.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

FIDELITY_FLOOR = 0.90
MAX_PAGES = 2
# Smallest allowed white border on any side of any page, in PDF points (72/inch).
# ~7.8mm. The render command sets 16-18mm; a --pdf-options call that forgets the
# margin block drops it to ~0, putting text flush against the paper edge. This
# floor sits well below any deliberate margin and well above that failure.
MIN_MARGIN_PT = 22

REQUIRED_TOOLS = {
    "pdftotext": "poppler-utils",
    "pdfinfo": "poppler-utils",
    "pdftohtml": "poppler-utils",
}


@dataclass
class CheckResult:
    name: str
    severity: str  # "FAIL" or "WARN"
    passed: bool
    detail: str


def check_tools_available() -> None:
    missing = [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]
    if missing:
        pkgs = sorted({REQUIRED_TOOLS[t] for t in missing})
        print(
            f"Missing required tool(s): {', '.join(missing)}. "
            f"Install package(s): {', '.join(pkgs)} (poppler-utils on most distros).",
            file=sys.stderr,
        )
        sys.exit(2)


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def extract_source_links(md_text: str) -> set[str]:
    """Pull every markdown link target and mailto from the source."""
    links = set(re.findall(r"\]\((https?://[^)]+|mailto:[^)]+)\)", md_text))
    return links


def strip_markdown(md_text: str) -> str:
    """Reduce markdown to plain words, matching what pdftotext would extract."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md_text)  # links -> text
    text = re.sub(r"[#*_`>|]", " ", text)  # md syntax
    text = re.sub(r"^\s*[-+]\s+", " ", text, flags=re.MULTILINE)  # bullets
    return text


def check_text_extracts(pdf_path: Path) -> CheckResult:
    text = run(["pdftotext", str(pdf_path), "-"])
    ok = len(text.strip()) > 0
    return CheckResult("Text extracts non-empty", "FAIL", ok,
                        "PDF produced no extractable text" if not ok else "ok")


def header_block(md_text: str) -> list[str]:
    """Non-empty lines between the H1 and the first section heading."""
    lines = md_text.splitlines()
    try:
        h1 = next(i for i, l in enumerate(lines) if l.startswith("# "))
    except StopIteration:
        return []
    block: list[str] = []
    for l in lines[h1 + 1:]:
        if l.startswith("##"):
            break
        if l.strip():
            block.append(l.strip())
        elif block:
            break
    return block


def check_header_line_breaks(md_text: str, pdf_path: Path) -> CheckResult:
    """The location line and the contact line must render on separate lines.
    Two trailing spaces on the location line force the break; without them
    md-to-pdf collapses the two source lines and the phone number ends up
    sitting next to the city."""
    block = header_block(md_text)
    if len(block) < 2:
        return CheckResult("Header line breaks", "FAIL", True,
                           "single-line header, nothing to check")
    loc = re.search(r"[A-Za-z]{4,}", block[0])
    contact = re.search(r"\(?\d[\d)]*", block[1])
    if not loc or not contact:
        return CheckResult("Header line breaks", "FAIL", True,
                           "no location/phone fragments to compare")
    a, b = loc.group(0), contact.group(0)
    layout = run(["pdftotext", "-layout", "-f", "1", "-l", "1", str(pdf_path), "-"])
    collapsed = any(a in ln and b in ln for ln in layout.splitlines()[:8])
    ok = not collapsed
    detail = "ok" if ok else f"'{a}' and '{b}' rendered on one line (missing hard break?)"
    return CheckResult("Header line breaks", "FAIL", ok, detail)


def check_bold_line_breaks(md_text: str) -> CheckResult:
    """Any two consecutive bold-led lines ("**...") with no blank line
    between them need a trailing hard break, or md-to-pdf runs them into one
    line. Catches the same class of bug as the header check, but for
    Experience employer/title pairs and Skills label pairs (e.g. "**Acme Co**"
    directly above "**Senior Designer** | 2021-2025", or "**Strategy &
    Research:**" above "**Tools:**"). A list item on the next line is exempt:
    CommonMark lets a list interrupt a paragraph, so those break correctly
    without a hard break."""
    lines = md_text.splitlines()
    missing = []
    for i in range(len(lines) - 1):
        cur, nxt = lines[i], lines[i + 1]
        if cur.strip().startswith("**") and nxt.strip().startswith("**") and not cur.endswith("  "):
            missing.append(f"'{cur.strip()[:40]}' -> '{nxt.strip()[:40]}'")
    ok = not missing
    detail = "ok" if ok else "missing hard break before: " + "; ".join(missing)
    return CheckResult("Bold line-pair breaks", "FAIL", ok, detail)


def check_links(md_text: str, pdf_path: Path) -> CheckResult:
    source_links = extract_source_links(md_text)
    if not source_links:
        return CheckResult("Header links present", "FAIL", True,
                            "no links in source, nothing to check")
    html = run(["pdftohtml", "-s", "-i", "-noframes", "-stdout", str(pdf_path)])
    pdf_hrefs = set(re.findall(r'href="([^"]+)"', html))
    # pdftohtml sometimes trims trailing slashes; compare loosely.
    normalized_pdf = {h.rstrip("/") for h in pdf_hrefs}
    missing = {l for l in source_links if l.rstrip("/") not in normalized_pdf}
    ok = not missing
    detail = "ok" if ok else f"missing from PDF: {', '.join(sorted(missing))}"
    return CheckResult("Header links present", "FAIL", ok, detail)


def check_title(pdf_path: Path) -> CheckResult:
    info = run(["pdfinfo", str(pdf_path)])
    title_line = next((l for l in info.splitlines() if l.startswith("Title:")), "")
    title = title_line[len("Title:"):].strip()
    expected = pdf_path.stem
    bad_markers = ["localhost", ".md", "Google Docs"]
    is_bad = any(marker in title for marker in bad_markers) or title != expected
    detail = "ok" if not is_bad else f"got '{title}', expected '{expected}'"
    return CheckResult("PDF title is clean", "FAIL", not is_bad, detail)


def check_fidelity(md_text: str, pdf_path: Path) -> CheckResult:
    source_words = len(strip_markdown(md_text).split())
    pdf_words = len(run(["pdftotext", str(pdf_path), "-"]).split())
    ratio = pdf_words / source_words if source_words else 0
    ok = ratio >= FIDELITY_FLOOR
    detail = f"ratio {ratio:.1%} (source={source_words} words, pdf={pdf_words} words)"
    return CheckResult("Extraction fidelity", "FAIL", ok, detail)


def check_page_count(pdf_path: Path) -> CheckResult:
    info = run(["pdfinfo", str(pdf_path)])
    pages_line = next((l for l in info.splitlines() if l.startswith("Pages:")), "")
    try:
        pages = int(pages_line[len("Pages:"):].strip())
    except ValueError:
        pages = -1
    ok = 0 < pages <= MAX_PAGES
    detail = f"{pages} page(s)" if pages >= 0 else "could not read page count"
    return CheckResult("Page count within limit", "WARN", ok, detail)


def check_page_size(pdf_path: Path) -> CheckResult:
    """The default assumes US roles (Letter paper); md-to-pdf's silent
    default is A4, which has no upside here and a small downside if anyone
    prints it. US Letter is the standard."""
    info = run(["pdfinfo", str(pdf_path)])
    size_line = next((l for l in info.splitlines() if l.startswith("Page size:")), "")
    ok = "letter" in size_line.lower()
    detail = size_line[len("Page size:"):].strip() if size_line else "could not read page size"
    return CheckResult("Page size is US Letter", "FAIL", ok, detail)


def check_margins(pdf_path: Path) -> CheckResult:
    """A zero-margin render puts text flush against the paper edge (this
    shipped broken once when --pdf-options overrode md-to-pdf's default
    margin without replacing it). Measure the actual white border on every
    side of every page from word bounding boxes."""
    xml = run(["pdftotext", "-bbox", str(pdf_path), "-"])
    pages = re.findall(
        r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', xml, re.DOTALL
    )
    if not pages:
        return CheckResult("Page margins present", "FAIL", False,
                           "could not read word positions from PDF")
    worst_pt: float | None = None
    worst_side = ""
    word_re = re.compile(
        r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)"'
    )
    for width_s, height_s, body in pages:
        width, height = float(width_s), float(height_s)
        coords = word_re.findall(body)
        if not coords:
            continue
        margins = {
            "left": min(float(c[0]) for c in coords),
            "right": width - max(float(c[2]) for c in coords),
            "top": min(float(c[1]) for c in coords),
            "bottom": height - max(float(c[3]) for c in coords),
        }
        side = min(margins, key=margins.get)
        if worst_pt is None or margins[side] < worst_pt:
            worst_pt, worst_side = margins[side], side
    if worst_pt is None:
        return CheckResult("Page margins present", "FAIL", False,
                           "no words found to measure margins")
    ok = worst_pt >= MIN_MARGIN_PT
    detail = (f"smallest is {worst_pt:.0f}pt ({worst_side}), "
              f"floor {MIN_MARGIN_PT}pt")
    return CheckResult("Page margins present", "FAIL", ok, detail)


def verify(md_path: Path, pdf_path: Path) -> list[CheckResult]:
    md_text = md_path.read_text(encoding="utf-8")
    return [
        check_text_extracts(pdf_path),
        check_links(md_text, pdf_path),
        check_header_line_breaks(md_text, pdf_path),
        check_bold_line_breaks(md_text),
        check_title(pdf_path),
        check_page_size(pdf_path),
        check_margins(pdf_path),
        check_fidelity(md_text, pdf_path),
        check_page_count(pdf_path),
    ]


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    md_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2])

    if not md_path.is_file():
        print(f"Markdown source not found: {md_path}", file=sys.stderr)
        return 2
    if not pdf_path.is_file():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    check_tools_available()

    results = verify(md_path, pdf_path)

    any_fail = False
    for r in results:
        status = "PASS" if r.passed else r.severity
        if not r.passed and r.severity == "FAIL":
            any_fail = True
        print(f"[{status}] {r.name}: {r.detail}")

    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
