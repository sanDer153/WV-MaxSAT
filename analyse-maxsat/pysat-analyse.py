import random
import time
import statistics
import numpy as np
import matplotlib.pyplot as plt
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


# def draw_results(results):
#     # for order, result in results.items():
#     #     print(result)
#     #     plt.plot(result[0], result[1])
#     # plt.show()
#     densities = []
#     orders = [0]
#     R = []
#     for order, result in results.items():
#         densities = result[0]
#         orders.append(order)
#     results[0] = [densities.copy(), [0]*len(densities)]
#     for order in orders:
#         R.append(results[order][1])
#         # R[order] = dict()
#         # for idx in range(len(result[0])):
#         #     R[order][result[0][idx]] = result[1][idx]

#     X = np.array(densities)
#     Y = np.array(orders)
#     X, Y = np.meshgrid(X, Y)
#     Z = np.array(R)
#     Z = np.log(Z)

#     fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#     ax.plot_surface(X, Y, Z)
#     ax.set_xlabel("Dichtheid")
#     ax.set_ylabel("Orde")
#     ax.set_zlabel("Recursieve oproepen")
#     plt.show()


def results3d():
    step = 3
    max_order = 25
    max_density = 15
    densities = [i/step for i in range(0, 3*max_density + 1)]
    data = {"order": [], "density": [], "time": []}
    for order in range(step, max_order, step):
        for density in densities:
            clauses = round(density * order)
            results = []
            for _ in range(50):
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
    df.to_csv("3d-graph-results.csv", sep=',', index=False, encoding='utf-8')

    # draw_results(results)


def results2d():
    # (density, max_order, step)
    test_scenarios = [(0.9, 1000, 25), (2, 500, 10),
                      (3, 500, 10), (3.4, 500, 10), (3.5, 500, 10), (3.6, 400, 10), (3.7, 350, 10), (3.8, 300, 10), (4.26, 170, 10), (5, 100, 10)]
    for (density, max_order, step) in test_scenarios:
        data = {"order": [], "time": []}
        for order in range(step, max_order, step):
            clauses = round(density * order)
            results = []
            for _ in range(25):
                with RC2(generate_problem(order, clauses)) as rc2:
                    begin = time.perf_counter_ns()
                    rc2.compute()
                    end = time.perf_counter_ns()
                results.append(end-begin)
            data["order"].append(order)
            data["time"].append(statistics.median(results))

        df = pd.DataFrame(data)
        df.to_csv(f"2d-graph-results-{density}.csv",
                  sep=',', index=False, encoding='utf-8')
        print(f"density {density} done.")


# results3d()
results2d()
