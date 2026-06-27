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
