from classes import Rectangle, FixedRectangle, Bin, Sheet

# Returns a tuple (r, i, j, need_to_rotate) where r is the index of the sheet we are going to place, i is the index of the bin and j is the index of the free_rectangle that best fits
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

    return tuple(best_fit[1:])


def split(rectangle, free_rectangle):
    result = []
    if free_rectangle.width < free_rectangle.height:
        if rectangle.height < free_rectangle.height:
            result.append(FixedRectangle(width=free_rectangle.width, height=free_rectangle.height - rectangle.height, position=rectangle.top_left))
        if rectangle.width < free_rectangle.width:
            result.append(FixedRectangle(width=free_rectangle.width - rectangle.width, height=rectangle.height, position=rectangle.bottom_right))
    else:
        if rectangle.width < free_rectangle.width:
            result.append(FixedRectangle(width=free_rectangle.width - rectangle.width, height=free_rectangle.height, position=rectangle.bottom_right))
        if rectangle.height < free_rectangle.height:
            result.append(FixedRectangle(width=rectangle.width, height=free_rectangle.height - rectangle.height, position=rectangle.top_left))
    return result

def maxrects_bssf(rectangle, sheets, unlimited_bins=False):
    # start with an empty bin
    bins = [Bin(width=rectangle.width, height=rectangle.height)]
    p = {}  # p[(i,j)] = number of images of type j on pattern(bin) i

    for i, sheet in enumerate(sheets):
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

    return bins, p

bins, _ = maxrects_bssf(Rectangle(100, 70), [Sheet(25, 25, 2), Sheet(30, 40, 4)], unlimited_bins=True)
print(bins)