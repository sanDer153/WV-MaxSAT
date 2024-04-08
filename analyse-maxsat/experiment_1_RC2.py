import random
import time
import statistics
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import pandas as pd


def generate_problem(n_vars, n_clauses):
    variables = list(range(1, n_vars+1))
    wcnf = WCNF()
    for _ in range(n_clauses):
        clause = list(
            map(lambda x: x * random.choice([-1, 1]), random.sample(variables, k=3)))
        wcnf.append(clause, weight=1)
    return wcnf


def experiment1():
    # testvalues: (3, 25, 15) -> +- 15 min.
    step, max_order, max_density = (3, 30, 15)
    densities = [i/step for i in range(0, step*max_density + 1)]
    data = {"order": [], "density": [], "time": []}
    for order in range(step, max_order, step):
        for density in densities:
            clauses = round(density * order)
            results = []
            for _ in range(75):
                with RC2(generate_problem(order, clauses)) as rc2:
                    begin = time.perf_counter_ns()
                    rc2.compute()
                    end = time.perf_counter_ns()
                results.append(end-begin)
            data["order"].append(order)
            data["density"].append(density)
            data["time"].append(statistics.median(results))
        print(f"order: {order} done.")

    df = pd.DataFrame(data)
    df.to_csv("results/3d-graph-results.csv",
              sep=',', index=False, encoding='utf-8')


if __name__ == "__main__":
    experiment1()
