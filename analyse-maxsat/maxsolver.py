import random
import statistics
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import time
# Problem: [[0, 3, 1], [6, 2, 8], ...] 2x is een variabele en 2x+1 is het complement
# literals: L = [True, False, False, True, ...] de assignment van 2x is L[x] en voor 2x+1 is het not(L[x])
recursive_calls = 0


def generate_problem(n_vars, n_clauses):
    variables = list(range(n_vars))
    formula = []
    for _ in range(n_clauses):
        clause = list(map(lambda x: 2 * x +
                          random.choice([0, 1]), random.sample(variables, k=3)))
        formula.append(clause)
    return formula


def get_complement(literal):
    if literal % 2 == 0:
        return literal + 1
    else:
        return literal - 1


def solve(formula, assignment, false_clauses, global_search_state):
    global recursive_calls
    recursive_calls += 1

    if len(formula) == 0:
        global_search_state["alpha"] = min(
            global_search_state["alpha"], false_clauses)
        return assignment

    new_formula = []
    for clause in formula:
        if len(clause) == 0:
            false_clauses += 1
        else:
            new_formula.append(clause.copy())
    formula = new_formula

    if false_clauses > global_search_state["alpha"]:
        return None

    present_literals = set([l for clause in formula for l in clause])
    pure_literals = [lit for lit in present_literals if get_complement(
        lit) not in present_literals]
    for pure_literal in pure_literals:
        formula = assign_true(formula, assignment, pure_literal)

    present_literals = list(set([l for clause in formula for l in clause]))
    if len(present_literals) == 0:
        return solve(formula, assignment, false_clauses, global_search_state)
    literal = random.choice(present_literals)
    assignment_1 = assignment.copy()
    assignment_2 = assignment.copy()
    formula_1 = assign_true(formula, assignment_1, literal)
    formula_2 = assign_true(formula, assignment_2, get_complement(literal))
    optimal_model_1 = solve(formula_1, assignment_1,
                            false_clauses, global_search_state)
    optimal_model_2 = solve(formula_2, assignment_2,
                            false_clauses, global_search_state)
    return optimal_model_2 if optimal_model_2 is not None else optimal_model_1


def assign_true(formula, assignment, lit):
    comp = get_complement(lit)
    assignment[lit] = True
    assignment[comp] = False
    new_formula = []
    for c in formula:
        if lit in c:
            continue
        else:
            clause = c.copy()
            if comp in clause:
                clause.remove(comp)
            new_formula.append(clause)
    return new_formula


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
    # formula = generate_problem(4, 20)
    # print(formula, solve(
    #     formula, [None, None, None, None, None, None, None, None], 0, {"alpha": 20}))

    for order in [5, 10, 15, 20]:
        densities = []
        calls = []
        clauses = 0
        while clauses/order <= max_density:
            r = []
            for _ in range(50):
                global recursive_calls
                recursive_calls = 0
                # begin = time.time()
                solve(generate_problem(order, clauses), [
                      None]*order*2, 0, {"alpha": clauses})
                # end = time.time()
                # r.append(end-begin)
                r.append(recursive_calls)
            densities.append(clauses/order)
            calls.append(statistics.median(r))
            clauses += round(0.2*order)
        results[order] = [densities, calls]
        print(f"order: {order} done.")

    draw_results(results)


main()
