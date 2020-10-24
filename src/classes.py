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
        return f'<Rectangle> width: {self.width}, height: {self.height}'


'''A type of rectangular sheet requested by the client'''
class Sheet(Rectangle):
    def __init__(self, width, height, demand):
        super().__init__(width, height)
        self.demand = demand

    def __repr__(self):
        return f'<Sheet> width: {self.width}, height: {self.height}, demand: {self.demand}'


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
        return f'\n<FixedRectangle> width: {self.width}, height: {self.height}, position: {self.bottom_left}, rotated: {self.rotated}'

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

    def __repr__(self):
        return f'<Bin> width: {self.width}, height: {self.height}, cuts: {self.cuts}, free area: {self.free_area}'


class Solution:
    def __init__(self, bins, sheets_per_pattern):
        self.bins = bins
        self.sheets_per_pattern = sheets_per_pattern
