import os
import numpy as np
import typing


class BaseEvaluator:
    def __init__(self, **kwargs):
        """
        :param input_file: path to input file which is used to evaluate
        """
        pass

    def evaluate(self, solution):
        """
        function which evaluates a given solution
        :param solution:
        :return: score for solution
        """
        pass


class BaseSolution:
    def __init__(self, **kwargs):
        pass


class Solution(BaseSolution):
    def __init__(self, indices: np.ndarray):
        super(Solution, self).__init__()
        self.indices = indices

    def set_indices(self, indices: np.ndarray):
        self.indices = indices

    def output(self, file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "w") as file:
            file.write(str(len(self.indices)) + "\n")
            file.write(" ".join([str(ind) for ind in self.indices]))
            file.write("\n")


class Evaluator(BaseEvaluator):
    def __init__(self, input_file: str):
        super(Evaluator, self).__init__()
        with open(input_file, "r") as file:
            first_row = file.readline()
            max_slices, n_pizzas = first_row.strip().split()
            self.max_slices = int(max_slices)
            self.n_pizzas = int(n_pizzas)
            self.sizes = np.array([int(s) for s in file.readline().strip().split()])

    def evaluate(self, solution: Solution) -> int:
        # If multiple pizzas with same size in solution -> error
        if len(np.unique(np.array(solution.indices))) != len(solution.indices):
            return -np.inf
        # If pizzas in solution do not match evaluator pizzas -> error
        sum_solution = sum([self.sizes[ind] for ind in solution.indices])
        if sum_solution > self.max_slices:
            return -np.inf
        return sum_solution - self.max_slices
