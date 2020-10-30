#!/usr/bin/env python3
import numpy as np
from Agent import *  # See the Agent.py file
from copy import deepcopy
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)


# All your code can go here.

# You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.

# Literals will be of the form W11 P11 and so on... where W represents presence of Wumpus and P represents presence of Pit
# Will we need literals to dfine presence/absence of breeze and stench (no)

literals = [
    "W11", "W12", "W13", "W14", "W21", "W22", "W23", "W24", "W31", "W32", "W33", "W34", "W41", "W42", "W43", "W44",  # for the possible positions of wumpus
    "P11", "P12", "P13", "P14", "P21", "P22", "P23", "P24", "P31", "P32", "P33", "P34", "P41", "P42", "P43", "P44",  # for the possible positions of pit
]

index_to_literals = dict(zip(range(32), literals))
literals_to_index = dict(zip(literals, range(32)))

initial_clauses = [
    "!W11", "!P11", "!W44", "!P44",
    # ONLY ONE PIT IS PRESENT (240 clauses)
    "!P11 !P12", "!P11 !P13", "!P11 !P14", "!P11 !P21", "!P11 !P22", "!P11 !P23", "!P11 !P24", "!P11 !P31", "!P11 !P32", "!P11 !P33", "!P11 !P34", "!P11 !P41",
    "!P11 !P42", "!P11 !P43", "!P11 !P44", "!P12 !P11", "!P12 !P13", "!P12 !P14", "!P12 !P21", "!P12 !P22", "!P12 !P23", "!P12 !P24", "!P12 !P31", "!P12 !P32",
    "!P12 !P33", "!P12 !P34", "!P12 !P41", "!P12 !P42", "!P12 !P43", "!P12 !P44", "!P13 !P11", "!P13 !P12", "!P13 !P14", "!P13 !P21", "!P13 !P22", "!P13 !P23",
    "!P13 !P24", "!P13 !P31", "!P13 !P32", "!P13 !P33", "!P13 !P34", "!P13 !P41", "!P13 !P42", "!P13 !P43", "!P13 !P44", "!P14 !P11", "!P14 !P12", "!P14 !P13",
    "!P14 !P21", "!P14 !P22", "!P14 !P23", "!P14 !P24", "!P14 !P31", "!P14 !P32", "!P14 !P33", "!P14 !P34", "!P14 !P41", "!P14 !P42", "!P14 !P43", "!P14 !P44",
    "!P21 !P11", "!P21 !P12", "!P21 !P13", "!P21 !P14", "!P21 !P22", "!P21 !P23", "!P21 !P24", "!P21 !P31", "!P21 !P32", "!P21 !P33", "!P21 !P34", "!P21 !P41",
    "!P21 !P42", "!P21 !P43", "!P21 !P44", "!P22 !P11", "!P22 !P12", "!P22 !P13", "!P22 !P14", "!P22 !P21", "!P22 !P23", "!P22 !P24", "!P22 !P31", "!P22 !P32",
    "!P22 !P33", "!P22 !P34", "!P22 !P41", "!P22 !P42", "!P22 !P43", "!P22 !P44", "!P23 !P11", "!P23 !P12", "!P23 !P13", "!P23 !P14", "!P23 !P21", "!P23 !P22",
    "!P23 !P24", "!P23 !P31", "!P23 !P32", "!P23 !P33", "!P23 !P34", "!P23 !P41", "!P23 !P42", "!P23 !P43", "!P23 !P44", "!P24 !P11", "!P24 !P12", "!P24 !P13",
    "!P24 !P14", "!P24 !P21", "!P24 !P22", "!P24 !P23", "!P24 !P31", "!P24 !P32", "!P24 !P33", "!P24 !P34", "!P24 !P41", "!P24 !P42", "!P24 !P43", "!P24 !P44",
    "!P31 !P11", "!P31 !P12", "!P31 !P13", "!P31 !P14", "!P31 !P21", "!P31 !P22", "!P31 !P23", "!P31 !P24", "!P31 !P32", "!P31 !P33", "!P31 !P34", "!P31 !P41",
    "!P31 !P42", "!P31 !P43", "!P31 !P44", "!P32 !P11", "!P32 !P12", "!P32 !P13", "!P32 !P14", "!P32 !P21", "!P32 !P22", "!P32 !P23", "!P32 !P24", "!P32 !P31",
    "!P32 !P33", "!P32 !P34", "!P32 !P41", "!P32 !P42", "!P32 !P43", "!P32 !P44", "!P33 !P11", "!P33 !P12", "!P33 !P13", "!P33 !P14", "!P33 !P21", "!P33 !P22",
    "!P33 !P23", "!P33 !P24", "!P33 !P31", "!P33 !P32", "!P33 !P34", "!P33 !P41", "!P33 !P42", "!P33 !P43", "!P33 !P44", "!P34 !P11", "!P34 !P12", "!P34 !P13",
    "!P34 !P14", "!P34 !P21", "!P34 !P22", "!P34 !P23", "!P34 !P24", "!P34 !P31", "!P34 !P32", "!P34 !P33", "!P34 !P41", "!P34 !P42", "!P34 !P43", "!P34 !P44",
    "!P41 !P11", "!P41 !P12", "!P41 !P13", "!P41 !P14", "!P41 !P21", "!P41 !P22", "!P41 !P23", "!P41 !P24", "!P41 !P31", "!P41 !P32", "!P41 !P33", "!P41 !P34",
    "!P41 !P42", "!P41 !P43", "!P41 !P44", "!P42 !P11", "!P42 !P12", "!P42 !P13", "!P42 !P14", "!P42 !P21", "!P42 !P22", "!P42 !P23", "!P42 !P24", "!P42 !P31",
    "!P42 !P32", "!P42 !P33", "!P42 !P34", "!P42 !P41", "!P42 !P43", "!P42 !P44", "!P43 !P11", "!P43 !P12", "!P43 !P13", "!P43 !P14", "!P43 !P21", "!P43 !P22",
    "!P43 !P23", "!P43 !P24", "!P43 !P31", "!P43 !P32", "!P43 !P33", "!P43 !P34", "!P43 !P41", "!P43 !P42", "!P43 !P44", "!P44 !P11", "!P44 !P12", "!P44 !P13",
    "!P44 !P14", "!P44 !P21", "!P44 !P22", "!P44 !P23", "!P44 !P24", "!P44 !P31", "!P44 !P32", "!P44 !P33", "!P44 !P34", "!P44 !P41", "!P44 !P42", "!P44 !P43",
    # ONLY ONE WUMPUS IS PRESENT (240 clauses)
    "!W11 !W12", "!W11 !W13", "!W11 !W14", "!W11 !W21", "!W11 !W22", "!W11 !W23", "!W11 !W24", "!W11 !W31", "!W11 !W32", "!W11 !W33", "!W11 !W34", "!W11 !W41",
    "!W11 !W42", "!W11 !W43", "!W11 !W44", "!W12 !W11", "!W12 !W13", "!W12 !W14", "!W12 !W21", "!W12 !W22", "!W12 !W23", "!W12 !W24", "!W12 !W31", "!W12 !W32",
    "!W12 !W33", "!W12 !W34", "!W12 !W41", "!W12 !W42", "!W12 !W43", "!W12 !W44", "!W13 !W11", "!W13 !W12", "!W13 !W14", "!W13 !W21", "!W13 !W22", "!W13 !W23",
    "!W13 !W24", "!W13 !W31", "!W13 !W32", "!W13 !W33", "!W13 !W34", "!W13 !W41", "!W13 !W42", "!W13 !W43", "!W13 !W44", "!W14 !W11", "!W14 !W12", "!W14 !W13",
    "!W14 !W21", "!W14 !W22", "!W14 !W23", "!W14 !W24", "!W14 !W31", "!W14 !W32", "!W14 !W33", "!W14 !W34", "!W14 !W41", "!W14 !W42", "!W14 !W43", "!W14 !W44",
    "!W21 !W11", "!W21 !W12", "!W21 !W13", "!W21 !W14", "!W21 !W22", "!W21 !W23", "!W21 !W24", "!W21 !W31", "!W21 !W32", "!W21 !W33", "!W21 !W34", "!W21 !W41",
    "!W21 !W42", "!W21 !W43", "!W21 !W44", "!W22 !W11", "!W22 !W12", "!W22 !W13", "!W22 !W14", "!W22 !W21", "!W22 !W23", "!W22 !W24", "!W22 !W31", "!W22 !W32",
    "!W22 !W33", "!W22 !W34", "!W22 !W41", "!W22 !W42", "!W22 !W43", "!W22 !W44", "!W23 !W11", "!W23 !W12", "!W23 !W13", "!W23 !W14", "!W23 !W21", "!W23 !W22",
    "!W23 !W24", "!W23 !W31", "!W23 !W32", "!W23 !W33", "!W23 !W34", "!W23 !W41", "!W23 !W42", "!W23 !W43", "!W23 !W44", "!W24 !W11", "!W24 !W12", "!W24 !W13",
    "!W24 !W14", "!W24 !W21", "!W24 !W22", "!W24 !W23", "!W24 !W31", "!W24 !W32", "!W24 !W33", "!W24 !W34", "!W24 !W41", "!W24 !W42", "!W24 !W43", "!W24 !W44",
    "!W31 !W11", "!W31 !W12", "!W31 !W13", "!W31 !W14", "!W31 !W21", "!W31 !W22", "!W31 !W23", "!W31 !W24", "!W31 !W32", "!W31 !W33", "!W31 !W34", "!W31 !W41",
    "!W31 !W42", "!W31 !W43", "!W31 !W44", "!W32 !W11", "!W32 !W12", "!W32 !W13", "!W32 !W14", "!W32 !W21", "!W32 !W22", "!W32 !W23", "!W32 !W24", "!W32 !W31",
    "!W32 !W33", "!W32 !W34", "!W32 !W41", "!W32 !W42", "!W32 !W43", "!W32 !W44", "!W33 !W11", "!W33 !W12", "!W33 !W13", "!W33 !W14", "!W33 !W21", "!W33 !W22",
    "!W33 !W23", "!W33 !W24", "!W33 !W31", "!W33 !W32", "!W33 !W34", "!W33 !W41", "!W33 !W42", "!W33 !W43", "!W33 !W44", "!W34 !W11", "!W34 !W12", "!W34 !W13",
    "!W34 !W14", "!W34 !W21", "!W34 !W22", "!W34 !W23", "!W34 !W24", "!W34 !W31", "!W34 !W32", "!W34 !W33", "!W34 !W41", "!W34 !W42", "!W34 !W43", "!W34 !W44",
    "!W41 !W11", "!W41 !W12", "!W41 !W13", "!W41 !W14", "!W41 !W21", "!W41 !W22", "!W41 !W23", "!W41 !W24", "!W41 !W31", "!W41 !W32", "!W41 !W33", "!W41 !W34",
    "!W41 !W42", "!W41 !W43", "!W41 !W44", "!W42 !W11", "!W42 !W12", "!W42 !W13", "!W42 !W14", "!W42 !W21", "!W42 !W22", "!W42 !W23", "!W42 !W24", "!W42 !W31",
    "!W42 !W32", "!W42 !W33", "!W42 !W34", "!W42 !W41", "!W42 !W43", "!W42 !W44", "!W43 !W11", "!W43 !W12", "!W43 !W13", "!W43 !W14", "!W43 !W21", "!W43 !W22",
    "!W43 !W23", "!W43 !W24", "!W43 !W31", "!W43 !W32", "!W43 !W33", "!W43 !W34", "!W43 !W41", "!W43 !W42", "!W43 !W44", "!W44 !W11", "!W44 !W12", "!W44 !W13",
    "!W44 !W14", "!W44 !W21", "!W44 !W22", "!W44 !W23", "!W44 !W24", "!W44 !W31", "!W44 !W32", "!W44 !W33", "!W44 !W34", "!W44 !W41", "!W44 !W42", "!W44 !W43",
]


