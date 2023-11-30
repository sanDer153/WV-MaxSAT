import random
import statistics
import matplotlib.pyplot as plt
import time
# Problem: [[0, 3, 1], [6, 2, 8], ...] 2x is een variabele en 2x+1 is het complement
# literals: L = [True, False, False, True, ...] de assignment van 2x is L[x] en voor 2x+1 is het not(L[x])
calls_to_dpll = 0


def generate_problem(vars, clauses):
    literals = list(range(vars))
    formula = []
    for _ in range(clauses):
        clause = list(map(lambda x: 2 * x +
                          random.choice([0, 1]), random.sample(literals, k=3)))
        formula.append(clause)
    return formula


def get_complement(literal):
    if literal % 2 == 0:
        return literal + 1
    else:
        return literal - 1


def DPLL(formula):
    global calls_to_dpll
    calls_to_dpll += 1
    # unit_propagation
    unit_literals = set()
    for clause in formula:
        if (len(clause) == 1):
            unit_literals.add(clause[0])
    formula = unit_propagation(formula, unit_literals)

    # pure literal elimination
    literal_elim_possible = True
    while literal_elim_possible:
        literal_elim_possible = False
        present_literals = set([l for clause in formula for l in clause])
        pure_literals = set()
        for literal in present_literals:
            if (get_complement(literal) not in present_literals):
                literal_elim_possible = True
                pure_literals.add(literal)
        formula = pure_literal_elimination(formula, pure_literals)

    # stopping conditions
    if (len(formula) == 0):
        return True
    if any(len(clause) == 0 for clause in formula):
        return False

    present_literals = list(set([l for clause in formula for l in clause]))
    literal = random.choice(present_literals)
    formula_1 = assign_true(formula, literal)
    formula_2 = assign_true(formula, get_complement(literal))
    return DPLL(formula_1) or DPLL(formula_2)


def unit_propagation(formula, literals):
    while len(literals) != 0:
        literal = literals.pop()
        complement = get_complement(literal)
        new_formula = []
        for c in formula:
            if literal in c:
                continue
            else:
                clause = c.copy()
                if complement in clause:
                    clause.remove(complement)
                    if (len(clause) == 1):
                        literals.add(clause[0])
            new_formula.append(clause)
        formula = new_formula
    return formula


def pure_literal_elimination(formula, literals):
    new_formula = []
    for clause in formula:
        if (len(set(clause).intersection(literals)) == 0):
            new_formula.append(clause.copy())
    return new_formula


def DPLL2(formula):
    global calls_to_dpll
    calls_to_dpll += 1

    if len(formula) == 0:
        return True
    if any(len(clause) == 0 for clause in formula):
        return False

    unit_clauses = [u_clause for u_clause in formula if len(u_clause) == 1]
    if len(unit_clauses) > 0:
        new_formula = assign_true(formula, unit_clauses[0][0])
        return DPLL2(new_formula)

    present_literals = list(set([l for clause in formula for l in clause]))
    literal = random.choice(present_literals)
    formula_1 = assign_true(formula, literal)
    formula_2 = assign_true(formula, get_complement(literal))
    return DPLL2(formula_1) or DPLL2(formula_2)


def assign_true(formula, lit):
    comp = get_complement(lit)
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
    for order, result in results.items():
        plt.plot(result[0], result[1])
    plt.show()


def main():
    max_density = 15
    results = {}
    # print(DPLL2(generate_problem(40, 180)))
    for order in [20, 25, 30, 35, 40, 45, 50]:
        densities = []
        calls = []
        clauses = 0
        while clauses/order <= max_density:
            r = []
            for _ in range(100):
                global calls_to_dpll
                calls_to_dpll = 0
                # begin = time.time()
                DPLL2(generate_problem(order, clauses))
                # end = time.time()
                # r.append(end-begin)
                r.append(calls_to_dpll)
            densities.append(clauses/order)
            calls.append(statistics.median(r))
            clauses += 10
        results[order] = [densities, calls]
        print(f"order: {order} done.")

    draw_results(results)


main()
