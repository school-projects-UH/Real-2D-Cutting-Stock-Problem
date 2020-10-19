from classes import *

def find_best_fit(rectangle, free_rectangles):
    best_fit = (1000000, -1)
    for i in range(len(free_rectangles)):
        free_rect = free_rectangles[i]
        if rectangle.width <= free_rect.width and rectangle.height <= free_rect.height:
            shortest_side_fit = min(free_rect.width - rectangle.width, free_rect.height - rectangle.height)
            if shortest_side_fit <= best_fit[0]:
                best_fit = (shortest_side_fit, i)
    return best_fit[1]



def maxrects_bssf(sheet, images):
    free_rectangles = [sheet]
    for img in images:
        pass
