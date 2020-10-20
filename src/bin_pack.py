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
        if rectangle.width <= free_rect.height and rectangle.height <= free_rect.width:
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

    return list(new_free_rectangles)

def is_contained(point, rectangle):
    x, y = point
    return x > rectangle.left and x < rectangle.right and y > rectangle.up and y < rectangle.down

def is_wrapped(rectangle1, rectangle2):
    return rectangle1.up >= rectangle2.up and rectangle1.right <= rectangle2.right and rectangle1.left >= rectangle2.left and rectangle1.down <= rectangle2.down

def maxrects_bssf(sheet, images):
    free_rectangles = [FixedRectangle(width=sheet.width, height=sheet.height, position=(0, sheet.height))]
    placement = []
    for img in images:
        print(f'Image: {img}')
        print(f'Free rectangles: {free_rectangles}')
        # Find the free Fi rectangle that best fits and remove it from the free_rectangles list
        idx, need_to_rotate = find_best_fit(img, free_rectangles)
        free_rect_to_split = free_rectangles.pop(idx)
        print(f'Idx: {idx}')
        print(f'Need to rotate: {need_to_rotate}')

        fixed_rectangle = FixedRectangle(width=img.width, height=img.height, position=(free_rect_to_split.bottom_left), rotated=need_to_rotate)

        # Place the rectangle at the bottom-left of Fi
        placement.append(fixed_rectangle)

        print(f'Rectangle to place at the bottom-left: {fixed_rectangle}')
        print(f'Rectangle to split: {free_rect_to_split}')
        # Perform the split
        free_rectangles += maxrect_split(fixed_rectangle, free_rect_to_split)
        print(f'new free rectangles: {maxrect_split(fixed_rectangle, free_rect_to_split)}')
        print(f'free_rectangles after the first split: {free_rectangles}')

        for fr in free_rectangles.copy():
            l = len(free_rectangles)
            free_rectangles += maxrect_split(fixed_rectangle ,fr)
            if len(free_rectangles) > l:
                free_rectangles.remove(fr)
        print(f'free_rectangles after the second split: {free_rectangles}')

        fr_copy = free_rectangles.copy()
        for i in range(len(fr_copy)):
            fi = fr_copy[i]
            for j in range(i + 1, len(fr_copy)):
                fj = fr_copy[j]
                if is_wrapped(fi, fj):
                    free_rectangles.pop(i)
                    break
        print(f'free_rectangles after the elimination of the wrapped ones')
        print('-----------------------------------------------------------\n')

    return placement



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

# print(nfr)

# print(is_wrapped(FixedRectangle(5, 5, (10, 10)), FixedRectangle(20, 20, (0, 20))))
# print(is_wrapped(FixedRectangle(5, 5, (18, 10)), FixedRectangle(20, 20, (0, 20))))
# print(is_wrapped(FixedRectangle(5, 5, (80, 80)), FixedRectangle(20, 20, (0, 20))))
# print(is_wrapped(FixedRectangle(20, 20, (0, 20)), FixedRectangle(20, 20, (0, 20))))

sheet = FixedRectangle(50, 50, (0, 50))
images = [Rectangle(10, 10), Rectangle(20, 8)]

print(maxrects_bssf(sheet, images))