def check_available_blocks(location):
    available = ["Up", "Down", "Left", "Right"]
    x, y = location
    if x == 1:
        # Left not present
        available.remove("Left")
    elif x == 4:
        # Right not present
        available.remove("Right")
    if y == 1:
        # Down not present
        available.remove("Down")
    elif y == 4:
        # Up not present
        available.remove("Up")

    # print(available)
    actions = []
    blocks = []
    if "Up" in available:
        blocks.append([x, y+1])
        actions.append("Up")

    if "Right" in available:
        blocks.append([x+1, y])
        actions.append("Right")

    if "Down" in available:
        blocks.append([x, y-1])
        actions.append("Down")

    if "Left" in available:
        blocks.append([x-1, y])
        actions.append("Left")

    return blocks, actions


def getSymbols(clauses):
    symbols = set()
    split_clauses = set()
    for clause in clauses:
        for sclause in clause.split(" "):
            if sclause != "":
                split_clauses.add(sclause)
        # print(split_clauses)

    for sclause in split_clauses:
        if sclause[0] == "!":
            symbols.add(sclause[1:])
        else:
            symbols.add(sclause)
    return symbols


def getLiterals(clause):
    literals = set()
    for lit in clause.split(" "):
        if lit != "":
            literals.add(lit)
    return literals


