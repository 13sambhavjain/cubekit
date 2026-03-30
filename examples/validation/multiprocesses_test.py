from multiprocessing import Pool, cpu_count
from functools import partial
import random
from cubekit.core import Cube3x3, w, Moves, g
from cubekit.solver3x3 import *
import random


def _run_batch(args):
    solver_class, func, check_func, scrambleLimit, random_start_face, batch_size = args
    fails = []
    passes = []
    for _ in range(batch_size):
        c = Cube3x3(start_faceId=random.choice(list(Cube3x3.faceIds)) if random_start_face else w)
        scram = c.apply_randomScramble(scrambleLimit, True)
        solver = solver_class(c, g, True)
        moves = func(solver)
        if not check_func(solver):
            fails.append(dict(scramble=scram, solution=moves))
        elif len(passes) < 10:
            passes.append(dict(scramble=scram, solution=moves))
    return fails, passes

def test(solver_class, func, check_func,
         numberOfCases=1000, scrambleLimit=10, breakAtFirstFail=False,
         getpasses=10, random_start_face=False,
         workers=None, chunksize=10000) -> dict:

    workers = workers or cpu_count()
    chunksize = min(chunksize, numberOfCases)
    
    # split into batches
    full_batches, remainder = divmod(numberOfCases, chunksize)
    batch_sizes = [chunksize] * full_batches + ([remainder] if remainder else [])
    batch_args = [
        (solver_class, func, check_func, scrambleLimit, random_start_face, size)
        for size in batch_sizes
    ]

    all_fails = []
    all_passes :list = []
    completed = 0

    with Pool(workers) as pool:
        for fails, passes in pool.imap_unordered(_run_batch, batch_args):
            all_fails.extend(fails)
            all_passes.extend(passes[:max(0, getpasses - len(all_passes))])
            completed += chunksize
            print(f"\r{min(completed, numberOfCases):,} / {numberOfCases:,} completed"
                  f"  |  fails: {len(all_fails)}", end='', flush=True)
            if breakAtFirstFail and all_fails:
                pool.terminate()
                break

    print()  # newline after progress
    return dict(fails=all_fails, passes=all_passes)

def test_solve_cube(*,numberOfCases: int=1000, scrambleLimit: int= 10, breakAtFirstFail: bool=False, getpasses: int = 10, random_start_face=False) -> dict[str,list[dict[str,Moves]]]:
    return test(Solver3x3, Solver3x3.solve_cube, FirstCorners.check_solved,
                numberOfCases, scrambleLimit, breakAtFirstFail, getpasses, random_start_face)
from cubekit.core import *


def printcases(cases):
    for case in cases:
        c = Cube3x3()
        c.apply_moves(case["scramble"])
        print(f"{case["scramble"]}, {case['scramble'].comment}")
        print(c)
        # if case["solution"]:
        c.apply_moves(case["solution"])
        print(f"{case["solution"]}, {case['solution'].comment=}")
        print(c)
        print("\n\n\n")

def check_print_result(result):
    if result['fails']:
        print("Fails = ")
        printcases(result["fails"])
        print("Failed")
        return
    else:
        print("Passes = ")
        printcases(result["passes"])
        print("Passed")


def main():
    result = test_solve_cube(scrambleLimit=30, numberOfCases=1000, breakAtFirstFail=True, random_start_face=True)
    check_print_result(result)
    # c = Cube3x3()
    # solver = LastLayer(c, w)
    # print(solver.apply_algo(FaceId.green, Algo.OLL.Edges.dot_shape))
    # print(solver.apply_algo(FaceId.red, Algo.OLL.Corners.Sune))
    # print(c)
    # print(moves:= solver.solve_OLL() + solver.solve_PLL())
    # print(moves.comment)
    # print(solver.check_solved())
    # print(c)

if __name__ == "__main__":
    main()