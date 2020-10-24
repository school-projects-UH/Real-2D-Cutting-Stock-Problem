import math
import random
from classes import *
from bin_pack import maxrects_bssf
from lp_solver import solve_LP
from random import randint

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
    def __init__(self, rectangle, sheets, pop_size=10, random_walk_steps=30, hill_climbing_neighbors=10):
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

    def roulette_wheel_selection(self):
        pass

    def bests_solution_reproduction(self):
        pass

    def crossover(self, Population):
        def select_patterns(parent):
            patterns = [(bin.free_space, j, bin) for j, bin in enumerate(parent.bins)]
            patterns.sort()

            # select a number between the [25%, 50%] of the patterns (patterns_len must be >= 4 since 0.25 * 4 = 1)
            count_to_select = len(patterns) >= 4 and \
                                random.randint(0.25 * len(patterns), 0.5 * len(patterns)) or \
                                random.randint(0, len(patterns) - 1)
            
            return [(j, bin) for _, j, bin in patterns[:count_to_select]]
        
        P = list(Population)
        parent1 = P[random.randint(0, len(P)-1)]
        P.remove(parent1)
        parent2 = P[random.randint(0, len(P)-1)]

        set_patterns1 = select_patterns(parent1)
        set_patterns2 = select_patterns(parent2)

        all_selected_patterns = list(set([bin for _,bin in set_patterns1 + set_patterns2]))
        covered_sheets = set([sheet for sheet in bin.cuts for _,bin in all_selected_patterns])
        not_covered_sheets = [Sheet(s.width, s.height, 1) for s in self.sheets if sheet not in coverd_sheets]
        
        placement, p = maxrects_bssf(self.rectangle, not_covered_sheets)
        
        bins = all_selected_patterns + placement
        
        updated_p, j_offset = {}, len(all_selected_patterns)
        for sheet_idx, sheet in enumerate(self.sheets):
            if sheet in covered_sheets: continue
            for (j, i), count in p.items():
                if sheet == not_covered_sheets[i]:
                    updated_p[j+j_offset, sheet_idx] = count

        patterns1_bins = set([bin for _,bin in set_patterns1])
        patterns_idxs = set([j for j,_ in set_patterns1] + [j for j,bin in set_patterns2 if bin not in patterns1_bins])
        
        sheets_per_patterns1 = { (j, i) : count for (j, i), count in parent1.sheets_per_pattern if j in patterns_idxs}
        sheets_per_patterns2 = { (j, i) : count for (j, i), count in parent2.sheets_per_pattern if j in patterns_idxs}
        sheets_per_patterns = { **sheets_per_patterns1, **sheets_per_patterns2, **updated_p }

        off_spring = Solution(bins, sheets_per_patterns)

        # Call Hillclimb

    def mutation(self, population):
        parent = population[randint(0, len(population)-1)]
        print(f"Parent solution:\n{parent}")
        offspring = self.random_walk(parent)
        offspring = self.hill_climbing(offspring, self.hill_climbing_neighbors)
        print(f"Offspring:\n{offspring}")
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
