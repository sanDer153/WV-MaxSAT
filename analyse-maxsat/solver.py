# formula = [(1, 4, 6), (3, 6, 2), ...]
# assignment = (None, None, True, False, False, True, ...)
# global_state = {"alpha": inf}
PRUNE = (None, None)


def get_complement(literal):
    if literal % 2 == 0:
        return literal + 1
    else:
        return literal - 1


def assign_true(formula, assignment, literals):
    assignment = list(assignment)
    for literal in literals:
        new_formula = []
        complement = get_complement(literal)
        assignment[literal] = True
        assignment[complement] = False

        for clause in formula:
            if literal in clause:
                continue
            elif complement in clause:
                cl = list(clause)
                cl.remove(literal)
                cl = tuple(cl)
                new_formula.append(cl)
            else:
                new_formula.append(clause)
        formula = new_formula
    assignment = tuple(assignment)
    return formula, assignment


def reduce_formula(current_formula, current_assignment, n_false_clauses, global_state):
    present_literals = set(
        [lit for clause in current_formula for lit in clause])
    new_formula = []
    for clause in current_formula:
        if clause == ():
            n_false_clauses += 1
        else:
            new_formula.append(clause)
    current_formula = new_formula

    # UP1: pure literal rule
    pure_literals = [lit for lit in present_literals if get_complement(
        lit) not in present_literals]
    if len(pure_literals) > 0:
        current_formula, current_assignment = assign_true(
            current_formula, current_assignment, pure_literals)
        return reduce_formula(current_formula, current_assignment, n_false_clauses, global_state)

    unit_clauses = [clause for clause in current_formula if len(clause) == 1]
    p_1 = [0] * len(current_assignment)
    for (lit) in unit_clauses:
        p_1[lit] += 1

    # UP2: upper bound rule
    constrained_literals = []
    for literal in present_literals:
        if p_1[literal] + n_false_clauses >= global_state["alpha"]:
            if p_1[get_complement(literal)] + n_false_clauses >= global_state["alpha"]:
                return PRUNE
            else:
                constrained_literals.append(literal)
    if len(constrained_literals) > 0:
        current_formula, current_assignment = assign_true(
            current_formula, current_assignment, constrained_literals)
        return reduce_formula(current_formula, current_assignment, n_false_clauses, global_state)

    p_i = [0] * len(current_assignment)
    for clause in current_formula:
        for lit in clause:
            p_i[lit] += 1

    # UP3: dominating unit-clause rule
    constrained_literals = set()
    for literal in present_literals:
        if p_1[literal] > p_i[get_complement(literal)]:
            constrained_literals.add(literal)
        elif p_1[literal] >= p_i[get_complement(literal)] and p_1[get_complement(literal)] >= p_i[literal]:
            constrained_literals.add(literal-(literal % 2))
    if len(constrained_literals) > 0:
        current_formula, current_assignment = assign_true(
            current_formula, current_assignment, constrained_literals)
        return reduce_formula(current_formula, current_assignment, n_false_clauses, global_state)

    return current_formula, current_assignment, n_false_clauses


def solve(current_formula, current_assignment, n_false_clauses, global_state):
    result = reduce_formula(current_formula, current_assignment,
                            n_false_clauses, global_state)
    if result == PRUNE:
        return PRUNE

    current_formula, current_assignment, n_false_clauses = result


print(solve([(1, 0, 2), (4, 5, 2), (0, 1, 4)],
      (None, None, None, None, None, None), 0, {"alpha": 3}))
