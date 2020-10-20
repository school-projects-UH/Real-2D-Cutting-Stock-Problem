from classes import *

def find_best_fit(rectangle, free_rectangles):
    best_fit = (1000000, -1, False)
    for i in range(len(free_rectangles)):
        free_rect = free_rectangles[i]
        if rectangle.width <= free_rect.width and rectangle.height <= free_rect.height:
            shortest_side_fit = min(free_rect.width - rectangle.width, free_rect.height - rectangle.height)
            if shortest_side_fit < best_fit[0]:
                best_fit = (shortest_side_fit, i, False)
        # Try by rotating the rectangle
        elif rectangle.width <= free_rect.height and rectangle.height <= free_rect.width:
            shortest_side_fit = min(free_rect.width - rectangle.height, free_rect.height - rectangle.width)
            if shortest_side_fit < best_fit[0]:
                best_fit = (shortest_side_fit, i, True)
    return best_fit[1], best_fit[2]

def maxrect_split(rectangle, free_rectangle):
    xf, yf = free_rectangle.position
    wf, hf = free_rectangle.width, free_rectangle.height
    w, h = rectangle.width, rectangle.height

    free_rect1 = PlacedImage(width=wf, height=hf - h, position=(xf, yf - h))
    free_rect2 = PlacedImage(width=wf - w, height=hf, position=(xf + w, yf))

    return (free_rect1, free_rect2)

def is_contained(point, rectangle):
    x, y = point
    up, right, down, left = rectangle.position[1] - rectangle.height, rectangle.position[0] + rectangle.width, rectangle.position[1], rectangle.position[0]
    return x > left and x < right and y > up and y < down

# def maxrect_split_up_to_four(rectangle, free_rectangle):
#     x, y = rectangle.position
#     w, h = rectangle.width, rectangle.height

def maxrects_bssf(sheet, images):
    free_rectangles = [PlacedImage(width=sheet.width, height=sheet.height, position=(0, sheet.height))]
    placement = []
    for img in images:
        # Find the free Fi rectangle that best fits and remove it from the free_rectangles list
        idx, need_to_rotate = find_best_fit(img, free_rectangles)
        free_rect_to_split = free_rectangles.pop(idx)

        # Place the rectangle at the bottom-left of Fi
        placement.append(PlacedImage(width=img.width, height=img.height, position=(free_rect_to_split.position), rotated=need_to_rotate))

        # Perform the split
        free_rect1, free_rect2 = maxrect_split(img, free_rect_to_split)
