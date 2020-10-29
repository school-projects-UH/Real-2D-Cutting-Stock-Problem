from src.classes import Rectangle, FixedRectangle, Bin, Sheet


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

    return best_fit[1], best_fit[2], best_fit[3]

def maxrect_split(rectangle: FixedRectangle, free_rectangle: FixedRectangle):
    new_free_rectangles = set()

    if rectangle.up > free_rectangle.up and rectangle.up < free_rectangle.down and rectangle.left < free_rectangle.right and rectangle.right > free_rectangle.left:
        new_free_rectangles.add(FixedRectangle(
            width=free_rectangle.width,
            height=rectangle.up - free_rectangle.up,
            position=(free_rectangle.left, rectangle.up)))

    if rectangle.right < free_rectangle.right and rectangle.right > free_rectangle.left and rectangle.up < free_rectangle.down and rectangle.down > free_rectangle.up:
        new_free_rectangles.add(FixedRectangle(
            width=free_rectangle.right - rectangle.right,
            height=free_rectangle.height,
            position=(rectangle.right, free_rectangle.down)))

    if rectangle.down < free_rectangle.down and rectangle.down > free_rectangle.up and rectangle.left < free_rectangle.right and rectangle.right > free_rectangle.left:
        new_free_rectangles.add(FixedRectangle(
            width=free_rectangle.width,
            height=free_rectangle.down - rectangle.down,
            position=(free_rectangle.left, free_rectangle.down)))

    if rectangle.left > free_rectangle.left and rectangle.left < free_rectangle.right and rectangle.down > free_rectangle.up and rectangle.up < free_rectangle.down:
        new_free_rectangles.add(FixedRectangle(
            width=rectangle.left - free_rectangle.left,
            height=free_rectangle.height,
            position=(free_rectangle.left, free_rectangle.down)))

    return list(new_free_rectangles)

def is_contained(point, rectangle):
    x, y = point
    return x > rectangle.left and x < rectangle.right and y > rectangle.up and y < rectangle.down

def is_wrapped(rectangle1, rectangle2):
    return rectangle1.up >= rectangle2.up and rectangle1.right <= rectangle2.right and rectangle1.left >= rectangle2.left and rectangle1.down <= rectangle2.down

def maxrects_bssf(rectangle, sheets, unlimited_bins=False):
    # start with an empty bin
    bins = [Bin(width=rectangle.width, height=rectangle.height)]
    p = {}  # p[(i,j)] = number of images of type j on pattern(bin) i

    for img_idx,img in enumerate(sheets):
        for _ in range(img.demand):

            # Find the free rectangle Fi that best fits and remove it from the free_rectangles list of the corresponding bin
            bin_idx, fr_idx, need_to_rotate = find_best_fit(img, bins)
            if bin_idx == -1:
                # Add a new bin
                if unlimited_bins:
                    bins.append(Bin(width=rectangle.width, height=rectangle.height))
                    bin_idx = len(bins) - 1
                # not feasible solution
                else:
                    return [], {}

            current_bin = bins[bin_idx]
            free_rectangles = current_bin.free_rectangles
            free_rect_to_split = free_rectangles.pop(fr_idx)

            # Place the rectangle that represents the cut at the bottom-left of Fi
            new_cut = FixedRectangle(width=img.width, height=img.height, position=(free_rect_to_split.bottom_left), rotated=need_to_rotate)
            current_bin.add_cut(new_cut, img_idx)

            # update the p vector
            try:
                p[bin_idx, img_idx] += 1
            except KeyError:
                p[bin_idx, img_idx] = 1

            # Perform the split
            free_rectangles += maxrect_split(new_cut, free_rect_to_split)

            # Perform the split on all the free rectangles intersected with the new fixed rectangle
            for fr in free_rectangles.copy():
                l = len(current_bin.free_rectangles)
                free_rectangles += maxrect_split(new_cut, fr)
                if len(free_rectangles) > l or is_wrapped(fr, new_cut):
                    free_rectangles.remove(fr)

            # Remove all free rectangles contained inside another
            fr_copy = free_rectangles.copy()
            for i in range(len(fr_copy)):
                fi = fr_copy[i]
                for j in range(i + 1, len(fr_copy)):
                    fj = fr_copy[j]
                    if is_wrapped(fi, fj):
                        free_rectangles.remove(fi)
                        break

    return bins, p
