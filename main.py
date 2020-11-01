from src.genetic_algorithm import Solver
from src.classes import Rectangle, Sheet
from sys import argv

if __name__ == "__main__":
    input_file = open(f"input.txt", "r")
    lines = input_file.readlines()
    [rectangle_width, rectangle_height] = lines[0].split(' ')
    rectangle = Rectangle(int(rectangle_width), int(rectangle_height))
    sheets = []
    for line in lines[1:]:
        [width, height, demand] = line.split(' ')
        sheets.append(Sheet(int(width), int(height), int(demand)))

    solver = Solver(rectangle, sheets, output="output.txt")
    solver.genetic_algorithm()