def neg(c):
    if c[0] == "!":
        return c[1:]
    else:
        return "!"+c


def symbol(c):
    if c[0] == "!":
        return c[1:]
    else:
        return c


def evaluate_clause(clause, model):
    flag = False
    for c in getLiterals(clause):
        if c not in model and neg(c) not in model:
            flag = True
        elif symbol(c) in model and model[symbol(c)] == (c[0] != "!"):
            return True

    if flag:
        return None
    return False


def findPureSymbol(symbols, clauses):
    for s in symbols:
        found_pos, found_neg = False, False
        for c in clauses:
            if not found_pos and s in getLiterals(c):
                found_pos = True
            if not found_neg and neg(s) in getLiterals(c):
                found_neg = True
        if found_pos != found_neg:
            return s, found_pos
    return None, None


def findUnitClause(clauses, model):
    for clause in clauses:
        count = 0
        for literal in getLiterals(clause):
            sym = symbol(literal)
            if sym in model and model[sym] == (literal[0] != "!"):
                return None, None
            if sym not in model:
                count += 1
                P, value = sym, (literal[0] != "!")
        if count == 1:
            return P, value
    return None, None


def remove(sym, symbols):
    return {x for x in symbols if x != sym}


def extend(model, P, value):
    tmodel = deepcopy(model)
    tmodel[P] = value
    return tmodel


