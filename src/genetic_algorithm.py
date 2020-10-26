import math
import random
from random import randint

from bin_pack import maxrects_bssf
from classes import *
from lp_solver import solve_LP


def _pick_two_randoms(top):
    if top == 1:
        return 0, 0
    r1 = randint(0, top-1)
    r2 = None
    if r1 == 0:
        r2 = randint(1, top-1)
    elif r1 == top-1:
        r2 = randint(0, top-2)
    else:
        r2 = [randint(0, r1 - 1), randint(r1 + 1, top - 1)][randint(0, 1)]
    return r1, r2


class Solver():
    def __init__(self, rectangle, sheets, pop_size=10, random_walk_steps=30, hill_climbing_neighbors=10, roulette_pop = 10):
        self.total_sheets = len(sheets)
        self.rectangle = rectangle
        self.sheets = sheets

        self.lb_patterns = math.ceil(sum([s.width * s.height for s in sheets]) / (rectangle.width * rectangle.height)) #lower bound of the number of patterns
        self.ub_sheet = {}  # the number of sheets i which can be placed on one pattern

        for i, sheet in enumerate(sheets):
            self.ub_sheet[i] = math.floor((rectangle.width * rectangle.height) / (sheet.width * sheet.height))

        self.pop_size = pop_size
        self.random_walk_steps = random_walk_steps
        self.hill_climbing_neighbors = hill_climbing_neighbors
        self.roulette_pop = roulette_pop

    def compute_amount_and_fitness(self):
        pass

    def random_walk(self, initial_solution):
        current_solution = initial_solution
        for step in range(self.random_walk_steps):
            new_solution = self.choose_neighbor(current_solution)
            if new_solution != None:
                current_solution = new_solution
        return current_solution

    '''Adds one sheet i in the pattern j'''
    def add(self, solution):
        pattern = random.randint(0,len(solution.bins)-1)
        sheet = random.randint(0, self.total_sheets - 1)
        sheets_per_pattern = dict(solution.sheets_per_pattern)
        sheets_per_pattern[pattern, sheet] += 1
        if sheets_per_pattern[pattern,sheet] >= self.ub_sheet[sheet]:
            return None
        return sheets_per_pattern

    ''' Removes one sheet i from the pattern j'''
    def remove(self, solution):
        pattern = random.randint(0,len(solution.bins)-1)
        sheet = random.randint(0, self.total_sheets - 1)
        sheets_per_pattern = dict(solution.sheets_per_pattern)
        sheets_per_pattern[pattern, sheet] -= 1
        if sheets_per_pattern[pattern,sheet] < 0 or sum([sheets_per_pattern[_pattern, _sheet] for _pattern, _sheet in sheets_per_pattern if _sheet == sheet]) == 0:
            return None
        return sheets_per_pattern

    '''Moves one sheet from a pattern to another one'''
    def move(self, solution):
        pattern_source, pattern_destiny = _pick_two_randoms(len(solution.bins))
        sheet = random.randint(0, self.total_sheets - 1)
        sheets_per_pattern = dict(solution.sheets_per_pattern)

        sheets_per_pattern[pattern_source, sheet] -= 1
        if sheets_per_pattern[pattern_source,sheet] < 0:
            return None

        sheets_per_pattern[pattern_destiny, sheet] += 1
        if sheets_per_pattern[pattern_destiny,sheet] >= self.ub_sheet[sheet]:
            return None

        return sheets_per_pattern

    '''swaps two sheets from two different patterns'''
    def swap(self, solution):
        pattern_one, pattern_two = _pick_two_randoms(len(solution.bins))
        sheet_one, sheet_two = _pick_two_randoms(self.total_sheets)

        sheets_per_pattern = dict(solution.sheets_per_pattern)

        sheets_per_pattern[pattern_one, sheet_one] -= 1
        if sheets_per_pattern[pattern_one, sheet_one] < 0:
            return None

        sheets_per_pattern[pattern_one, sheet_two] += 1
        if sheets_per_pattern[pattern_one, sheet_two] >= self.ub_sheet[sheet_two]:
            return None

        sheets_per_pattern[pattern_two, sheet_two] -= 1
        if sheets_per_pattern[pattern_two, sheet_two] < 0:
            return None

        sheets_per_pattern[pattern_two, sheet_one] += 1
        if sheets_per_pattern[pattern_two, sheet_one] >= self.ub_sheet[sheet_one]:
            return None

        return sheets_per_pattern

    def choose_neighbor(self, solution):
        operator = [self.add, self.remove, self.move, self.swap][randint(0, 3)]
        sheets_per_pattern = operator(solution)

        # if the operator could not be applied
        if sheets_per_pattern == None:
            return None

        bins = []
        # Check the feasibility of the new solution
        for i in range(len(solution.bins)):
            sheets = [Sheet(s.width, s.height, sheets_per_pattern[i, j]) for j,s in enumerate(self.sheets)]
            placement, _ = maxrects_bssf(self.rectangle, sheets)
            if placement == []:
                return None
            bins += placement

        fitness, prints_per_pattern = solve_LP(bins, sheets_per_pattern, self.sheets)
        neighbor = Solution(bins, sheets_per_pattern, prints_per_pattern, fitness)
        return neighbor


    def create_initial_population(self):
        initial_sheets = [Sheet(s.width, s.height, 1) for s in self.sheets]
        placement, sheets_per_pattern = maxrects_bssf(self.rectangle, initial_sheets, unlimited_bins=True)
        fitness, prints_per_pattern = solve_LP(placement, sheets_per_pattern, self.sheets)
        initial_solution = Solution(placement, sheets_per_pattern, prints_per_pattern, fitness)
        initial_population = []
        for _ in range(self.pop_size):
            initial_population.append(self.random_walk(initial_solution))

        return initial_population

    def update_best_solution(self):
        pass

    def roulette_wheel_selection(self, population):
        fitness = [solution.fitness for solution in population]
        total_fit = float(sum(fitness))
        relative_fitness = [f / total_fit for f in fitness]
        probabilities = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]
 
        chosen = []
        for _ in range(self.roulette_pop):
            r = random.random()
            for (i, solution) in enumerate(population):
                if r <= probabilities[i]:
                    chosen.append(solution)
                    break
        return chosen

    def bests_solution_reproduction(self):
        pass

    def crossover(self, Population):
        def select_patterns(parent):
            patterns = [(bin.free_area, bin) for bin in parent.bins]
            patterns.sort()

            # select a number between the [25%, 50%] of the patterns (patterns_len must be >= 4 since 0.25 * 4 = 1)
            count_to_select = len(patterns) >= 4 and \
                                random.randint(0.25 * len(patterns), 0.5 * len(patterns)) or \
                                random.randint(0, len(patterns) - 1)

            return [bin for _, bin in patterns[:count_to_select]]

        P = list(Population)
        parent1 = P[random.randint(0, len(P)-1)]
        P.remove(parent1)
        parent2 = P[random.randint(0, len(P)-1)]

        set_patterns1 = select_patterns(parent1)
        set_patterns2 = select_patterns(parent2)

        all_selected_patterns = list(set(set_patterns1 + set_patterns2))

        covered_sheets = []
        for bin in all_selected_patterns:
            for sheet in bin.cuts:
                covered_sheets.append(sheets)

        sheets_to_process = [Sheet(s.width, s.height, s in covered_sheets and 0 or 1) for s in self.sheets]
        placement, _ = maxrects_bssf(self.rectangle, sheets_to_process, unlimited_bins=True)

        bins = all_selected_patterns + placement
        sheets_per_patterns = { }
        sheets_idx = { (s.width, s.height):i for i,s in enumerate(self.sheets) }

        for bin in range(len(bins)):
            for sheet_idx in range(len(self.sheets)):
                sheets_per_patterns[bin, sheet_idx] = 0

        for j, bin in enumerate(bins):
            for cut in bin.cuts:
                i = sheets_idx[cut.width, cut.height] if not cut.rotated else sheets_idx[cut.height, cut.width]
                sheets_per_patterns[j,i] = sheets_per_patterns[j,i]+1

        fitness, prints_per_pattern = solve_LP(bins, sheets_per_patterns, self.sheets)
        off_spring = Solution(bins, sheets_per_patterns, prints_per_pattern, fitness)
        return self.hill_climbing(off_spring, self.hill_climbing_neighbors)

    def mutation(self, population):
        parent = population[randint(0, len(population)-1)]
        offspring = self.random_walk(parent)
        offspring = self.hill_climbing(offspring, self.hill_climbing_neighbors)
        return offspring


    def hill_climbing(self, solution, no_neighbors):
        current_solution = solution

        while True:
            best_neighbor = current_solution
            for _ in range(no_neighbors):
                new_neighbor = self.choose_neighbor(current_solution)
                if new_neighbor != None and new_neighbor.fitness < best_neighbor.fitness:
                    best_neighbor = new_neighbor

            if best_neighbor.fitness < current_solution.fitness:
                current_solution = best_neighbor
            else:
                break

        return current_solution

    def delete_overproduction(self):
        pass

    def genetic_algorithm(self):
        pass

rectangle = Rectangle(100, 100)
sheets = [Sheet(40, 60, 500), Sheet(50, 50, 1000), Sheet(22, 22, 400), Sheet(70, 40, 2000), Sheet(50, 30, 400)]
solver = Solver(rectangle, sheets)


first_generation = solver.create_initial_population()
print(f'First Generation:\n{first_generation}\n')
intermediate_generation = solver.roulette_wheel_selection(first_generation)
second_generation = solver.crossover(intermediate_generation)
print(f'Second Generation:\n{second_generation}\n')
