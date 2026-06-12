"""Compose a shade-pixel grid into colored terminal cells.

Two render modes share the same pixel grid from the model: braille packs a
2x4 sub-cell dot matrix into each character (U+2800 block), ASCII maps the
same 2x4 block's coverage onto a density ramp. Either way each cell carries
an average shade in [0, 1] that the app maps to a color attribute.
"""

# Braille dot bit for sub-cell position [dy][dx] (dots 1-8 of U+2800).
BRAILLE_DOT = (
    (0x01, 0x08),
    (0x02, 0x10),
    (0x04, 0x20),
    (0x40, 0x80),
)
BRAILLE_BASE = 0x2800

ASCII_RAMP = " .:-=+*#%@"

# xterm-256 color ladders, darkest to lightest.
PALETTES = (
    ("forest", (22, 28, 34, 40, 46, 118)),
    ("purple", (53, 90, 92, 129, 135, 183)),
    ("autumn", (58, 94, 130, 172, 214, 220)),
    ("ice", (23, 30, 37, 44, 51, 159)),
)


def compose(grid, px_w, px_h, cols, rows, x_off, ascii_mode):
    """Flatten the pixel grid into rows of (char, shade) cells.

    x_off gives a per-pixel-row horizontal displacement (the wind sway), so
    animation never re-rasterizes the model. Blank cells have shade None.
    """
    out = []
    for r in range(rows):
        row_cells = []
        base_py = r * 4
        for c in range(cols):
            bits = 0
            count = 0
            shade_sum = 0.0
            for dy in range(4):
                py = base_py + dy
                if py >= px_h:
                    break
                row = grid[py]
                off = x_off[py]
                for dx in range(2):
                    px = c * 2 + dx - off
                    if 0 <= px < px_w:
                        v = row[px]
                        if v >= 0:
                            bits |= BRAILLE_DOT[dy][dx]
                            count += 1
                            shade_sum += v
            if count == 0:
                row_cells.append((" ", None))
            elif ascii_mode:
                ch = ASCII_RAMP[min(9, 1 + count)]
                row_cells.append((ch, shade_sum / count))
            else:
                row_cells.append((chr(BRAILLE_BASE + bits), shade_sum / count))
        out.append(row_cells)
    return out
