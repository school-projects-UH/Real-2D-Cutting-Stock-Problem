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
    xf, yf = free_rectangle.bottom_left
    wf, hf = free_rectangle.width, free_rectangle.height
    w, h = rectangle.width, rectangle.height

    free_rect1 = FixedRectangle(width=wf, height=hf - h, position=(xf, yf - h))
    free_rect2 = FixedRectangle(width=wf - w, height=hf, position=(xf + w, yf))

    return (free_rect1, free_rect2)

def is_contained(point, rectangle):
    x, y = point
    return x > rectangle.left and x < rectangle.right and y > rectangle.up and y < rectangle.down

def maxrects_bssf(sheet, images):
    free_rectangles = [FixedRectangle(width=sheet.width, height=sheet.height, position=(0, sheet.height))]
    placement = []
    for img in images:
        # Find the free Fi rectangle that best fits and remove it from the free_rectangles list
        idx, need_to_rotate = find_best_fit(img, free_rectangles)
        free_rect_to_split = free_rectangles.pop(idx)

        # Place the rectangle at the bottom-left of Fi
        placement.append(FixedRectangle(width=img.width, height=img.height, position=(free_rect_to_split.bottom_left), rotated=need_to_rotate))

        # Perform the split
        free_rect1, free_rect2 = maxrect_split(img, free_rect_to_split)
