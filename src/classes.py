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
        super().__init__(width, height)
        self.rotated = rotated
        self.up = position[1] - height
        self.right = position[0] + width
        self.down = position[1]
        self.left = position[0]
        self.bottom_left = position
        self.top_left = position[0], position[1] - height
        self.top_right = position[0] + width, position[1] - height
        self.bottom_right = position[0] + width, position[1]

    def __repr__(self):
        return f'<PlacedImage> width: {self.width}, height: {self.height}, position: {self.bottom_left}, rotated: {self.rotated}'
