"""Headless smoke tests: geometry and composition, no curses required."""

import unittest

from cannaleaf.model import LeafParams, rasterize
from cannaleaf.render import ASCII_RAMP, BRAILLE_BASE, compose


class RasterizeTest(unittest.TestCase):
    def test_fills_a_leaf_worth_of_pixels(self):
        grid, anchor = rasterize(LeafParams(), 160, 96)
        filled = [v for row in grid for v in row if v >= 0]
        self.assertGreater(len(filled), 1000)
        self.assertTrue(all(0.0 <= v <= 1.0 for v in filled))
        self.assertTrue(0 < anchor < 96)

    def test_leaflet_count_changes_silhouette(self):
        slim, _ = rasterize(LeafParams(leaflets=3), 160, 96)
        full, _ = rasterize(LeafParams(leaflets=13), 160, 96)
        count = lambda g: sum(1 for row in g for v in row if v >= 0)
        self.assertLess(count(slim), count(full))

    def test_tiny_grid_does_not_crash(self):
        grid, _ = rasterize(LeafParams(), 8, 8)
        self.assertEqual(len(grid), 8)


class ComposeTest(unittest.TestCase):
    def setUp(self):
        self.grid, _ = rasterize(LeafParams(), 160, 96)

    def test_braille_cells(self):
        cells = compose(self.grid, 160, 96, 80, 24, [0] * 96, False)
        self.assertEqual(len(cells), 24)
        self.assertEqual(len(cells[0]), 80)
        lit = [(ch, sh) for row in cells for ch, sh in row if sh is not None]
        self.assertGreater(len(lit), 100)
        self.assertTrue(all(BRAILLE_BASE < ord(ch) <= BRAILLE_BASE + 0xFF
                            for ch, _ in lit))
        self.assertTrue(all(0.0 <= sh <= 1.0 for _, sh in lit))

    def test_ascii_cells(self):
        cells = compose(self.grid, 160, 96, 80, 24, [0] * 96, True)
        lit = [ch for row in cells for ch, sh in row if sh is not None]
        self.assertGreater(len(lit), 100)
        self.assertTrue(all(ch in ASCII_RAMP for ch in lit))

    def test_sway_offset_shifts_columns(self):
        flat = compose(self.grid, 160, 96, 80, 24, [0] * 96, False)
        bent = compose(self.grid, 160, 96, 80, 24, [6] * 96, False)
        first_lit = lambda cells: min(c for row in cells for c, (_, sh)
                                      in enumerate(row) if sh is not None)
        self.assertEqual(first_lit(bent), first_lit(flat) + 3)


if __name__ == "__main__":
    unittest.main()
