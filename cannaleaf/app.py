"""Curses front end: animation loop, palettes, and live keyboard controls."""

import argparse
import curses
import math
import time

from .model import LeafParams, rasterize
from .render import PALETTES, compose

FALLBACK_COLORS = (
    curses.COLOR_GREEN,
    curses.COLOR_MAGENTA,
    curses.COLOR_YELLOW,
    curses.COLOR_CYAN,
)

HELP_LINES = (
    "  q       quit            ",
    "  + / -   leaflet count   ",
    "  [ / ]   serration depth ",
    "  , / .   leaflet width   ",
    "  z / x   zoom out / in   ",
    "  w       cycle wind      ",
    "  p       cycle palette   ",
    "  r       braille / ascii ",
    "  space   pause sway      ",
    "  ?       toggle help     ",
)


def init_palette(idx):
    """Return shade-indexed attrs for palette idx, darkest to lightest."""
    name, colors = PALETTES[idx]
    if curses.COLORS >= 256:
        attrs = []
        for j, col in enumerate(colors):
            curses.init_pair(j + 1, col, -1)
            attrs.append(curses.color_pair(j + 1))
        return attrs
    curses.init_pair(1, FALLBACK_COLORS[idx % len(FALLBACK_COLORS)], -1)
    pair = curses.color_pair(1)
    return [pair | curses.A_DIM, pair | curses.A_DIM, pair, pair,
            pair | curses.A_BOLD, pair | curses.A_BOLD]


def sway_offsets(px_h, anchor_y, wind, phase):
    """Per-pixel-row horizontal displacement: a slow bend plus a faint rustle.

    Rows farther above the attachment point move more, so the tips lead and
    the stem stays planted.
    """
    offs = [0] * px_h
    if wind <= 0 or anchor_y <= 0:
        return offs
    bend = 3.6 * wind
    for py in range(px_h):
        rel = (anchor_y - py) / anchor_y
        if rel <= 0:
            continue
        off = (bend * math.sin(phase * 1.5 + py * 0.035) * rel ** 1.7
               + 0.9 * wind * math.sin(phase * 6.3 + py * 0.22) * rel * rel)
        offs[py] = int(round(off))
    return offs


