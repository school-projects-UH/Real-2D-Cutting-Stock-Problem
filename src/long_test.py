from random import randint, shuffle
from sys import argv
from classes import Rectangle, Sheet
from genetic_algorithm import Solver


class SolverConfig:
    def __init__(self, name, config={}):
        self.total_fitness = 0
        self.total_time = 0
        self.worst_time = 0
        self.worst_fitness = 0
        self.config = config
        self.name = name

    def __repr__(self):
        result = f'{self.name}:\n'
        for key in self.config:
            result += f'{key}: {self.config[key]}\n'
        return result + '\n'

    def call_solver(self, main_sheet, sheets, output):
        solver = Solver()
        solution, time = solver.solve(main_sheet, sheets, **self.config, ret_time=True, output=output)
        fitness = solution.fitness
        self.total_fitness += fitness
        self.total_time += time
        self.worst_time = max(time, self.worst_time)
        self.worst_fitness = max(fitness, self.worst_fitness)

sover_config_list = [
    {},
    {'no_best_solutions': 15},
    {'no_best_solutions': 5},
    {'pop_size': 80},
    {'random_walk_steps': 150},
    {'random_walk_steps': 75},
    {'hill_climbing_neighbors': 40},
    {'no_generations': 50},
    {'prob_crossover': 0.90},
    {'prob_crossover': 0.60},
    {'roulette_pop': 60},
    {'roulette_pop': 30}]
sover_config_list = [SolverConfig(f'SolverNo{i + 1}', sover_config_list[i]) for i in range(len(sover_config_list))]

no_tests = int(argv[1])
for i in range(no_tests):
    # generate the main sheet dimensions
    main_sheet_width = randint(20, 200)
    main_sheet_height = randint(20, 200)
    main_sheet = Rectangle(main_sheet_width, main_sheet_height)

    # generate the list of sheets
    no_sheets = randint(1, 12)
    sheets = []
    for _ in range(no_sheets):
        sheet_dimensions = [randint(5, max(main_sheet_width, main_sheet_height)), randint(5, min(main_sheet_width, main_sheet_height))]
        shuffle(sheet_dimensions)
        [sheet_width, sheet_height] = sheet_dimensions
        sheet_demand = randint(1, 1000000)
        sheets.append(Sheet(sheet_width, sheet_height, sheet_demand))

    test_info = f'TestNo: {i + 1}\n'
    test_info += f'{main_sheet_width} {main_sheet_height}\n'
    test_info += '\n'.join([f'{sheet.width} {sheet.height} {sheet.demand}' for sheet in sheets]) + '\n'
    print(test_info)
    with open(f'tests/test{i + 1}.txt', "w") as input_file:
        input_file.write('\n'.join(test_info.split('\n')[1:-1]))

    for solver_config in sover_config_list:
        print(f"\nCalling {solver_config.name}...\n")
        solver_config.call_solver(main_sheet, sheets, output=f'tests/results/testNo{i + 1}_{solver_config.name}.txt')

sorted_by_fitness = sorted(sover_config_list, key=lambda sc: sc.total_fitness)
sorted_by_time = sorted(sover_config_list, key=lambda sc: sc.total_time)
sorted_by_worst_fitness = sorted(sover_config_list, key=lambda sc: sc.worst_fitness)
sorted_by_worst_time = sorted(sover_config_list, key=lambda sc: sc.worst_time)

results_by_fitness = open('tests/results/results_by_fitness.txt', "w")
for i, result in enumerate(sorted_by_fitness):
    results_by_fitness.write(f'{i + 1}- {result.name, result.total_fitness / sorted_by_fitness[0].total_fitness}\n')

results_by_time = open('tests/results/results_by_time.txt', "w")
for i, result in enumerate(sorted_by_time):
    results_by_time.write(f'{i + 1}- {result.name, result.total_time / no_tests}\n')

results_by_worst_fitness = open('tests/results/results_by_worst_fitness.txt', "w")
for i, result in enumerate(sorted_by_worst_fitness):
    results_by_worst_fitness.write(f'{i + 1}- {result.name, result.worst_fitness}\n')

results_by_worst_time = open('tests/results/results_by_worst_time.txt', "w")
for i, result in enumerate(sorted_by_worst_time):
    results_by_worst_time.write(f'{i + 1}- {result.name, result.worst_time}\n')
