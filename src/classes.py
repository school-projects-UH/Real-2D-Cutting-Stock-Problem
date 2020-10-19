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
class PlacedImage(Rectangle):
    def __init__(self, width, height, position, rotated=False):
        super().__init__(width, height)
        self.position = position
        self.rotated = rotated

    def __repr__(self):
        return f'<PlacedImage> width: {self.width}, height: {self.height}, position: {self.position}, rotated: {self.rotated}'