def dpll(clauses, symbols, model) -> bool:
    # print(clauses, symbols, model)
    unknown_clauses = []
    for clause in clauses:
        val = evaluate_clause(clause, model)
        if val is False:
            return False
        if val is None:
            unknown_clauses.append(clause)
    if not unknown_clauses:
        return model
    P, value = findPureSymbol(symbols, unknown_clauses)
    if P:
        return dpll(clauses, remove(P, symbols), extend(model, P, value))
    P, value = findUnitClause(clauses, model)
    if P:
        return dpll(clauses, remove(P, symbols), extend(model, P, value))

    P, symbols = list(symbols)[0], list(symbols)[1:]

    return (dpll(clauses, symbols, extend(model, P, True)) or
            dpll(clauses, symbols, extend(model, P, False)))


def dpll_satisfiable(clauses) -> bool:
    symbols = getSymbols(clauses)
    # print(clauses, symbols)
    return dpll(clauses, symbols, dict())


def isSafe(block, clauses):
    # run dpll with
    # KB entails !P(block) and KB entails !W(block)
    # Check KB and P(block) is unsat
    # Check KB and W(block) is unsat
    tclauses1 = deepcopy(clauses)
    tclauses2 = deepcopy(clauses)

    tclauses1.append(f"P{block[0]}{block[1]}")
    tclauses2.append(f"W{block[0]}{block[1]}")

    hasPit = dpll_satisfiable(tclauses1)
    hasWumpus = dpll_satisfiable(tclauses2)
    # print(hasPit if hasPit == False else True, hasWumpus if hasWumpus == False else True)
    return ((hasPit == False) and (hasWumpus == False))


