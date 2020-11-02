import math
import random
from random import randint

from src.bin_pack import maxrects_bssf
from src.classes import Solution, Sheet
from src.lp_solver import solve_LP
import time

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
    def __init__(self, pop_size=60, random_walk_steps=100, hill_climbing_neighbors=25, roulette_pop = 45, no_best_solutions=10, no_generations=30, prob_crossover=0.75):
        self.pop_size = pop_size
        self.random_walk_steps = random_walk_steps
        self.hill_climbing_neighbors = hill_climbing_neighbors
        self.roulette_pop = roulette_pop
        self.no_best_solutions = no_best_solutions
        self.no_generations = no_generations
        self.prob_crossover=prob_crossover

    def solve(self, rectangle, sheets,  output=None):
        self.total_sheets = len(sheets)
        self.rectangle = rectangle
        self.sheets = sheets

        self.lb_patterns = math.ceil(sum(
            [s.width * s.height for s in sheets]) / (rectangle.width * rectangle.height)) #lower bound of the number of patterns
        self.ub_sheet = {}  # the number of sheets i which can be placed on one pattern

        for i, sheet in enumerate(sheets):
            self.ub_sheet[i] = math.floor((rectangle.width * rectangle.height) / (sheet.width * sheet.height))

        start_time = time.time()
        solution = self.genetic_algorithm()
        end_time = time.time()
        exec_time = end_time - start_time

        if output != None:
            with open(output, "w") as output_file:
                output_file.write(f"Input data:\nMain sheet: {rectangle}")
                output_file.write("Orders:\n")
                for sheet in self.sheets:
                    output_file.write(str(sheet))
                output_file.write(f"\nParameters:\nPopulation size: {self.pop_size}\nNo. generations: {self.no_generations}\nRandom walk steps: {self.random_walk_steps}\nHill climbing neighbors: {self.hill_climbing_neighbors}\nNo. best solutions: {self.no_best_solutions}\nRoulette population size: {self.roulette_pop}\nCrossover probability: {self.prob_crossover}")
                output_file.write("\n\n")
                output_file.write(f"Output:\n{solution}")
                output_file.write(f"Time:{exec_time} seconds")

        return solution

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
        try:
            sheets_per_pattern[pattern, sheet] += 1
        except KeyError:
            sheets_per_pattern[pattern, sheet] = 1
        if sheets_per_pattern[pattern,sheet] >= self.ub_sheet[sheet]:
            return None
        return sheets_per_pattern

    ''' Removes one sheet i from the pattern j'''
    def remove(self, solution):
        pattern = random.randint(0,len(solution.bins)-1)
        sheet = random.randint(0, self.total_sheets - 1)
        sheets_per_pattern = dict(solution.sheets_per_pattern)
        try:
            sheets_per_pattern[pattern, sheet] -= 1
        except KeyError:
            return None

        if sheets_per_pattern[pattern, sheet] < 0 or sum([sheets_per_pattern[_pattern, _sheet] for _pattern, _sheet in sheets_per_pattern if _sheet == sheet]) == 0:
            return None

        return sheets_per_pattern

    '''Moves one sheet from a pattern to another one'''
    def move(self, solution):
        pattern_source, pattern_destiny = _pick_two_randoms(len(solution.bins))
        sheet = random.randint(0, self.total_sheets - 1)
        sheets_per_pattern = dict(solution.sheets_per_pattern)
        try:
            sheets_per_pattern[pattern_source, sheet] -= 1
        except KeyError:
            return None
        try:
            sheets_per_pattern[pattern_destiny, sheet] += 1
        except KeyError:
            sheets_per_pattern[pattern_destiny, sheet] = 1

        if  sheets_per_pattern[pattern_source, sheet] < 0 or \
            sheets_per_pattern[pattern_destiny,sheet] >= self.ub_sheet[sheet]:
            return None

        return sheets_per_pattern

    '''swaps two sheets from two different patterns'''
    def swap(self, solution):
        pattern_one, pattern_two = _pick_two_randoms(len(solution.bins))
        sheet_one, sheet_two = _pick_two_randoms(self.total_sheets)

        sheets_per_pattern = dict(solution.sheets_per_pattern)
        try:
            sheets_per_pattern[pattern_one, sheet_one] -= 1
            sheets_per_pattern[pattern_two, sheet_two] -= 1
        except KeyError:
            return None

        try:
            sheets_per_pattern[pattern_one, sheet_two] += 1
        except KeyError:
            sheets_per_pattern[pattern_one, sheet_two] = 1

        try:
            sheets_per_pattern[pattern_two, sheet_one] += 1
        except KeyError:
            sheets_per_pattern[pattern_two, sheet_one] = 1

        if sheets_per_pattern[pattern_one, sheet_one] < 0 or \
            sheets_per_pattern[pattern_two, sheet_two] < 0 or \
            sheets_per_pattern[pattern_one, sheet_two] >= self.ub_sheet[sheet_two] or \
            sheets_per_pattern[pattern_two, sheet_one] >= self.ub_sheet[sheet_one]:
            return None

        return sheets_per_pattern

    def choose_neighbor(self, solution):
        operators = [self.add, self.remove, self.move, self.swap]
        if (len(solution.bins) == 1):
            operators = [self.add, self.remove]
        operator = operators[randint(0, len(operators) - 1)]
        sheets_per_pattern = operator(solution)

        # if the operator could not be applied
        if sheets_per_pattern == None:
            return None

        bins = []
        # Check the feasibility of the new solution
        for i in range(len(solution.bins)):
            sheets = [Sheet(s.width, s.height, sheets_per_pattern[i, j]) for (j,s) in enumerate(self.sheets) if (i,j) in sheets_per_pattern]
            placement, _ = maxrects_bssf(self.rectangle, sheets)
            if placement == []:
                return None
            bins += placement
        try:
            fitness, prints_per_pattern = solve_LP(bins, sheets_per_pattern, self.sheets)
        except:
            return self.choose_neighbor(solution)
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

    def update_best_solution(self, population):
        best_solution = population[0]
        for solution in population:
            if solution.fitness < best_solution.fitness:
                best_solution = solution
        return best_solution

    def roulette_wheel_rank_based_selection(self, population):
        solutions = [(solution.fitness, solution) for solution in population]
        solutions.sort()
        n = len(population)
        fitness = [i for i in range(n,0,-1)]
        # Use the gauss formula to get the sum of all ranks (sum of integers 1 to N).
        total_fit = n * (n + 1) / 2
        relative_fitness = [f / total_fit for f in fitness]
        probabilities = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]

        chosen = []
        for _ in range(self.roulette_pop):
            r = random.random()
            for (i, pair) in enumerate(solutions):
                if r <= probabilities[i]:
                    _ , solution = pair
                    chosen.append(solution)
                    break
        return chosen

    def bests_solution_reproduction(self, population):
        solutions = [(solution.fitness, solution) for solution in population]
        solutions.sort()
        return [solution for (_, solution) in solutions[:self.no_best_solutions]]

    def crossover(self, Population):
        def select_patterns(parent):
            patterns = [(bin.free_area, bin) for bin in parent.bins]
            patterns.sort()

            # select a number between the [25%, 50%] of the patterns (patterns_len must be >= 4 since 0.25 * 4 = 1)
            count_to_select = len(patterns) >= 4 and \
                                random.randint(math.ceil(0.25 * len(patterns)),math.floor(0.5 * len(patterns))) or \
                                random.randint(0, len(patterns) - 1)

            return [bin for _, bin in patterns[:count_to_select]]

        r1, r2 = _pick_two_randoms(len(Population) - 1)
        parent1, parent2 = Population[r1], Population[r2]
        set_patterns1 = select_patterns(parent1)
        set_patterns2 = select_patterns(parent2)

        all_selected_patterns = list(set(set_patterns1 + set_patterns2))

        covered_sheets = []
        for bin in all_selected_patterns:
            for sheet in bin.cuts:
                covered_sheets.append(sheet)

        sheets_to_process = [Sheet(s.width, s.height, s in covered_sheets and 0 or 1) for s in self.sheets]
        placement, _ = maxrects_bssf(self.rectangle, sheets_to_process, unlimited_bins=True)

        bins = all_selected_patterns + placement
        sheets_per_patterns = { }
        sheets_idx = { (s.width, s.height):i for i,s in enumerate(self.sheets) }

        for j, bin in enumerate(bins):
            for cut in bin.cuts:
                i = sheets_idx[cut.width, cut.height] if not cut.rotated else sheets_idx[cut.height, cut.width]
                try:
                    sheets_per_patterns[j,i] += 1
                except KeyError:
                    sheets_per_patterns[j,i] = 1

        fitness, prints_per_pattern = solve_LP(bins, sheets_per_patterns, self.sheets)
        off_spring = Solution(bins, sheets_per_patterns, prints_per_pattern, fitness)
        return self.hill_climbing(off_spring)

    def mutation(self, population):
        parent = population[randint(0, len(population)-1)]
        offspring = self.random_walk(parent)
        offspring = self.hill_climbing(offspring)
        return offspring


    def hill_climbing(self, solution):
        current_solution = solution

        while True:
            best_neighbor = current_solution
            for _ in range(self.hill_climbing_neighbors):
                new_neighbor = self.choose_neighbor(current_solution)
                if new_neighbor != None and new_neighbor.fitness < best_neighbor.fitness:
                    best_neighbor = new_neighbor

            if best_neighbor.fitness < current_solution.fitness:
                current_solution = best_neighbor
            else:
                break

        return current_solution

    def genetic_algorithm(self):
        # self.trace = open("trace.txt", "w")
        current_generation = self.create_initial_population()
        # print(f"Generation #0-----------------------------------------------------")
        # self.trace.write(f"Initial Generation:\n{self.print_population(current_generation)}")
        best_known = self.update_best_solution(current_generation)
        # self.trace.write(f"Best known solution: {best_known}")

        for k in range(self.no_generations):

            intermediate_generation = self.roulette_wheel_rank_based_selection(current_generation)
            current_generation = self.bests_solution_reproduction(current_generation)
            for i in range(len(current_generation), self.pop_size):
                if random.random() < self.prob_crossover:
                    current_generation.append(self.crossover(intermediate_generation))
                else:
                    current_generation.append(self.mutation(intermediate_generation))

            best_known = self.update_best_solution(current_generation)
            # print(f"Generation #{k+1}-----------------------------------------------------")
            #self.trace.write(f"Generation #{k+1}:\n{self.print_population(current_generation)}")
            #self.trace.write(f"Best known solution:\n{best_known}\n")
            #self.trace.write("----------------------------------------------------------------------------------------------\n\n")

        best_known = self.hill_climbing(best_known)
        self.clean_solution(best_known)
        return best_known

    def clean_solution(self, solution):
        updated_prints_per_pattern = {}
        counter = 0
        updated_bins = []
        for i, bin in enumerate(solution.bins):
            if solution.prints_per_pattern[f'x{i}'] != 0:
                updated_prints_per_pattern[f'x{counter}'] = solution.prints_per_pattern[f'x{i}']
                updated_bins.append(bin)
                counter += 1
        solution.bins = updated_bins
        solution.prints_per_pattern = updated_prints_per_pattern

    def print_population(self, population):
        result = ''
        for idx, solution in enumerate(population):
            result += f'Solution #{idx + 1}:\n{solution}\n\n'
        return result
