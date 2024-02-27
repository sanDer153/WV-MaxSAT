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


def experiment2():
    # (density, max_order, step)
    test_scenarios = [(3.6, 400, 10), (3.7, 350, 9), (3.8, 300, 7)]
    for (density, max_order, step) in test_scenarios:
        data = {"order": [], "time": []}
        for order in range(max(3, step), max_order+1, step):
            clauses = round(density * order)
            results = []
            for _ in range(300):
                with RC2(generate_problem(order, clauses)) as rc2:
                    begin = time.perf_counter_ns()
                    rc2.compute()
                    end = time.perf_counter_ns()
                results.append(end-begin)
            data["order"].append(order)
            data["time"].append(statistics.median(results))

        df = pd.DataFrame(data)
        df.to_csv(f"results/2d-graph-results-{density}.csv",
                  sep=',', index=False, encoding='utf-8')
        print(f"density {density} done.")


if __name__ == "__main__":
    experiment2()
