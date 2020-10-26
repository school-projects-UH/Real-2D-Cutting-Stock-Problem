from genetic_algorithm import Solver
from classes import Rectangle, Sheet

if __name__ == "__main__":
    input_file = open("input.txt", "r")
    lines = input_file.readlines()
    [rectangle_widht, rectangle_height] = lines[0].split(' ')
    rectangle = Rectangle(int(rectangle_widht), int(rectangle_height))
    sheets = []
    for line in lines[1:]:
        [width, height, demand] = line.split(' ')
        sheets.append(Sheet(int(width), int(height), int(demand)))

    solver = Solver(rectangle, sheets)
    solver.genetic_algorithm()