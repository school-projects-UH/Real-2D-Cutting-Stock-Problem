import random
import hashlib
import json
import sys

from collections import namedtuple
Rect = namedtuple('Rect', ['value', 'direction'])

''' Base class for sheet'''
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __repr__(self):
        return f'{self.width} X {self.height}\n'

    def __eq__(self, other):
        return isinstance(other, Rectangle) and self.width == other.width and self.height == other.height



'''A type of rectangular sheet requested by the client'''
class Sheet(Rectangle):
    def __init__(self, width, height, demand):
        super().__init__(width, height)
        self.demand = demand

    def __repr__(self):
        return f'{self.width} X {self.height}: {self.demand}\n'


'''An sheet placed on a rectangle'''
class FixedRectangle(Rectangle):
    def __init__(self, width, height, position, rotated=False):
        if rotated:
            super().__init__(height, width)
        else:
            super().__init__(width, height)

        self.rotated = rotated
        self.position = position

        self.up = position[1] - self.height
        self.right = position[0] + self.width
        self.down = position[1]
        self.left = position[0]

        self.bottom_left = position
        self.top_left = position[0], position[1] - self.height
        self.top_right = position[0] + self.width, position[1] - self.height
        self.bottom_right = position[0] + self.width, position[1]

    @staticmethod
    def create_from_tuple(info):
        width, height, pos, rotated = info
        if rotated:
            return FixedRectangle(height, width, pos, rotated=True)
        return FixedRectangle(width, height, pos)

    def as_tuple(self):
        return (self.width, self.height, self.position, self.rotated)

    def __repr__(self):
        # return f'topleft {self.top_left} , position {self.position}: {self.width} X {self.height}'
        return f'{self.position}: {self.width} X {self.height}'

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __hash__(self):
        return hash(self.as_tuple())


class Bin(FixedRectangle):

    def __init__(self, width, height, position=None):
        super().__init__(width, height, position=position)
        self.cuts = []
        self.free_area = width * height
        self.free_rectangles = [FixedRectangle(width, height, position=position)]

    def add_cut(self, sheet):
        self.cuts.append(sheet)
        self.free_area -= sheet.width * sheet.height

    def __repr__(self):
        result = ''
        for cut in self.cuts:
            result += str(cut) + '  '
        result += f'\nfree space: {self.free_area}   '
        return result

    def split(self, r: Rect):
        B1, B2 = None, None
        if r.direction == 'h':
            B1 = Bin(self.width, r.value - self.up, position=(self.left, r.value))
            B2 = Bin(self.width, self.down - r.value, position=(self.left, self.down))
            for c in self.cuts:
                if c.down <= r.value:
                    B1.add_cut(c)
                else:
                    B2.add_cut(c)
        else:
            B1 = Bin(r.value - self.left, self.height, position=(self.left, self.down))
            B2 = Bin(self.right - r.value, self.height, position=(r.value, self.down))
            for c in self.cuts:
                if c.right <= r.value:
                    B1.add_cut(c)
                else:
                    B2.add_cut(c)
        return B1, B2

    def find_cut(self):
        # print(self.cuts)
        for cut in self.cuts:
            if cut.up > self.up:
                if any(map(lambda c: c.up < cut.up and c.down > cut.up, self.cuts)):
                    pass
                else:
                    return Rect(cut.up, 'h')
            if cut.down < self.down:
                if any(map(lambda c: c.up < cut.down and c.down > cut.down, self.cuts)):
                    pass
                else:
                    return Rect(cut.down, 'h')
            if cut.left > self.left:
                if any(map(lambda c: c.left < cut.left and c.right > cut.left, self.cuts)):
                    pass
                else:
                    return Rect(cut.left, 'v')
            if cut.right < self.right:
                if any(map(lambda c: c.left < cut.right and c.right > cut.right, self.cuts)):
                    pass
                else:
                    return Rect(cut.right, 'v')
        raise Exception()
        # assert(False, "There should be always a guillotine cut")

    def list_cuts(self):
        # print(self.cuts)
        if self.cuts == []:
            return []
        if len(self.cuts) == 1 and self.cuts[0].width == self.width and self.cuts[0].height == self.height:
            return []

        cut = self.find_cut()
        p = None
        if cut.direction == 'h':
            p = (self.left, cut.value, 'right')
        else:
            p = (cut.value, self.down, 'up')
        # print(cut)
        B1, B2 = self.split(cut)

        return [p] + B1.list_cuts() + B2.list_cuts()

class Solution:
    def __init__(self, bins, sheets_per_pattern, prints_per_pattern=None, fitness=None):
        self.bins = bins
        self.sheets_per_pattern = sheets_per_pattern
        self.prints_per_pattern = prints_per_pattern
        self.fitness = fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __repr__(self):
        result = ''
        for idx,bin in enumerate(self.bins):
            result += str(bin)
            result += f'No. of prints: ' + str(self.prints_per_pattern[f'x{idx}']) + '\n\n'
        result += f'fitness: {self.fitness}\n'
        return result
