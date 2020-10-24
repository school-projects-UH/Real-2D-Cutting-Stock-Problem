import math
import random
from classes import *
from bin_pack import maxrects_bssf
from random import randint

def _pick_two_randoms(top):
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
    def __init__(self,sheets,demands, width ,height):
        self.total_sheets = len(sheets)
        self.rectangle = Rectangle(width ,height)
        self.sheets = []

        self.lb_patterns = math.ceil(sum([w * h for (w, h) in sheets]) / (width * height)) #lower bound of the number of patterns
        self.ub_sheet = {}  # the number of sheets i which can be placed on one pattern

        for i, sheet in enumerate(sheets):
            w, h = sheet
            self.sheets.append(Sheet(w, h, demands[i]))
            self.ub_sheet[i] = math.floor((width * height) / (w * h))


    def compute_amount_and_fitness(self):
        pass

    def random_walk(self):
        pass

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

        if sheets_per_pattern[pattern,sheet] < 0 or sum([sheets_per_pattern[_pattern, _sheet] for _pattern, _sheet in sheets_per_pattern if _pattern == pattern]) == 0:
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
        pattern_one = random.randint(0,len(solution.bins)-1)
        pattern_two = random.randint(0,len(solution.bins)-1)
        sheet_one = random.randint(0, self.total_sheets - 1)
        sheet_two = random.randint(0, self.total_sheets - 1)

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
        pass

    def create_initial_population(self):
        pass

    def update_best_solution(self):
        pass

    def roulette_wheel_selection(self):
        pass

    def bests_solution_reproduction(self):
        pass

    def crossover(self):
        pass

    def mutation(self):
        pass

    def hill_climbing(self):
        pass

    def delete_overproduction(self):
        pass

    def genetic_algorithm(self):
        pass


rectangle = Rectangle(15, 15)
sheets = [Sheet(10, 5, 1), Sheet(8, 5, 1), Sheet(8, 8, 1), Sheet(3, 15, 1)]
placement, sheets_per_pattern = maxrects_bssf(rectangle, sheets, unlimited_bins=True)
sheets = [(10, 5), (8, 5), (8, 8), (3, 15)]
demands = [1, 1, 1, 1]

GA = Solver(sheets, demands, 15, 15)

s1 = Solution(placement, sheets_per_pattern)

print(s1.sheets_per_pattern)
new_sheets_per_pattern = GA.move(s1)
print(new_sheets_per_pattern)
