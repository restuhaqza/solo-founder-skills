#!/usr/bin/env python3
"""Render docs/assets/demo.gif — a terminal-style animated demo of a skill.

Pure stdlib + Pillow. Deterministic (no randomness, no network). Regenerate with:

    python3 scripts/make_demo_gif.py

The frame mirrors the real output of
`skills/founder-operating-rhythm/scripts/runway.py --cash 120000 --revenue 8000
--costs 14000 --growth 6`, so the GIF never drifts from the script.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Catppuccin Mocha
BG = "#1e1e2e"
BAR = "#181825"
TEXT = "#cdd6f4"
DIM = "#6c7086"
SURFACE = "#45475a"
GREEN = "#a6e3a1"
YELLOW = "#f9e2af"
BLUE = "#89b4fa"
MAUVE = "#cba6f7"
RED = "#f38ba8"

FONT_PATH = "/System/Library/Fonts/Menlo.ttc"
W, H = 1040, 828
PAD = 30
FS = 21
LH = 33
TITLEBAR = 44
TOP = TITLEBAR + 22

USER_TEXT = "am I going to make it? $120k in the bank, $8k MRR, $14k spend, 6% growth"
CMD_LINES = [
    "$ python3 skills/founder-operating-rhythm/scripts/runway.py \\",
    "      --cash 120000 --revenue 8000 --costs 14000 --growth 6",
]

# Output lines as (runs, colour-pairs) — mirrors the script's rendered output.
OUTPUT = [
    [("Cash on hand:        ", DIM), ("$120,000", TEXT)],
    [("Monthly revenue:     ", DIM), ("$8,000", TEXT)],
    [("Monthly costs:       ", DIM), ("$14,000", TEXT)],
    [("Net monthly burn:    ", DIM), ("$6,000", TEXT)],
    [("Revenue growth:      ", DIM), ("6%/mo", TEXT)],
    [("--------------------------------------------------------", SURFACE)],
    [("Runway (pre-tax):    ", DIM), ("20.0 months", GREEN)],
    [("Break-even:          ", DIM), ("month 10", YELLOW)],
    [("Tax set-aside:       ", DIM), ("$2,400/mo (30% of revenue)", TEXT)],
    [("Runway (after tax):  ", DIM), ("14.3 months", YELLOW)],
    [("Flip growth rate:    ", DIM), ("2.8%/mo (pre-tax) · 4.0%/mo after tax", MAUVE)],
    [("--------------------------------------------------------", SURFACE)],
    [("Verdict: ", DIM), ("DEFAULT ALIVE", GREEN)],
]
ACCENT = [("→ hold ", MAUVE), ("≥ 4.0%/mo after tax", MAUVE), (" — you're at 6%.", DIM)]

HEADER = [("solo-founder-skills", MAUVE), ("  ·  ", DIM), ("founder-operating-rhythm", BLUE)]
USER_RUNS = [("› ", BLUE), (USER_TEXT, TEXT)]

# Line slots
I_HEADER, I_BLANK1, I_USER, I_BLANK2, I_CMD1, I_CMD2 = 0, 1, 2, 3, 4, 5
I_OUT0 = 6  # blank, then OUTPUT, then blank, then ACCENT
N_LINES = I_OUT0 + 1 + len(OUTPUT) + 1 + 1


def load_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size, index=0)


FONT = load_font(FS)
FONT_SM = load_font(15)
FONT_DOT = load_font(16)


def base_canvas() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, TITLEBAR], fill=BAR)
    for i, colour in enumerate((RED, YELLOW, GREEN)):
        cx, cy = 28 + i * 22, TITLEBAR // 2
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=colour)
    d.text((W // 2, TITLEBAR // 2), "solo-founder-skills — live demo", font=FONT_SM, fill=DIM, anchor="mm")
    d.line([0, TITLEBAR, W, TITLEBAR], fill=SURFACE, width=1)
    return img


def draw_line(d: ImageDraw.ImageDraw, runs, y: int, cursor: bool) -> None:
    x = PAD
    for text, colour in runs:
        d.text((x, y), text, font=FONT, fill=colour)
        x += FONT.getlength(text)
    if cursor:
        d.rectangle([x + 2, y + 3, x + 12, y + FS + 4], fill=TEXT)


def render(display, cursor_line=None) -> Image.Image:
    img = base_canvas()
    d = ImageDraw.Draw(img)
    for i, runs in enumerate(display):
        if runs is None:
            continue
        draw_line(d, runs, TOP + i * LH, cursor=(i == cursor_line))
    return img


def build_frames():
    frames = []  # (display, duration_ms, cursor_line)

    def snap(disp):
        return [list(r) if r is not None else None for r in disp]

    disp = [None] * N_LINES
    disp[I_HEADER] = HEADER
    frames.append((snap(disp), 350, None))

    # Type the user's plain-English ask.
    for t in range(2, len(USER_TEXT) + 1, 3):
        disp[I_USER] = [USER_RUNS[0], (USER_TEXT[:t], TEXT)]
        frames.append((snap(disp), 42, I_USER))
    disp[I_USER] = USER_RUNS
    frames.append((snap(disp), 320, None))

    # Type the command (wrapped over two lines).
    total = len(CMD_LINES[0]) + len(CMD_LINES[1])
    for t in range(3, total + 1, 3):
        a = CMD_LINES[0][: min(t, len(CMD_LINES[0]))]
        b = CMD_LINES[1][: max(0, t - len(CMD_LINES[0]))]
        disp[I_CMD1] = [("$ ", GREEN), (a[2:], TEXT)] if a else None
        disp[I_CMD2] = [(b, TEXT)] if b else None
        frames.append((snap(disp), 38, I_CMD2 if b else I_CMD1))
    disp[I_CMD1] = [("$ ", GREEN), (CMD_LINES[0][2:], TEXT)]
    disp[I_CMD2] = [(CMD_LINES[1], TEXT)]
    frames.append((snap(disp), 340, None))

    # Reveal the output block one line at a time.
    block = [[]] + OUTPUT + [[]] + [ACCENT]
    for j, line in enumerate(block):
        disp[I_OUT0 + j] = line
        frames.append((snap(disp), 110, None))

    frames.append((snap(disp), 2600, None))  # hold
    return frames


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the README demo GIF.")
    parser.add_argument("--out", default="docs/assets/demo.gif")
    parser.add_argument("--poster", default="docs/assets/demo-poster.png")
    args = parser.parse_args()

    frames = build_frames()
    images = [render(disp, cur).convert("P", palette=Image.ADAPTIVE, colors=64) for disp, _, cur in frames]
    durations = [ms for _, ms, _ in frames]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        out,
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=True,
    )

    poster = Path(args.poster)
    render(frames[-1][0]).save(poster)
    size_kb = out.stat().st_size / 1024
    print(f"wrote {out}  ({len(images)} frames, {size_kb:.0f} KB)")
    print(f"wrote {poster}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
