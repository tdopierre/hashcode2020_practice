import os
import time
import numpy as np
from util import Solution, Evaluator
import random
import copy


def complete_solution(s: Solution, e: Evaluator):
    s_score = e.evaluate(s)
    slices_needed = np.abs(s_score)
    available_indices = [ind for ind in (set(range(e.n_pizzas)) - set(s.indices.tolist())) if e.sizes[ind] <= slices_needed]
    if not len(available_indices):
        return s, False

    # available_indices = sorted(available_indices, key=lambda x: e.sizes[x])
    random.shuffle(available_indices)
    available_sizes = [e.sizes[ind] for ind in available_indices]
    cumsum = np.cumsum(available_sizes)

    ix_to_add = np.where(cumsum <= slices_needed)[0][-1]
    to_add = available_indices[:ix_to_add + 1]
    new_solution = Solution(np.concatenate((s.indices, to_add)))
    return new_solution, True


def find_solutions(file_path, task_name, max_sec=5):
    begin = time.time()
    # Init evaluator
    evaluator = Evaluator(file_path)

    # Finind valid init solution
    solution = Solution(indices=np.array(range(evaluator.n_pizzas)))
    random.shuffle(solution.indices)
    solution_score = evaluator.evaluate(solution=solution)

    while solution_score == -np.inf:
        solution.indices = solution.indices[:len(solution.indices) // 2]
        solution_score = evaluator.evaluate(solution=solution)

    # Creating list with best solutions / scores
    best_solutions = [(copy.deepcopy(solution), solution_score)]
    solution, did_update = complete_solution(solution, evaluator)
    solution_score = evaluator.evaluate(solution)
    if did_update:
        best_solutions.append((copy.deepcopy(solution), solution_score))
    print(f"Best score {solution_score} using {len(solution.indices)} pizzas. {solution.indices[:15]}...")
    solution.output(f"submissions/{task_name}/{solution_score}.txt")
    it = 0
    while True:
        it += 1
        if time.time() - begin > max_sec:
            break
        np.random.shuffle(solution.indices)
        # print(f"Dropped: {solution.indices}")
        to_drop = min(np.random.choice([1, 1000]), len(solution.indices))
        # to_drop = 1

        tmp_solution = copy.deepcopy(solution)

        tmp_solution.indices = tmp_solution.indices[:-to_drop]
        tmp_solution, did_update = complete_solution(tmp_solution, evaluator)
        # time.sleep(1)
        # print(f"did_update {did_update}")
        if did_update:
            new_solution_score = evaluator.evaluate(tmp_solution)
            # print(f"new solution {tmp_solution.indices}")
            if new_solution_score > solution_score:
                solution = tmp_solution
                # print(f"new solution {tmp_solution.indices}")
                solution_score = new_solution_score
                best_solutions.append((copy.deepcopy(solution), solution_score))
                print(f"[it {it}] Best score: {solution_score} with {len(solution.indices)} pizzas.")
                solution.output(f"submissions/{task_name}/{solution_score}.txt")


def main():
    inputs_dir = "problem/inputs"
    for file in os.listdir(inputs_dir):
        for i in range(10):
            find_solutions(f"{inputs_dir}/{file}", file, max_sec=5)


if __name__ == "__main__":
    main()
