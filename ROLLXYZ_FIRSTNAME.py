#!/usr/bin/env python3
from Agent import *  # See the Agent.py file
from copy import deepcopy


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

# Representation follows DIMACS format without trailing zero

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

    blocks = []
    if "Up" in available:
        blocks.append([x, y+1])

    if "Right" in available:
        blocks.append([x+1, y])

    if "Down" in available:
        blocks.append([x, y-1])

    if "Left" in available:
        blocks.append([x-1, y])

    return blocks


def test():
    ag = Agent()
    clauses = deepcopy(initial_clauses)
    ag.TakeAction("Up")
    ag.TakeAction("Up")
    ag.TakeAction("Up")
    ag.TakeAction("Right")
    ag.TakeAction("Right")
    ag.TakeAction("Down")

    currLoc = ag.FindCurrentLocation()
    while(currLoc != [4, 4]):
        blocks = check_available_blocks(currLoc)

        # Percieve and add to KB
        percept = ag.PerceiveCurrentLocation()
        print(percept)
        if percept[0] == True:  # Pit in adjacent location
            clause = ""
            for block in blocks:
                mystr = f"P{block[0]}{block[1]} "
                clause += mystr
            print(clause)
            clauses.append(clause)
        if percept[1] == True:  # Wumpus in adjacent location
            clause = ""
            for block in blocks:
                mystr = f"W{block[0]}{block[1]} "
                clause += mystr
            print(clause)
            clauses.append(clause)

        # Move to block in blocks if safe (check if !P(block) and !W(block), after added to clauses is unsatisfiable)
        #                                 (if satisfiable, add to kb that block is unsafe)
        currLoc = [4, 4]


def main():
    ag = Agent()
    print('curLoc', ag.FindCurrentLocation())
    print('Percept [breeze, stench] :', ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept', ag.PerceiveCurrentLocation())
    ag.TakeAction('Up')
    print(ag.FindCurrentLocation())
    print('Percept', ag.PerceiveCurrentLocation())


if __name__ == '__main__':
    test()
