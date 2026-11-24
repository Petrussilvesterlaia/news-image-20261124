#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news poster (1024x1024 PNG).

Renders six verified stories of Tuesday 24 November 2026 as a clean
editorial poster: masthead date, 2x3 grid of story cards, each with a
simple pictogram icon drawn from shapes, a bold headline, one summary
line and a small dateline tag. Run: python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 44
GUTTER = 20

BG = (246, 241, 231)        # off-white paper
CARD = (255, 253, 248)      # card paper
INK = (25, 23, 19)          # near-black ink
MUTED = (96, 90, 78)        # warm grey for summaries
ACCENT = (178, 39, 30)      # single accent: news red
ACCENT_SOFT = (242, 221, 216)
RULE = (216, 207, 192)
BORDER = (224, 216, 200)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_drone(d, cx, cy, s, col):
    """Quadcopter pictogram centred at (cx, cy), span s."""
    u = s / 10.0
    # arms
    d.line([(cx - 3.2 * u, cy - 3.2 * u), (cx + 3.2 * u, cy + 3.2 * u)],
           fill=col, width=max(2, int(0.55 * u)))
    d.line([(cx + 3.2 * u, cy - 3.2 * u), (cx - 3.2 * u, cy + 3.2 * u)],
           fill=col, width=max(2, int(0.55 * u)))
    # rotors
    for rx, ry in [(-3.4, -3.4), (3.4, -3.4), (-3.4, 3.4), (3.4, 3.4)]:
        d.ellipse([cx + rx * u - 1.5 * u, cy + ry * u - 0.55 * u,
                   cx + rx * u + 1.5 * u, cy + ry * u + 0.55 * u],
                  outline=col, width=max(2, int(0.45 * u)))
    # body
    d.rounded_rectangle([cx - 1.9 * u, cy - 1.3 * u,
                         cx + 1.9 * u, cy + 1.3 * u],
                        radius=int(0.8 * u), fill=col)
    d.ellipse([cx - 0.7 * u, cy - 0.55 * u, cx + 0.7 * u, cy + 0.55 * u],
              fill=ACCENT_SOFT)


def draw_jet(d, cx, cy, s, col):
    """Jet aircraft pictogram, nose pointing up-right."""
    u = s / 10.0
    body = [(cx - 3.6 * u, cy + 1.6 * u), (cx - 0.6 * u, cy + 0.4 * u),
            (cx + 3.4 * u, cy - 3.2 * u), (cx + 3.8 * u, cy - 2.2 * u),
            (cx + 1.2 * u, cy + 1.8 * u), (cx - 2.2 * u, cy + 3.4 * u)]
    d.polygon(body, fill=col)
    # wings (larger, swept)
    d.polygon([(cx - 0.4 * u, cy - 0.4 * u), (cx + 1.2 * u, cy - 4.4 * u),
               (cx + 2.6 * u, cy - 3.8 * u), (cx + 0.9 * u, cy + 0.6 * u)],
              fill=col)
    d.polygon([(cx - 1.4 * u, cy + 1.0 * u), (cx - 4.4 * u, cy + 2.4 * u),
               (cx - 3.6 * u, cy + 3.8 * u), (cx - 0.6 * u, cy + 2.0 * u)],
              fill=col)
    # tail fin
    d.polygon([(cx - 2.6 * u, cy + 1.2 * u), (cx - 3.4 * u, cy - 1.4 * u),
               (cx - 2.4 * u, cy - 1.2 * u), (cx - 1.6 * u, cy + 1.8 * u)],
              fill=col)


