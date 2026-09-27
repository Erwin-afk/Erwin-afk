"""Generate the profile README SVGs (header + project cards), dark and light.

    pip install fonttools brotli
    python scripts/build_assets.py

Edit INFO (header) or PROJECTS (cards) below, then rerun. JetBrains Mono is
subset to the characters actually used and embedded as WOFF2, so every visitor
sees the same font and the monospace math holds.
"""
import base64
import io
import os
import urllib.request
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")
FONT_CACHE = os.path.join(HERE, ".fonts")
FONT_URL = "https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/fonts/ttf/JetBrainsMono-{}.ttf"
FONTS = {400: "Regular", 700: "Bold"}
ADV = 0.6  # JetBrains Mono advance width, in em

THEMES = {
    "dark": dict(
        panel="#161b22", bar="#1c2128", border="#30363d", text="#e6edf3",
        muted="#9198a1", faint="#6e7681", accent="#e9a23b", logo_top="#f7c878", green="#3fb950",
        ansi=["#484f58", "#ff7b72", "#3fb950", "#e9a23b", "#58a6ff", "#bc8cff", "#39c5cf", "#b1bac4"],
    ),
    "light": dict(
        panel="#f6f8fa", bar="#eaeef2", border="#d0d7de", text="#1f2328",
        muted="#59636e", faint="#818b98", accent="#b4761a", logo_top="#dc9a33", green="#1a7f37",
        ansi=["#24292f", "#cf222e", "#1a7f37", "#b4761a", "#0969da", "#8250df", "#1b7c83", "#6e7781"],
    ),
}

USED = set()


def w(s, size):
    return len(s) * size * ADV


def text(x, y, s, fill, size, bold=False, anchor=None, extra=""):
    USED.update(s)
    attrs = f'x="{x:g}" y="{y:g}" fill="{fill}" font-size="{size:g}"'
    if bold:
        attrs += ' font-weight="700"'
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    return f"<text {attrs}{extra}>{escape(s)}</text>"


def run(x, y, size, segments):
    """A line of differently styled segments, each placed by monospace math."""
    out = []
    for s, fill, bold in segments:
        if s.strip():
            out.append(text(x, y, s, fill, size, bold))
        x += w(s, size)
    return "".join(out)


def appear(t, total):
    """Hidden until t seconds, then shown. Visible if SMIL never runs."""
    return (f'<animate attributeName="opacity" values="0;1" keyTimes="0;{t / total:.4f}" '
            f'calcMode="discrete" dur="{total}s" fill="freeze"/>')


def discrete(attr, points, total):
    """Step an attribute through (time, value) points; points[0] must be at t=0."""
    vals = ";".join(f"{v:g}" for _, v in points)
    keys = ";".join(f"{t / total:.4f}" for t, _ in points)
    return (f'<animate attributeName="{attr}" values="{vals}" keyTimes="{keys}" '
            f'calcMode="discrete" dur="{total}s" fill="freeze"/>')


def svg(width, height, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" xml:space="preserve" role="img" aria-label="{escape(label)}">'
        f"<title>{escape(label)}</title>"
        "<style>/*FONT*/text{font-family:'JBM','JetBrains Mono',ui-monospace,"
        "SFMono-Regular,Menlo,Consolas,monospace;font-variant-ligatures:none;white-space:pre}</style>"
        f"{body}</svg>"
    )


# ── header: a terminal running neofetch ─────────────────────────────────────

# Drawn as rects, one per horizontal run: glyph-based block art leaves seams.
ART = [
    "#######  ##    ##",
    "##       ###   ##",
    "##       ####  ##",
    "######   ## ## ##",
    "##       ##  ####",
    "##       ##   ###",
    "#######  ##    ##",
]

INFO = [
    ("role", "full-stack developer"),
    ("location", "Hungary"),
    ("focus", "mobile + web, end to end"),
    ("stack", "TypeScript · React Native · Supabase"),
    ("building", "JogsiGo · CleanValet · GymHero"),
]


