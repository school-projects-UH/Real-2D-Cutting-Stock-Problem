from src.genetic_algorithm import Solver
from src.classes import Rectangle, Sheet
import os
from time import time
base_path = os.path.curdir + "/tests/collection/"

solver = Solver()

for test_case in os.listdir(base_path):
    if os.path.isdir(base_path + test_case): continue
    with open(base_path + test_case, "r") as input_file:
        lines = input_file.readlines()
        [rectangle_width, rectangle_height] = lines[0].split(' ')
        rectangle = Rectangle(int(rectangle_width), int(rectangle_height))
        sheets = []
        for line in lines[1:]:
            [width, height, demand] = line.split(' ')
            sheets.append(Sheet(int(width), int(height), int(demand)))
        solver.solve(rectangle, sheets, output=f"{base_path}results/{test_case[:-4]}_output_{time()}.txt")
