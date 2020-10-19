''' Base class for images and also could represent a sheet'''
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

'''A type of rectangular image requested by the client'''
class Image(Rectangle):
    def __init__(self, width, height, demand):
        super.__init__(width, height)
        self.demand = demand

'''An image placed on a sheet'''
class PlacedImage(Rectangle):
    def __init__(self, width, height, position, rotated):
        super().__init__(width, height)
        self.position = position
        self.rotated = rotated