def header(c):
    W, H = 720, 358
    fs, cw = 15, 15 * ADV
    x0 = 28
    y_cmd = 72
    info_x = x0 + len(ART[0]) * cw + 40
    val_x = info_x + 10 * cw
    info_y0, info_lh = 106, 23
    art_top, cell_h = info_y0 - 13, 18
    prompt = [("❯ ", c["accent"], True)]

    typed = "neofetch"
    t_type0, t_char = 0.45, 0.075
    t_out = t_type0 + len(typed) * t_char + 0.25
    t_row = 0.045
    rows = 2 + len(INFO) + 2  # user@host, rule, info, status, colors
    t_done = t_out + rows * t_row + 0.2
    T = round(t_done + 0.05, 2)

    p = []
    # window
    p.append('<defs><clipPath id="win"><rect x="1" y="1" width="{}" height="{}" rx="12"/></clipPath>'
             '<clipPath id="typed"><rect x="{:g}" y="{}" width="{:g}" height="22">{}</rect></clipPath></defs>'
             .format(W - 2, H - 2, x0 + 2 * cw, y_cmd - 16, len(typed) * cw,
                     discrete("width", [(0, 0)] + [(t_type0 + (k + 1) * t_char, (k + 1) * cw)
                                                    for k in range(len(typed))], T)))
    p.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{c["panel"]}"/>')
    p.append(f'<rect x="1" y="1" width="{W - 2}" height="38" fill="{c["bar"]}" clip-path="url(#win)"/>')
    p.append(f'<line x1="1" y1="39" x2="{W - 1}" y2="39" stroke="{c["border"]}"/>')
    p.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="none" stroke="{c["border"]}"/>')
    for i, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        p.append(f'<circle cx="{22 + i * 20}" cy="20" r="6" fill="{col}"/>')
    p.append(text(W / 2, 24.5, "ervin@github: ~", c["faint"], 12, anchor="middle"))

    # $ neofetch
    p.append(run(x0, y_cmd, fs, prompt))
    p.append(f'<g clip-path="url(#typed)">{text(x0 + 2 * cw, y_cmd, typed, c["text"], fs)}</g>')

    # logo
    runs = []
    for j, row in enumerate(ART):
        k = 0
        while k < len(row):
            if row[k] == "#":
                start = k
                while k < len(row) and row[k] == "#":
                    k += 1
                runs.append((x0 + start * cw, art_top + j * cell_h, (k - start) * cw))
            else:
                k += 1

    def blocks_at(dx, fill, extra=""):
        return "".join(f'<rect x="{x + dx:g}" y="{y + dx:g}" width="{rw:g}" height="{cell_h + 0.5:g}" '
                       f'fill="{fill}"{extra}/>' for x, y, rw in runs)

    art_bottom = art_top + len(ART) * cell_h
    p.append(f'<defs><linearGradient id="logo" gradientUnits="userSpaceOnUse" x1="0" y1="{art_top}" '
             f'x2="0" y2="{art_bottom}"><stop offset="0" stop-color="{c["logo_top"]}"/>'
             f'<stop offset="1" stop-color="{c["accent"]}"/></linearGradient></defs>')
    art = blocks_at(3, c["accent"], ' fill-opacity="0.25"') + blocks_at(0, "url(#logo)")
    p.append(f'<g shape-rendering="crispEdges">{appear(t_out, T)}{art}</g>')

    # info column
    lines = [
        [("ervin", c["accent"], True), ("@", c["text"], False), ("github", c["accent"], True)],
        [("─" * 12, c["faint"], False)],
    ]
    for k, v in INFO:
        lines.append([(k, c["accent"], True)] + [(" " * (10 - len(k)), None, False)] + [(v, c["text"], False)])
    lines.append([("status", c["accent"], True), (" " * 4, None, False),
                  ("● ", c["green"], False), ("open to freelance work", c["text"], False)])
    for i, segs in enumerate(lines):
        y = info_y0 + i * info_lh
        p.append(f"<g>{appear(t_out + (i + 1) * t_row, T)}{run(info_x, y, fs, segs)}</g>")
    y_blocks = info_y0 + len(lines) * info_lh - 13
    blocks = "".join(f'<rect x="{info_x + i * 3 * cw:g}" y="{y_blocks}" width="{3 * cw:g}" height="17" fill="{col}"/>'
                     for i, col in enumerate(c["ansi"]))
    p.append(f"<g>{appear(t_out + (len(lines) + 1) * t_row, T)}{blocks}</g>")
    assert val_x + w(INFO[3][1], fs) < W - x0, "info column overflows"

    # final prompt + cursor
    y_end = y_blocks + 17 + 38
    p.append(f"<g>{appear(t_done, T)}{run(x0, y_end, fs, prompt)}</g>")
    cur_pts_x = [(0, x0 + 2 * cw)] + [(t_type0 + (k + 1) * t_char, x0 + (3 + k) * cw) for k in range(len(typed))]
    cur_pts_x.append((t_done, x0 + 2 * cw))
    p.append(
        f'<rect x="{x0 + 2 * cw:g}" y="{y_end - 13}" width="{cw:g}" height="17" fill="{c["accent"]}">'
        + discrete("x", cur_pts_x, T)
        + discrete("y", [(0, y_cmd - 13), (t_done, y_end - 13)], T)
        + f'<animate attributeName="opacity" values="1;0" dur="1.1s" begin="{T}s" '
          'calcMode="discrete" repeatCount="indefinite"/></rect>'
    )
    assert y_end + 26 <= H, f"header too short: need {y_end + 26}"
    return svg(W, H, "".join(p),
               "Terminal running neofetch: Ervin Nyisztor, full-stack developer in Hungary. "
               "Stack: TypeScript, React Native, Supabase. Building JogsiGo, CleanValet and GymHero.")


