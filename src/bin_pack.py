from src.classes import Rectangle, FixedRectangle, Bin, Sheet
from random import random

# Returns a tuple (i, j, need_to_rotate) where i is the index of the bin and j is the index of the free_rectangle that best fits
def find_best_fit(rectangle, bins):
    best_fit = (1000000, -1, -1, False)

    for i,current_bin in enumerate(bins):
        for j,free_rect in enumerate(current_bin.free_rectangles):
            # If the rectangle fits inside the current free rectangle...
            if rectangle.width <= free_rect.width and rectangle.height <= free_rect.height:
                shortest_side_fit = min(free_rect.width - rectangle.width, free_rect.height - rectangle.height)
                if shortest_side_fit < best_fit[0]:
                    best_fit = (shortest_side_fit, i, j, False)
            # Try by rotating the rectangle
            if rectangle.width <= free_rect.height and rectangle.height <= free_rect.width:
                shortest_side_fit = min(free_rect.width - rectangle.height, free_rect.height - rectangle.width)
                if shortest_side_fit < best_fit[0]:
                    best_fit = (shortest_side_fit, i, j, True)
        if best_fit[1] != -1:
            return tuple(best_fit[1:])

    return tuple(best_fit[1:])

def split(rectangle, free_rectangle):
    result = []
    if free_rectangle.width < free_rectangle.height:
        # split horizontally
        if rectangle.height < free_rectangle.height:
            result.append(FixedRectangle(width=free_rectangle.width, height=free_rectangle.height - rectangle.height, position=rectangle.top_left))
        if rectangle.width < free_rectangle.width:
            result.append(FixedRectangle(width=free_rectangle.width - rectangle.width, height=rectangle.height, position=rectangle.bottom_right))
    else:
        # split vertically
        if rectangle.width < free_rectangle.width:
            result.append(FixedRectangle(width=free_rectangle.width - rectangle.width, height=free_rectangle.height, position=rectangle.bottom_right))
        if rectangle.height < free_rectangle.height:
            result.append(FixedRectangle(width=rectangle.width, height=free_rectangle.height - rectangle.height, position=rectangle.top_left))
    return result

def pack_rectangles(rectangle, sheets, unlimited_bins=False):
    # start with an empty bin
    bins = [Bin(width=rectangle.width, height=rectangle.height)]
    p = {}  # p[(i,j)] = number of images of type j on pattern(bin) i

    sheets_list = sorted(sheets, key=lambda sheet: (min(sheet.width, sheet.height), max(sheet.width, sheet.height)), reverse=True)
    use_rectangle_merge = random() < 0.75

    for i, sheet in enumerate(sheets_list):
        for _ in range(sheet.demand):
            # Find globally the best choice: the rectangle wich best fits on a free_rectangle of any bin
            bin_idx, fr_idx, need_to_rotate = find_best_fit(sheet, bins)

            if bin_idx == -1:
                # Add a new bin
                if unlimited_bins:
                    bins.append(Bin(width=rectangle.width, height=rectangle.height))
                    _, _, need_to_rotate = find_best_fit(sheet, [bins[-1]])
                    bin_idx = len(bins) - 1
                    fr_idx = 0
                # not feasible solution
                else:
                    return [], {}

            # update the p vector
            try:
                p[bin_idx, i] += 1
            except KeyError:
                p[bin_idx, i] = 1

            current_bin = bins[bin_idx]
            free_rectangles = current_bin.free_rectangles
            free_rect_to_split = free_rectangles[fr_idx]

            # Place the rectangle that represents the cut at the bottom-left of Fi
            new_cut = FixedRectangle(width=sheet.width, height=sheet.height, position=(free_rect_to_split.bottom_left), rotated=need_to_rotate)
            current_bin.add_cut(new_cut)

            # Perform the split
            free_rectangles.pop(fr_idx)
            free_rectangles += split(new_cut, free_rect_to_split)

            if use_rectangle_merge:
                free_rectangles = {fr for fr in free_rectangles}
                while True:
                    changed = False

                    for fi in free_rectangles:
                        for fj in free_rectangles:
                            if fi == fj: continue
                            if fi.up == fj.up and fi.down == fj.down and min(fi.right, fj.right) == max(fi.left, fj.left):

                                free_rectangles.remove(fi)
                                free_rectangles.remove(fj)
                                free_rectangles.add(FixedRectangle(width=fi.width + fj.width, height=fi.height, position=(min(fi.left, fj.left), fi.down)))
                                changed = True
                            elif fi.left == fj.left and fi.right == fj.right and min(fi.down, fj.down) == max(fi.up, fj.up):

                                free_rectangles.remove(fi)
                                free_rectangles.remove(fj)
                                free_rectangles.add(FixedRectangle(width=fi.width, height=fi.height + fj.height, position=(fi.left, max(fi.down, fj.down))))
                                changed = True
                            if changed:
                                break
                        if changed:
                            break

                    if not changed:
                        break

                current_bin.free_rectangles = [fr for fr in free_rectangles]

    return bins, p
