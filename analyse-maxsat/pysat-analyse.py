import random
import time
import statistics
import numpy as np
import matplotlib.pyplot as plt
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF


def generate_problem(n_vars, n_clauses):
    variables = list(range(1, n_vars+1))
    wcnf = WCNF()
    for _ in range(n_clauses):
        clause = list(
            map(lambda x: x * random.choice([-1, 1]), random.sample(variables, k=3)))
        wcnf.append(clause, weight=1)
    return wcnf


def draw_results(results):
    # for order, result in results.items():
    #     print(result)
    #     plt.plot(result[0], result[1])
    # plt.show()
    densities = []
    orders = [0]
    R = []
    for order, result in results.items():
        densities = result[0]
        orders.append(order)
    results[0] = [densities.copy(), [0]*len(densities)]
    for order in orders:
        R.append(results[order][1])
        # R[order] = dict()
        # for idx in range(len(result[0])):
        #     R[order][result[0][idx]] = result[1][idx]

    X = np.array(densities)
    Y = np.array(orders)
    X, Y = np.meshgrid(X, Y)
    Z = np.array(R)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(X, Y, Z)
    ax.set_xlabel("Dichtheid")
    ax.set_ylabel("Orde")
    ax.set_zlabel("Recursieve oproepen")
    plt.show()


def main():
    max_density = 7
    results = {}
    for order in [5, 10, 15, 20, 25, 30]:
        densities = []
        times = []
        clauses = 0
        while clauses/order <= max_density:
            r = []
            for _ in range(50):
                with RC2(generate_problem(order, clauses)) as rc2:
                    begin = time.time()
                    rc2.compute()
                    end = time.time()
                r.append(end-begin)
            densities.append(clauses/order)
            times.append(statistics.median(r))
            clauses += round(0.2*order)
        results[order] = [densities, times]
        print(f"order: {order} done.")

    draw_results(results)


main()