def draw_help(stdscr, rows, cols):
    height = len(HELP_LINES) + 2
    width = len(HELP_LINES[0]) + 2
    y0 = max((rows - height) // 2, 0)
    x0 = max((cols - width) // 2, 0)
    top = "┌─ cannaleaf " + "─" * (width - 14) + "┐"
    bottom = "└" + "─" * (width - 2) + "┘"
    try:
        stdscr.addstr(y0, x0, top)
        for k, line in enumerate(HELP_LINES):
            stdscr.addstr(y0 + 1 + k, x0, "│" + line + "│")
        stdscr.addstr(y0 + height - 1, x0, bottom)
    except curses.error:
        pass


def run(stdscr, args):
    curses.curs_set(0)
    stdscr.timeout(50)
    curses.start_color()
    curses.use_default_colors()

    params = LeafParams(leaflets=args.leaflets)
    pal_idx = next(i for i, (n, _) in enumerate(PALETTES) if n == args.palette)
    attrs = init_palette(pal_idx)
    n_shades = len(attrs)
    wind = args.wind
    ascii_mode = args.ascii
    paused = False
    show_help = False
    need_raster = True
    grid, anchor_y, px_w, px_h = None, 0, 0, 0
    last_size = (0, 0)
    phase = 0.0
    last_t = time.monotonic()
    frames = 0

    while True:
        now = time.monotonic()
        if not paused:
            phase += now - last_t
        last_t = now

        rows, cols = stdscr.getmaxyx()
        if rows < 8 or cols < 24:
            stdscr.erase()
            try:
                stdscr.addstr(0, 0, "terminal too small")
            except curses.error:
                pass
            stdscr.refresh()
        else:
            if need_raster or (rows, cols) != last_size:
                px_w, px_h = cols * 2, (rows - 1) * 4
                grid, anchor_y = rasterize(params, px_w, px_h)
                last_size = (rows, cols)
                need_raster = False

            x_off = sway_offsets(px_h, anchor_y, wind, phase)
            cells = compose(grid, px_w, px_h, cols, rows - 1, x_off, ascii_mode)

            stdscr.erase()
            for r, row_cells in enumerate(cells):
                c = 0
                n = len(row_cells)
                while c < n:
                    shade = row_cells[c][1]
                    if shade is None:
                        c += 1
                        continue
                    attr = attrs[min(n_shades - 1, int(shade * n_shades))]
                    j = c
                    chunk = []
                    while j < n and row_cells[j][1] is not None and \
                            attrs[min(n_shades - 1, int(row_cells[j][1] * n_shades))] == attr:
                        chunk.append(row_cells[j][0])
                        j += 1
                    try:
                        stdscr.addstr(r, c, "".join(chunk), attr)
                    except curses.error:
                        pass
                    c = j

            status = (" cannaleaf  leaflets:%d  serration:%.2f  width:%.2f"
                      "  zoom:%.1f  wind:%.1f  palette:%s  %s%s   [?] help  [q]uit"
                      % (params.leaflets, params.serration, params.width,
                         params.zoom, wind, PALETTES[pal_idx][0],
                         "ascii" if ascii_mode else "braille",
                         "  paused" if paused else ""))
            stdscr.insstr(rows - 1, 0, status[:cols - 1], curses.A_DIM)

            if show_help:
                draw_help(stdscr, rows, cols)
            stdscr.refresh()

        frames += 1
        if args.frames and frames >= args.frames:
            return

        ch = stdscr.getch()
        if ch in (ord("q"), 27):
            return
        elif ch in (ord("+"), ord("=")):
            params.leaflets = min(13, params.leaflets + 2)
            need_raster = True
        elif ch == ord("-"):
            params.leaflets = max(3, params.leaflets - 2)
            need_raster = True
        elif ch == ord("]"):
            params.serration = min(0.9, params.serration + 0.05)
            need_raster = True
        elif ch == ord("["):
            params.serration = max(0.0, params.serration - 0.05)
            need_raster = True
        elif ch == ord("."):
            params.width = min(0.30, params.width + 0.02)
            need_raster = True
        elif ch == ord(","):
            params.width = max(0.08, params.width - 0.02)
            need_raster = True
        elif ch == ord("x"):
            params.zoom = min(1.6, params.zoom + 0.1)
            need_raster = True
        elif ch == ord("z"):
            params.zoom = max(0.4, params.zoom - 0.1)
            need_raster = True
        elif ch == ord("w"):
            wind = (wind + 0.5) % 2.5
        elif ch == ord("p"):
            pal_idx = (pal_idx + 1) % len(PALETTES)
            attrs = init_palette(pal_idx)
        elif ch == ord("r"):
            ascii_mode = not ascii_mode
        elif ch == ord(" "):
            paused = not paused
        elif ch == ord("?"):
            show_help = not show_help
        elif ch == curses.KEY_RESIZE:
            need_raster = True


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="cannaleaf",
        description="A procedurally drawn, gently swaying cannabis leaf "
                    "for your terminal.")
    parser.add_argument("--leaflets", type=int, default=7,
                        help="leaflet count, odd, 3-13 (default: 7)")
    parser.add_argument("--palette", default="forest",
                        choices=[name for name, _ in PALETTES],
                        help="color palette (default: forest)")
    parser.add_argument("--wind", type=float, default=1.0,
                        help="wind strength, 0 disables sway (default: 1.0)")
    parser.add_argument("--ascii", action="store_true",
                        help="render with an ascii ramp instead of braille")
    parser.add_argument("--frames", type=int, default=0, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    args.leaflets = max(3, min(13, args.leaflets | 1))
    args.wind = max(0.0, min(2.0, args.wind))
    curses.wrapper(run, args)


if __name__ == "__main__":
    main()
