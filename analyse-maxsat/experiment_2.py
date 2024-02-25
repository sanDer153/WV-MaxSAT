import random
import time
import statistics
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import pandas as pd
from itertools import repeat
from multiprocessing import Pool


def generate_problem(n_vars, n_clauses, seed):
    random.seed(seed)
    variables = list(range(1, n_vars+1))
    wcnf = WCNF()
    for _ in range(n_clauses):
        clause = list(
            map(lambda x: x * random.choice([-1, 1]), random.sample(variables, k=3)))
        wcnf.append(clause, weight=1)
    return wcnf


def getSolvingTime(order, clauses, seed):
    with RC2(generate_problem(order, clauses, seed)) as rc2:
        begin = time.perf_counter_ns()
        rc2.compute()
        end = time.perf_counter_ns()
        return end-begin


def experiment2():
    reps = 500
    # (density, max_order, step)
    test_scenarios = [(0.9, 1000, 25), (2, 500, 10), (3, 500, 10), (3.4, 500, 10), (3.5, 500, 10),
                      (3.6, 400, 10), (3.7, 350, 9), (3.8, 300, 7), (4.26, 170, 4), (5, 100, 2), (6, 50, 2)]
    # test_scenarios = [(5, 100, 2)]
    for (density, max_order, step) in test_scenarios:
        data = {"order": [], "time": []}
        for order in range(max(3, step), max_order+1, step):
            clauses = round(density * order)
            seeds = [random.randint(0, 1000000000) for _ in range(reps)]
            pool = Pool()
            results = pool.starmap(getSolvingTime, zip(
                repeat(order), repeat(clauses), seeds))
            pool.close()
            pool.join()
            data["order"].append(order)
            data["time"].append(statistics.median(results))

        df = pd.DataFrame(data)
        df.to_csv(f"results/2d-graph-results-{density}.csv",
                  sep=',', index=False, encoding='utf-8')
        print(f"density {density} done.")


if __name__ == "__main__":
    experiment2()
