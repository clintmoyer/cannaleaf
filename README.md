# cannaleaf

A procedurally drawn, gently swaying cannabis leaf for your terminal.

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

## Install

```sh
python3 -m pip install cannaleaf
cannaleaf
```

## Run from source

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

## Tests

```sh
python3 -m unittest discover -s tests
```

## Build and publish

Build the source distribution and wheel:

```sh
python3 -m pip install -e ".[dev]"
python3 -m build
python3 -m twine check dist/*
```

Upload to TestPyPI first:

```sh
python3 -m twine upload --repository testpypi dist/*
```

Then upload the same checked artifacts to PyPI:

```sh
python3 -m twine upload dist/*
```
