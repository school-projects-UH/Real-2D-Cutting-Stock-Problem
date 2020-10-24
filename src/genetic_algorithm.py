import math
import random
from classes import *

class Solver():
    def __init__(self,sheets,demands,  width ,height):
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
            
        if sheets_per_pattern[pattern,sheet] < 0:
            return None

        return sheets_per_pattern

    '''Moves one sheet from a pattern to another one'''
    def move(self, solution):
        pattern_source = random.randint(0,len(solution.bins)-1)
        pattern_destiny = random.randint(0,len(solution.bins)-1)
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

