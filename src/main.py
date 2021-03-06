from genetic_algorithm import Solver
from classes import Rectangle, Sheet
from sys import argv

if __name__ == "__main__":
    with open(f"{argv[1]}", "r") as input_file:
        lines = input_file.readlines()

    [rectangle_width, rectangle_height] = lines[0].split(' ')
    rectangle = Rectangle(int(rectangle_width), int(rectangle_height))
    sheets = []
    for line in lines[1:]:
        [width, height, demand] = line.split(' ')
        sheets.append(Sheet(int(width), int(height), int(demand)))

    # rectangle = Rectangle(70, 70)
    # sheets = [Sheet(25, 25, 2), Sheet(22, 26, 3)]
    solver = Solver()
    solver.solve(rectangle, sheets, output=f"{argv[2]}")
    # solver.solve(rectangle, sheets)
