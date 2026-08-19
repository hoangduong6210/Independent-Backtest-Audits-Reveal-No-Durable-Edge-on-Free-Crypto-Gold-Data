#!/usr/bin/env python3
"""Build paper/current_state/manuscript.pdf from the Markdown source."""
import os, shutil, markdown, matplotlib
from xhtml2pdf import pisa
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(HERE, "..", "paper", "current_state")
FIGDIR = os.path.join(HERE, "..", "figures", "generated")
FONTDIR = os.path.join(HERE, "_fonts")
os.makedirs(FONTDIR, exist_ok=True)

_mpl = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
for fn in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans-Oblique.ttf"):
    dst = os.path.join(FONTDIR, fn)
    if not os.path.exists(dst):
        shutil.copy(os.path.join(_mpl, fn), dst)
pdfmetrics.registerFont(TTFont("DV", os.path.join(FONTDIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DV-b", os.path.join(FONTDIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DV-i", os.path.join(FONTDIR, "DejaVuSans-Oblique.ttf")))
registerFontFamily("DV", normal="DV", bold="DV-b", italic="DV-i", boldItalic="DV-b")
try:
    import xhtml2pdf.default as _xd
    _xd.DEFAULT_FONT["dv"] = "DV"
except Exception:
    pass

CSS = """
@page { size: A4; margin: 1.8cm 1.6cm; }
body { font-family: "DV"; font-size: 9.5pt; line-height: 1.35; color: #111; }
h1 { font-size: 16pt; color: #1A2A4A; }
h2 { font-size: 12.5pt; color: #1A2A4A; margin-top: 12pt; border-bottom: 1px solid #ccc; }
h3 { font-size: 10.5pt; color: #25406b; margin-top: 8pt; }
p { margin: 3pt 0; text-align: justify; }
img { width: 15cm; }
table { border-collapse: collapse; width: 100%; font-size: 7.5pt; }
th, td { border: 0.5pt solid #888; padding: 2pt 3pt; }
th { background: #e8edf4; font-weight: bold; }
code { font-size: 8pt; color: #444; }
"""


def link_callback(uri, rel):
    b = os.path.basename(uri.replace("\\", "/"))
    for d in (FIGDIR, FONTDIR):
        p = os.path.join(d, b)
        if os.path.exists(p):
            return p
    return uri


def add_history_metadata(path):
    """Record research and maintenance dates without backdating the PDF."""
    reader = PdfReader(path)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    existing = {
        str(key): str(value)
        for key, value in (reader.metadata or {}).items()
        if key and value is not None
    }
    existing.update({
        "/Title": "Independent Backtest Audits Reveal No Durable Edge on Free Crypto/Gold Data",
        "/Author": "Duong Viet Hoang",
        "/Subject": (
            "Core research campaign conducted 2026-06-28 to 2026-06-30; "
            "manuscript revisions through 2026-07-17; repository maintenance "
            "on 2026-08-19 introduced no new experimental result."
        ),
        "/Keywords": "backtest audit, reproducibility, cryptocurrency, gold, negative result",
        "/ResearchPeriod": "2026-06-28/2026-06-30",
        "/OriginalReleaseDate": "2026-06-30",
        "/RepositoryMaintenanceDate": "2026-08-19",
    })
    writer.add_metadata(existing)
    temporary = f"{path}.metadata"
    with open(temporary, "wb") as stream:
        writer.write(stream)
    os.replace(temporary, path)


def main():
    text = open(os.path.join(PAPER, "manuscript.md"), encoding="utf-8").read()
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    out = os.path.join(PAPER, "manuscript.pdf")
    with open(out, "wb") as f:
        res = pisa.CreatePDF(html, dest=f, link_callback=link_callback, encoding="utf-8")
    if res.err:
        raise RuntimeError(f"PDF build failed with {res.err} error(s)")
    add_history_metadata(out)
    print(f"manuscript.pdf: err={res.err} size={os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