def draw_bank(d, cx, cy, s, col):
    """Bank building pictogram with a dollar sign."""
    u = s / 10.0
    # pediment
    d.polygon([(cx - 3.8 * u, cy - 1.2 * u), (cx, cy - 3.8 * u),
               (cx + 3.8 * u, cy - 1.2 * u)], fill=col)
    # columns
    for ox in (-2.6, 0.0, 2.6):
        d.rectangle([cx + ox * u - 0.55 * u, cy - 0.9 * u,
                     cx + ox * u + 0.55 * u, cy + 2.4 * u], fill=col)
    # base
    d.rectangle([cx - 3.8 * u, cy + 2.4 * u, cx + 3.8 * u, cy + 3.6 * u],
                fill=col)
    # dollar sign in the pediment gap
    f = font(F_BOLD, int(2.6 * u))
    d.text((cx, cy + 0.55 * u), "$", font=f, fill=ACCENT_SOFT, anchor="mm")


def draw_tanker(d, cx, cy, s, col):
    """Oil tanker pictogram on waves."""
    u = s / 10.0
    # hull
    d.polygon([(cx - 4.0 * u, cy - 0.6 * u), (cx + 4.0 * u, cy - 0.6 * u),
               (cx + 3.2 * u, cy + 1.6 * u), (cx - 3.2 * u, cy + 1.6 * u)],
              fill=col)
    # deck containers
    d.rectangle([cx - 3.0 * u, cy - 2.6 * u, cx - 1.2 * u, cy - 0.6 * u],
                fill=col)
    d.rectangle([cx - 0.8 * u, cy - 2.2 * u, cx + 1.0 * u, cy - 0.6 * u],
                fill=col)
    # bridge tower
    d.rectangle([cx + 1.6 * u, cy - 3.2 * u, cx + 3.0 * u, cy - 0.6 * u],
                fill=col)
    # waves
    for wy, wx0 in [(2.6, -4.0), (3.4, -2.6)]:
        d.arc([cx + wx0 * u, cy + wy * u, cx + (wx0 + 2.6) * u,
               cy + (wy + 1.6) * u], start=180, end=360, fill=col,
              width=max(2, int(0.45 * u)))


def draw_globe(d, cx, cy, s, col):
    """Globe with a leaf pictogram."""
    u = s / 10.0
    d.ellipse([cx - 3.6 * u, cy - 3.6 * u, cx + 3.6 * u, cy + 3.6 * u],
              outline=col, width=max(2, int(0.6 * u)))
    d.ellipse([cx - 1.6 * u, cy - 3.6 * u, cx + 1.6 * u, cy + 3.6 * u],
              outline=col, width=max(2, int(0.4 * u)))
    d.line([(cx - 3.6 * u, cy), (cx + 3.6 * u, cy)], fill=col,
           width=max(2, int(0.4 * u)))
    # leaf
    leaf = [(cx - 0.6 * u, cy + 3.4 * u), (cx - 3.2 * u, cy + 1.2 * u),
            (cx - 1.4 * u, cy + 3.8 * u), (cx + 1.2 * u, cy + 3.8 * u)]
    d.polygon(leaf, fill=ACCENT)


def draw_podium(d, cx, cy, s, col):
    """Podium with microphone pictogram."""
    u = s / 10.0
    # microphone
    d.ellipse([cx - 1.1 * u, cy - 3.8 * u, cx + 1.1 * u, cy - 1.6 * u],
              fill=col)
    d.line([(cx, cy - 1.6 * u), (cx, cy + 0.6 * u)], fill=col,
           width=max(2, int(0.5 * u)))
    d.arc([cx - 1.6 * u, cy - 2.6 * u, cx + 1.6 * u, cy + 0.6 * u],
          start=0, end=180, fill=col, width=max(2, int(0.45 * u)))
    # podium
    d.polygon([(cx - 3.6 * u, cy + 0.8 * u), (cx + 3.6 * u, cy + 0.8 * u),
               (cx + 2.8 * u, cy + 3.8 * u), (cx - 2.8 * u, cy + 3.8 * u)],
              fill=col)
    d.rectangle([cx - 3.6 * u, cy + 0.8 * u, cx + 3.6 * u, cy + 1.5 * u],
                fill=col)