# ── project cards ───────────────────────────────────────────────────────────

PROJECTS = [
    dict(slug="jogsigo", n="01", kind="mobile + web", title="JogsiGo", live=True, hint="open app ↗",
         desc=["Driving-school platform for Hungary: students",
               "book lessons, instructors run their day, and",
               "every payment invoices itself via Számlázz.hu."],
         tags=["Expo", "Supabase", "Stripe Connect", "Postgres RLS"]),
    dict(slug="cleanvalet", n="02", kind="mobile + web", title="CleanValet", live=False, hint="private repo",
         desc=["Home-cleaning marketplace, three apps on one",
               "backend: homeowners book and pay, cleaners",
               "claim jobs from a realtime feed, admins run it."],
         tags=["React Native", "Supabase", "Stripe", "Twilio", "Sentry"]),
    dict(slug="gymhero", n="03", kind="mobile", title="GymHero", live=False, hint="private repo",
         desc=["Workouts become four stats (Power, Endurance,",
               "Agility, Discipline) that decide which hero",
               "you turn into. HealthKit sync, all on-device."],
         tags=["Expo", "TypeScript", "Zustand", "HealthKit"]),
    dict(slug="portfolio", n="04", kind="web", title="Portfolio", live=True, hint="open site ↗",
         desc=["Where the dev work and the music live together.",
               "Static Next.js build, dark-first theme with no",
               "flash on load, driven by a single content file."],
         tags=["Next.js", "Tailwind", "TypeScript", "Vercel"]),
]


def card(pr, c):
    W, H, pad = 430, 200, 22
    p = [f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{c["panel"]}" stroke="{c["border"]}"/>']
    p.append(run(pad, 34, 12, [(pr["n"], c["accent"], True), ("  " + pr["kind"], c["faint"], False)]))

    status = "live" if pr["live"] else "in development"
    dot = c["green"] if pr["live"] else c["accent"]
    sx = W - pad - w(status, 11.5)
    p.append(f'<circle cx="{sx - 9:g}" cy="30" r="3.5" fill="{dot}"/>')
    p.append(text(W - pad, 34, status, c["muted"], 11.5, anchor="end"))

    p.append(text(pad, 72, pr["title"], c["text"], 22, bold=True))
    p.append(text(W - pad, 71, pr["hint"], c["accent"] if pr["live"] else c["faint"], 11.5, anchor="end"))
    assert pad + w(pr["title"], 22) + 16 + w(pr["hint"], 11.5) < W - pad, pr["slug"] + ": title row overflows"

    for i, line in enumerate(pr["desc"]):
        assert pad + w(line, 12.5) <= W - pad, f"{pr['slug']}: desc line too long: {line!r}"
        p.append(text(pad, 101 + i * 19, line, c["muted"], 12.5))

    x, y = pad, 158
    for tag in pr["tags"]:
        tw = w(tag, 11) + 16
        p.append(f'<rect x="{x:g}" y="{y}" width="{tw:g}" height="22" rx="6" fill="{c["accent"]}" '
                 f'fill-opacity="0.12" stroke="{c["accent"]}" stroke-opacity="0.35"/>')
        p.append(text(x + 8, y + 15, tag, c["accent"], 11))
        x += tw + 6
    assert x - 6 <= W - pad, pr["slug"] + ": tags overflow"

    label = f'{pr["title"]} ({status}): {" ".join(pr["desc"])} Built with {", ".join(pr["tags"])}.'
    return svg(W, H, "".join(p), label)


# ── build ───────────────────────────────────────────────────────────────────

def font_css():
    css = []
    os.makedirs(FONT_CACHE, exist_ok=True)
    for weight, style in FONTS.items():
        path = os.path.join(FONT_CACHE, f"JetBrainsMono-{style}.ttf")
        if not os.path.exists(path):
            urllib.request.urlretrieve(FONT_URL.format(style), path)
        font = TTFont(path, recalcTimestamp=False)
        cmap = font.getBestCmap()
        missing = sorted(ch for ch in USED if ord(ch) not in cmap and ch != " ")
        assert not missing, f"glyphs missing from font: {missing}"
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = []
        opts.hinting = False
        opts.name_IDs = []
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(sorted(USED)))
        sub.subset(font)
        buf = io.BytesIO()
        font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:'JBM';font-weight:{weight};"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(css)


def main():
    files = {}
    for theme, c in THEMES.items():
        files[f"header-{theme}.svg"] = header(c)
        for pr in PROJECTS:
            files[f"{pr['slug']}-{theme}.svg"] = card(pr, c)
    css = font_css()
    os.makedirs(OUT, exist_ok=True)
    for name, body in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(body.replace("/*FONT*/", css) + "\n")
        print(f"{name:24} {os.path.getsize(os.path.join(OUT, name)) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
