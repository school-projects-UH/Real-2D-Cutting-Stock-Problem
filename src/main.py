from genetic_algorithm import Solver
from classes import Rectangle, Sheet
from sys import argv

if __name__ == "__main__":

    input_file = open(f"{argv[1]}", "r")
    lines = input_file.readlines()
    [rectangle_widht, rectangle_height] = lines[0].split(' ')
    rectangle = Rectangle(int(rectangle_widht), int(rectangle_height))
    sheets = []
    for line in lines[1:]:
        [width, height, demand] = line.split(' ')
        sheets.append(Sheet(int(width), int(height), int(demand)))

    solver = Solver(rectangle, sheets, pop_size=25, no_generations=30, hill_climbing_neighbors=25, roulette_pop=20, no_best_solutions=5)
    solver.genetic_algorithm()
