"""Parametric cannabis-leaf geometry, rasterized onto a sub-cell pixel grid.

The leaf is modeled as N lance-shaped leaflets fanning radially from an
attachment point, each with a sawtooth-serrated edge, plus a short petiole.
`rasterize` paints the model into a grid of shade values that a renderer can
turn into braille or ASCII cells. Geometry knows nothing about curses.
"""

import math
from dataclasses import dataclass


@dataclass
class LeafParams:
    leaflets: int = 7        # odd count, 3..13
    spread_deg: float = 95.0 # fan half-angle of the outermost leaflet pair
    width: float = 0.15      # max leaflet half-width as a fraction of its length
    serration: float = 0.45  # serration depth, 0 (smooth) .. 0.9 (deeply toothed)
    teeth: int = 14          # serration teeth along each leaflet
    zoom: float = 1.0


# Shade values: 0.0 is darkest (vein), 1.0 is lightest (serrated tip edges).
VEIN_SHADE = 0.04
STEM_SHADE = 0.10


def rasterize(params, px_w, px_h):
    """Paint the leaf into a px_h x px_w grid.

    Returns (grid, anchor_y): grid holds -1.0 for empty pixels and a shade in
    [0, 1] for leaf pixels; anchor_y is the pixel row of the attachment point,
    which the animator uses as the sway pivot.
    """
    grid = [[-1.0] * px_w for _ in range(px_h)]
    half = max((params.leaflets - 1) // 2, 1)
    length = min(px_h * 0.66, px_w * 0.44) * params.zoom
    cx = px_w / 2.0
    cy = max(min((px_h - 1.38 * length) / 2.0 + length, px_h - 2.0), 2.0)
    if length < 8:
        return grid, int(cy)

    def put(x, y, shade):
        xi, yi = int(x), int(y)
        if 0 <= xi < px_w and 0 <= yi < px_h:
            cur = grid[yi][xi]
            # Where leaflets overlap near the center, keep the darker shade so
            # the heart of the leaf stays deep green.
            if cur < 0 or shade < cur:
                grid[yi][xi] = shade

    for i in range(-half, half + 1):
        rank = abs(i) / half
        angle = math.radians(params.spread_deg * (i / half))
        # Outer leaflets are progressively shorter, like the real plant.
        ll = length * (1.0 - 0.62 * rank ** 1.3)
        hw = ll * params.width
        dir_x, dir_y = math.sin(angle), math.cos(angle)
        perp_x, perp_y = math.cos(angle), -math.sin(angle)
        steps = max(int(ll * 2.5), 24)
        for si in range(steps + 1):
            t = si / steps
            # Lance profile: zero at the stalk, widest around 40% out, zero at the tip.
            w = hw * math.sin(math.pi * t ** 0.88)
            if t > 0.12:
                tooth = (t * params.teeth) % 1.0
                w *= 1.0 - 0.55 * params.serration * tooth
            if w < 0.4 and 0.02 < t < 0.98:
                w = 0.4
            bx = cx + dir_x * t * ll
            by = cy - dir_y * t * ll
            fill = max(int(w * 4), 1)
            for sj in range(-fill, fill + 1):
                s = w * sj / fill
                rel = abs(s) / max(w, 1e-6)
                shade = min(1.0, 0.18 + 0.52 * rel + 0.38 * t)
                if rel < 0.12 and t < 0.92:
                    shade = VEIN_SHADE
                put(bx + perp_x * s, by - perp_y * s, shade)

    # Petiole: a short, slightly curved stem hanging below the attachment point.
    stem = 0.36 * length
    stem_steps = max(int(stem * 2), 1)
    for si in range(stem_steps + 1):
        t = si / stem_steps
        x = cx + 1.5 * math.sin(t * 2.2)
        y = cy + t * stem
        for dx in (-0.5, 0.0, 0.5):
            put(x + dx, y, STEM_SHADE)

    return grid, int(cy)
