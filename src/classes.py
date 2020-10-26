import random
import hashlib
import json
import sys

''' Base class for sheet'''
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __repr__(self):
        return f'{self.width} X {self.height}\n'
    
    def __eq__(self, other):
        return isinstance(other, Rectangle) and self.width == other.width and self.height == other.height
    
    def __hash__(self):
        return hash((self.width, self.height))


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

    def __eq__(self , other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f'{self.position}: {self.width} X {self.height}'

    def __hash__(self):
        return int.from_bytes(hashlib.sha256(json.dumps(self.__dict__).encode()).digest(), byteorder=sys.byteorder)


class Bin(FixedRectangle):

    def __init__(self, width, height):
        super().__init__(width, height, position=(0, height))
        self.cuts = []
        self.free_area = width * height
        self.free_rectangles = [FixedRectangle(width, height, position=(0, height))]

    def add_cut(self, sheet, i):
        self.cuts.append(sheet)
        self.free_area -= sheet.width * sheet.height

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __gt__(self, other):
        return self.free_area > other.free_area

    def __hash__(self):
        return random.randint(0, 100000000000000000000000000000000000000000000000000000000000000000)

    def __repr__(self):
        result = ''
        for cut in self.cuts:
            result += str(cut) + '  '
        result += f'\nfree space: {self.free_area}   '
        return result


class Solution:
    def __init__(self, bins, sheets_per_pattern, prints_per_pattern, fitness):
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