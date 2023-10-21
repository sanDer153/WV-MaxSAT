import random
import statistics
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
    unit_prop_possible = True
    while unit_prop_possible:
        unit_prop_possible = False
        for clause in formula:
            if (len(clause) == 1):
                unit_prop_possible = True
                formula = unit_propagation(formula, clause[0])
                break

    # pure literal elimination
    literal_elim_possible = True
    while literal_elim_possible:
        literal_elim_possible = False
        present_literals = set([l for clause in formula for l in clause])
        for literal in present_literals:
            if (get_complement(literal) not in present_literals):
                literal_elim_possible = True
                formula = pure_literal_elimination(formula, literal)
                break

    # stopping conditions
    if (len(formula) == 0):
        return True
    if any(len(clause) == 0 for clause in formula):
        return False

    literal = random.choice([l for clause in formula for l in clause])
    formula_1 = formula + [[literal]]
    formula_2 = formula + [[get_complement(literal)]]
    return DPLL(formula_1) or DPLL(formula_2)


def unit_propagation(formula, literal):
    complement = get_complement(literal)
    new_formula = []
    for clause in formula:
        if (literal in clause):
            continue
        elif (complement in clause):
            clause.remove(complement)
            new_formula.append(clause)
        else:
            new_formula.append(clause)
    return new_formula


def pure_literal_elimination(formula, literal):
    new_formula = []
    for clause in formula:
        if (literal not in clause):
            new_formula.append(clause)
    return new_formula


def draw_results(results):
    pass


def main():
    max_density = 10
    results = {}
    for order in [40]:
        densities = []
        calls = []
        clauses = 0
        while clauses/order <= max_density:
            r = []
            for _ in range(50):
                global calls_to_dpll
                calls_to_dpll = 0
                DPLL(generate_problem(order, clauses))
                r.append(calls_to_dpll)
            densities.append(clauses/order)
            calls.append(statistics.median(r))
            clauses += 10
        results[order] = [densities, calls]

    draw_results(results)


main()
