import unittest
from src.bin_pack import maxrects_bssf, find_best_fit
from src.classes import FixedRectangle, Rectangle, Bin

class BinPackTestCase(unittest.TestCase):

    def test_find_best_fit_one_bin(self):
        rect = Rectangle(10, 58)
        b1 = Bin(100, 100, 12)
        b1.free_rectangles = [Rectangle(70, 80), Rectangle(60, 60)]
        bins = [b1]

        best_fit = find_best_fit(rect, bins)
        self.assertTrue(best_fit == (0, 1, False), msg=best_fit)

    def test_find_best_fit_more_than_one_bin(self):
        rect = Rectangle(30, 30)
        b1 = Bin(100, 100, 12)
        b1.free_rectangles = [Rectangle(40, 80), Rectangle(60, 60), Rectangle(20, 80), Rectangle(32, 32)]
        b2 = Bin(100, 100, 12)
        b2.free_rectangles = [Rectangle(30, 40), Rectangle(10, 2)]
        bins = [b1, b2]

        best_fit = find_best_fit(rect, bins)
        self.assertTrue(best_fit == (1, 0, False), msg=best_fit)

    def test_find_best_fit_no_solution(self):
        rect = Rectangle(30, 30)
        b1 = Bin(100, 100, 12)
        b1.free_rectangles = [Rectangle(20, 10)]
        b2 = Bin(100, 100, 12)
        b2.free_rectangles = [Rectangle(10, 15)]
        bins = [b1, b2]

        best_fit = find_best_fit(rect, bins)
        self.assertTrue(best_fit == (-1, -1, False), msg=best_fit)

    def test_maxrects_bssf_one_bin(self):
        sheet = FixedRectangle(50, 50, (0, 50))
        images = [Rectangle(10, 10), Rectangle(20, 8), Rectangle(10, 5), Rectangle(5, 2), Rectangle(20, 30),
            Rectangle(20, 30), Rectangle(10, 3), Rectangle(10, 50), Rectangle(1, 18)]

        placement = maxrects_bssf(sheet, images)

        self.assertTrue(len(placement) == 1)
        self.assertTrue(placement[0].cuts == [
            FixedRectangle(width=10, height=10, position=(0, 50), rotated=False),
            FixedRectangle(width=20, height=8, position=(0, 40), rotated=True),
            FixedRectangle(width=10, height=5, position=(0, 20), rotated=True),
            FixedRectangle(width=5, height=2, position=(0, 10), rotated=True),
            FixedRectangle(width=20, height=30, position=(5, 20), rotated=True),
            FixedRectangle(width=20, height=30, position=(10, 50), rotated=False),
            FixedRectangle(width=10, height=3, position=(2, 10), rotated=True),
            FixedRectangle(width=10, height=50, position=(35, 50), rotated=False),
            FixedRectangle(width=1, height=18, position=(8, 40), rotated=False)])

    def test_maxrects_bssf_more_than_one_bin(self):
        sheet = FixedRectangle(15, 15, (0, 15))
        images = [Rectangle(10, 5), Rectangle(8, 5), Rectangle(8, 8), Rectangle(3, 15)]
        placement = maxrects_bssf(sheet, images, ilimited_bins=True)

        b1_cuts = [
            FixedRectangle(width=10, height=5, position=(0,15)),
            FixedRectangle(width=8, height=5, position=(10,15), rotated=True),
            FixedRectangle(width=8, height=8, position=(0,10))]
        b2_cuts = [FixedRectangle(width=3, height=15, position=(0,15))]

        self.assertTrue(list(map(lambda b: b.cuts, placement)) == [b1_cuts, b2_cuts])
    
    def test_maxrects_bssf_no_solution(self):
        sheet = FixedRectangle(15, 15, (0, 15))
        images = [Rectangle(10, 5), Rectangle(8, 5), Rectangle(8, 8), Rectangle(3, 15)]
        placement = maxrects_bssf(sheet, images)

        self.assertListEqual(placement, [])