ICONS = {
    "drone": draw_drone,
    "jet": draw_jet,
    "bank": draw_bank,
    "tanker": draw_tanker,
    "globe": draw_globe,
    "podium": draw_podium,
}

STORIES = [
    {
        "icon": "drone",
        "tag": "POLAND  ·  AIRSPACE",
        "headline": "Russian drone crosses into Poland",
        "summary": "Warsaw scrambles air defences overnight.",
    },
    {
        "icon": "jet",
        "tag": "SOUTH KOREA  ·  AIRSPACE",
        "headline": "Seoul on alert after Russian jet",
        "summary": "Evacuation alert issued, then lifted.",
    },
    {
        "icon": "bank",
        "tag": "WASHINGTON  ·  SANCTIONS",
        "headline": "U.S. targets Iran's shadow banks",
        "summary": "$14.7bn in illicit flows hit by sanctions.",
    },
    {
        "icon": "tanker",
        "tag": "STRAIT OF HORMUZ  ·  OIL",
        "headline": "Three tankers hit by mines in Hormuz",
        "summary": "IRGC claim comes as U.S. warships escort shipping.",
    },
    {
        "icon": "globe",
        "tag": "TURKEY  ·  CLIMATE",
        "headline": "COP31 talks stall in Turkey",
        "summary": "Oil producers clash with the climate bloc.",
    },
    {
        "icon": "podium",
        "tag": "WASHINGTON  ·  JUSTICE",
        "headline": "Trump attacks Newsom death-row move",
        "summary": "President vows a federal death-penalty push.",
    },
]


def draw_card(d, x, y, w, h, story):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD,
                        outline=BORDER, width=2)
    # red top rule
    d.rounded_rectangle([x, y, x + w, y + 6], radius=3, fill=ACCENT)
    pad = 20
    # icon disc
    ix, iy, ir = x + pad + 34, y + pad + 34, 34
    d.ellipse([ix - ir, iy - ir, ix + ir, iy + ir], fill=ACCENT_SOFT)
    ICONS[story["icon"]](d, ix, iy, 46, ACCENT)
    # headline, right of icon
    f_head = font(F_BOLD, 29)
    tx = x + pad + 84
    tw = w - pad - 84 - pad
    lines = wrap(d, story["headline"], f_head, tw)[:2]
    ty = y + pad + 2
    for ln in lines:
        d.text((tx, ty), ln, font=f_head, fill=INK)
        ty += 36
    # summary, full width below
    f_sum = font(F_REG, 22)
    sy = y + pad + 78
    for ln in wrap(d, story["summary"], f_sum, w - 2 * pad)[:2]:
        d.text((x + pad, sy), ln, font=f_sum, fill=MUTED)
        sy += 29
    # dateline tag at bottom
    f_tag = font(F_BOLD, 17)
    d.text((x + pad, y + h - pad - 17), story["tag"], font=f_tag,
           fill=ACCENT)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    f_kick = font(F_BOLD, 24)
    kicker = "T H E   W O R L D   I N   O N E   I M A G E"
    kw = d.textlength(kicker, font=f_kick)
    d.text(((W - kw) / 2, 40), kicker, font=f_kick, fill=ACCENT)

    f_date = font(F_BOLD, 54)
    date = "TUESDAY, 24 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 76), date, font=f_date, fill=INK)

    # rule under masthead
    d.line([(MARGIN, 152), (W - MARGIN, 152)], fill=RULE, width=2)
    f_sub = font(F_REG, 25)
    sub = "Six stories that defined the day."
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 168), sub, font=f_sub, fill=MUTED)

    # ---- story grid: 2 cols x 3 rows ----
    cw = (W - 2 * MARGIN - GUTTER) // 2
    ch = 222
    gx, gy = MARGIN, 216
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_card(d, gx + col * (cw + GUTTER), gy + row * (ch + 18),
                  cw, ch, story)

    # ---- footer ----
    f_foot = font(F_REG, 20)
    foot = "Compiled from wire reports  ·  24 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 968), foot, font=f_foot, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
