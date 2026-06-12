# cannaleaf

A procedurally drawn, gently swaying cannabis leaf for your terminal.

Pure Python stdlib (`curses`), no dependencies. The leaf is parametric —
leaflet count, width, and serration are all live-tweakable — and rendered
with Unicode braille characters for 2×4 sub-cell resolution, shaded with a
green gradient (dark at the central veins, light at the serrated tips). A
slow sine bend plus a faint high-frequency rustle make it sway in the wind,
pivoting from the stem so the tips lead.

```
                            ⢀⡀
                            ⣾⣷
                           ⣸⣿⣿⣇
                  ⢀⡀      ⢠⣿⣿⣿⣿⡄      ⢀⡀
                   ⣿⣧⣄    ⣼⣿⣿⣿⣿⣧    ⣠⣼⣿
                   ⢹⣿⣿⣷⣤ ⠰⣿⣿⣿⣿⣿⣿⠆ ⣤⣾⣿⣿⡏
                    ⢿⣿⣿⣿⣷⣜⣿⣿⣿⣿⣿⣿⣣⣾⣿⣿⣿⡿
                    ⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗
                ⣀⣀⣀⣀ ⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇ ⣀⣀⣀⣀
                ⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁
                  ⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁
                    ⠈⠙⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠋⠁
                    ⠘⠻⠿⢿⣿⡿⠿⠟⠛⣿⠻⠿⢿⣿⡿⠿⠟⠃
                             ⣿
                             ⣿
                             ⣿
                             ⠉
```

## Run it

No install needed — from the repo root:

```sh
python3 -m cannaleaf
```

Or install it as a command:

```sh
pip install -e .
cannaleaf
```

## Options

```
--leaflets N        leaflet count, odd, 3-13 (default: 7)
--palette NAME      forest | purple | autumn | ice (default: forest)
--wind X            wind strength, 0 disables sway (default: 1.0)
--ascii             render with an ascii density ramp instead of braille
```

## Keys

| Key     | Action                                      |
| ------- | ------------------------------------------- |
| `+` `-` | more / fewer leaflets                       |
| `[` `]` | shallower / deeper serration                |
| `,` `.` | thinner / fatter leaflets (sativa ↔ indica) |
| `z` `x` | zoom out / in                               |
| `w`     | cycle wind strength                         |
| `p`     | cycle color palette                         |
| `r`     | toggle braille / ascii renderer             |
| `space` | pause the sway                              |
| `?`     | help overlay                                |
| `q`     | quit                                        |

The leaf re-centers and re-scales itself on terminal resize.

## Design

The geometry (`model.py`) knows nothing about curses: each leaflet is a
lance-shaped scanline fill fanning radially from an attachment point, with a
sawtooth cut along the edge for serration, rasterized onto a pixel grid of
shade values. Renderers (`render.py`) pack that grid into braille (2×4 dots
per cell) or an ASCII ramp, so output modes are swappable. The app
(`app.py`) only re-rasterizes when a parameter or the terminal size changes;
the wind sway is applied at compose time as a per-pixel-row horizontal
offset.

On terminals without 256-color support it falls back to the basic palette
with dim/bold shading.

## Tests

```sh
python3 -m unittest discover -s tests
```
