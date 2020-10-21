import random
import hashlib
import json
import sys

''' Base class for images and also could represent a sheet'''
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __repr__(self):
        return f'<Rectangle> width: {self.width}, height: {self.height}'


'''A type of rectangular image requested by the client'''
class Image(Rectangle):
    def __init__(self, width, height, demand):
        super().__init__(width, height)
        self.demand = demand

    def __repr__(self):
        return f'<Image> width: {self.width}, height: {self.height}, demand: {self.demand}'


'''An image placed on a sheet'''
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

    def __init__(self, width, height, total_diff_images):
        super().__init__(width, height, position=(0, height))
        self.cuts = []
        self.no_images = [0 for _ in range(total_diff_images)]
        self.free_area = width * height
        self.free_rectangles = [FixedRectangle(width, height, position=(0, height))]

    def add_cut(self, image, i):
        self.cuts.append(image)
        self.no_images[i] += 1
        self.free_area -= image.width * image.height

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f'<Bin> width: {self.width}, height: {self.height}, cuts: {self.cuts}, free area: {self.free_area}'