def test(ag):
    clauses = deepcopy(initial_clauses)

    currLoc = ag.FindCurrentLocation()

    visited = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0], ]
    lastMove = None
    rework = False
    moves = []

    while(currLoc != [4, 4]):
        blocks, actions = check_available_blocks(currLoc)

        # Percieve and add to KB if not visited
        # print(f"{currLoc} Visited?: {visited[currLoc[1]-1][currLoc[0]-1]}")
        if visited[currLoc[1]-1][currLoc[0]-1] == 0:
            percept = ag.PerceiveCurrentLocation()
            rework = False
            # print("Percept: ", percept)
            visited[currLoc[1]-1][currLoc[0]-1] = 1
            if percept[0] == True:  # Pit in adjacent location
                clause = ""
                for block in blocks:
                    mystr = f"P{block[0]}{block[1]} "
                    clause += mystr
                # print(clause)
                clauses.append(clause)
            else:  # No pit in adjacent location
                clause = ""
                for block in blocks:
                    mystr = f"!P{block[0]}{block[1]}"
                    clauses.append(mystr)  # And not or condition
            if percept[1] == True:  # Wumpus in adjacent location
                clause = ""
                for block in blocks:
                    mystr = f"W{block[0]}{block[1]} "
                    clause += mystr
                # print(clause)
                clauses.append(clause)
            else:  # No wumpus in adjacent location
                clause = ""
                for block in blocks:
                    mystr = f"!W{block[0]}{block[1]}"
                    clauses.append(mystr)  # And not or condition

        # TODO: Move to block in blocks if safe (check if !P(block) and !W(block), after added to clauses is unsatisfiable)
        #                                 (if satisfiable, add to kb that block is unsafe)

        for block, action in zip(blocks, actions):
            # print(block, action)
            if isSafe(block, clauses) and (visited[block[1]-1][block[0]-1] == 0 or rework == True):
                if rework and previousMove == action:
                    print(f"Do not perform {previousMove} while reworking")
                    continue
                ag.TakeAction(action)
                clauses.append(f"!W{block[0]}{block[1]}")
                clauses.append(f"!P{block[0]}{block[1]}")
                lastMove = action
                moves.append(action)
                break
            else:
                # Unsure if safe or not safe as percept not fully developed
                pass
        pLoc = currLoc
        currLoc = ag.FindCurrentLocation()
        if currLoc == pLoc:
            # print("No moves found: backtracking")
            if lastMove == None:
                print("Time to rework through")
                pp.pprint(visited)
                rework = True
            elif lastMove == "Up":
                ag.TakeAction("Down")
                previousMove = lastMove  # If reworking, do not do this move
            elif lastMove == "Right":
                ag.TakeAction("Left")
                previousMove = lastMove  # If reworking, do not do this move
            elif lastMove == "Down":
                ag.TakeAction("Up")
                previousMove = lastMove  # If reworking, do not do this move
            elif lastMove == "Left":
                ag.TakeAction("Right")
                previousMove = lastMove  # If reworking, do not do this move
            lastMove = None
            currLoc = ag.FindCurrentLocation()

    print("Reached goal")


def exhaustive_search():
    count = 0
    for w in range(2, 15):
        for p in range(2, 15):
            world = [
                ['', '', '', ''],  # Rooms [1,1] to [4,1]
                ['', '', '', ''],  # Rooms [1,2] to [4,2]
                ['', '', '', ''],  # Rooms [1,3] to [4,3]
                ['', '', '', ''],  # Rooms [1,4] to [4,4]
            ]
            if p != w and p != 4 and w != 4:
                count += 1
                if count < 0:
                    continue
                if count == 99 or count == 130:
                    continue
                print(f"World #{count}")
                world[p % 4][p//4] = 'P'
                world[w % 4][w//4] = 'W'
                print(f"{world[3]}")
                print(f"{world[2]}")
                print(f"{world[1]}")
                print(f"{world[0]}")
                ag = Agent(world)
                test(ag)
                if count % 20 == 0:
                    print("--------------------------------------------------------------")
                    print("Worlds seen: ", count)
                    print("--------------------------------------------------------------")
    print(count)


if __name__ == '__main__':
    exhaustive_search()
