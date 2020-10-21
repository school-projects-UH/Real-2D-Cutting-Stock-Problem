import unittest
from src.bin_pack import maxrects_bssf
from src.classes import FixedRectangle, Rectangle

class BinPackTestCase(unittest.TestCase):

    def test_1(self):
        sheet = FixedRectangle(50, 50, (0, 50))
        images = [Rectangle(10, 10), Rectangle(20, 8), Rectangle(10, 5), Rectangle(5, 2), Rectangle(20, 30),
            Rectangle(20, 30), Rectangle(10, 3), Rectangle(10, 50), Rectangle(1, 18)]

        placement = maxrects_bssf(sheet, images)

        self.assertTrue(placement == [
            FixedRectangle(width=10, height=10, position=(0, 50), rotated=False),
            FixedRectangle(width=20, height=8, position=(0, 40), rotated=True),
            FixedRectangle(width=10, height=5, position=(0, 20), rotated=True),
            FixedRectangle(width=5, height=2, position=(0, 10), rotated=True),
            FixedRectangle(width=20, height=30, position=(5, 20), rotated=True),
            FixedRectangle(width=20, height=30, position=(10, 50), rotated=False),
            FixedRectangle(width=10, height=3, position=(2, 10), rotated=True),
            FixedRectangle(width=10, height=50, position=(35, 50), rotated=False),
            FixedRectangle(width=1, height=18, position=(8, 40), rotated=False)])
