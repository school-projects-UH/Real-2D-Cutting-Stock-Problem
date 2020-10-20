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

def maxrect_split(rectangle: FixedRectangle, free_rectangle: FixedRectangle):
    new_free_rectangles = set()

    if is_contained(rectangle.top_left, free_rectangle):
        new_free_rectangles.add(FixedRectangle(
            width=rectangle.left - free_rectangle.left,
            height=free_rectangle.height,
            position=free_rectangle.position))
        new_free_rectangles.add(FixedRectangle(
            width=free_rectangle.width,
            height=rectangle.up-free_rectangle.up,
            position=(free_rectangle.left, rectangle.up)))

    if is_contained(rectangle.top_right, free_rectangle):
        new_free_rectangles.add(FixedRectangle(
            width=free_rectangle.right-rectangle.right,
            height=free_rectangle.height,
            position=(rectangle.right, free_rectangle.down)))
        new_free_rectangles.add(FixedRectangle(
            width=free_rectangle.width,
            height=rectangle.up-free_rectangle.up,
            position=(free_rectangle.left, rectangle.up)))

    if is_contained(rectangle.bottom_right, free_rectangle):
        new_free_rectangles.add(FixedRectangle(
            width=free_rectangle.right-rectangle.right,
            height=free_rectangle.height,
            position=(rectangle.right, free_rectangle.down)))
        new_free_rectangles.add(FixedRectangle(
            width=free_rectangle.width,
            height=free_rectangle.down - rectangle.down,
            position=free_rectangle.position))

    if is_contained(rectangle.bottom_left, free_rectangle):
        new_free_rectangles.add(FixedRectangle(
            width=rectangle.left - free_rectangle.left,
            height=free_rectangle.height,
            position=free_rectangle.position))
        new_free_rectangles.add(FixedRectangle(
            width=free_rectangle.width,
            height=free_rectangle.down - rectangle.down,
            position=free_rectangle.position))

    return new_free_rectangles

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
        # free_rect1, free_rect2 = maxrect_split(img, free_rect_to_split)


# print(maxrect_split(FixedRectangle(10, 10, (25, 35)), FixedRectangle(30, 30, (0, 30))))

# free_rect = FixedRectangle(20, 20, (0, 20))
# rect = FixedRectangle(5, 5, (10, 10))
# nfr = maxrect_split(rect, free_rect)

# free_rect = FixedRectangle(30, 30, (10, 30))
# rect = FixedRectangle(20, 10, (0, 20))
# nfr = maxrect_split(rect, free_rect)

# free_rect = FixedRectangle(20, 20, (0, 20))
# rect = FixedRectangle(20, 20, (18, 4))
# nfr = maxrect_split(rect, free_rect)

# for fr in nfr:
#     print(fr)