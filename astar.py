import os
import numpy as np
import xlsxwriter
import pandas as pd

gamma = 0.2
start = (2, 0)
real_cost = 0.04


class Node:
    def __init__(self, pos, Util):
        self.pos = pos
        self.cameFrom = None
        self.H = -Util
        self.G = float("inf")

"""Find the neighbors of a node"""
def neighbors(node):
    x, y = node.pos
    neighbs = np.array([node])
    if x - 1 >= 0 and not checkIfWallOrNegTerm([x - 1, y]):
        if neighbs[0] == node:
            neighbs[0] = gridNodes[x - 1, y]
        else:
            neighbs = np.append(neighbs, gridNodes[x - 1, y])

    if y - 1 >= 0 and not checkIfWallOrNegTerm([x, y - 1]):
        if neighbs[0] == node:
            neighbs[0] = gridNodes[x, y - 1]
        else:
            neighbs = np.append(neighbs, gridNodes[x, y - 1])

    if x + 1 <= numRows - 1 and not checkIfWallOrNegTerm([x + 1, y]):
        if neighbs[0] == node:
            neighbs[0] = gridNodes[x + 1, y]
        else:
            neighbs = np.append(neighbs, gridNodes[x + 1, y])

    if y + 1 <= numCols - 1 and not checkIfWallOrNegTerm([x, y + 1]):

        if neighbs[0] == node:
            neighbs[0] = gridNodes[x + 1, y]
        else:
            neighbs = np.append(neighbs, gridNodes[x, y + 1])

    return neighbs



"""Check if the given position is wall or negative terminal node"""
def checkIfWallOrNegTerm(pos):
    check = False
    for itemmm in wall:
        if pos[0] == itemmm[0] and pos[1] == itemmm[1]:
            check = True
    if not check:
        for itemm in negTerm:
            if pos[0] == itemm[0] and pos[1] == itemm[1]:
                check = True
    return check



"""A* algorithm"""
def aStar(StartNode, goalNode):

    openset = set()
    closedset = set()

    current = StartNode

    current.G = 0

    openset.add(current)


    numIters = 0

    while openset:

        numIters += 1

        current = min(openset, key=lambda c: c.G + c.H)
        print(current.pos)
        if current == goalNode:

            path = []
            while current.cameFrom:
                path.append(current)
                current = current.cameFrom
            path.append(current)
            return path[::-1], numIters

        openset.remove(current)


        for node in neighbors(current):

            newG = current.G + real_cost

            if node.G > newG:
                node.G = newG
                node.cameFrom = current
                if node not in openset:
                    openset.add(node)


    print("No path was found!")




"""This is the start. Read utilities from .xlsx file"""
data = pd.read_excel(os.path.dirname(os.path.abspath(__file__)) + r'\utilities\gamma=' + str(gamma) + '.xlsx')

util = np.zeros((data.shape[0] - 1, data.shape[1] - 1), dtype=float)
wall = np.array([[-2, -2]])
posTerm = np.array([[-2, -2]])
negTerm = np.array([[-2, -2]])
gridNodes = np.full((data.shape[0] - 1, data.shape[1] - 1), None)
numRows = data.shape[0] - 1
numCols = data.shape[1] - 1
for row in range(data.shape[0] - 1):
    for col in range(data.shape[1]):
        if col > 0:
            util[row, col - 1] = float(data.iat[row, col])
            if np.isnan(util[row, col - 1]):
                if wall[0, 0] == -2:

                    wall[0] = [row, col - 1]

                else:
                    wall = np.append(wall, [[row, col - 1]], axis=0)


            elif util[row, col - 1] == 1:
                if posTerm[0, 0] == -2:
                    posTerm[0] = [row, col - 1]
                    gridNodes[row, col - 1] = Node([row, col - 1], util[row, col - 1])

                else:
                    posTerm = np.append(posTerm, [[row, col - 1]], axis=0)
                    gridNodes[row, col - 1] = Node([row, col - 1], util[row, col - 1])

            elif util[row, col - 1] == -1:
                if negTerm[0, 0] == -2:
                    negTerm[0] = [row, col - 1]

                else:
                    negTerm = np.append(negTerm, [[row, col - 1]], axis=0)

            else:
                gridNodes[row, col - 1] = Node([row, col - 1], util[row, col - 1])



"""Run A* algorithm"""
pathToGoal, numIterations = aStar(gridNodes[start], gridNodes[posTerm[0, 0], posTerm[0, 1]])


"""If goal_node was found then print results."""
if pathToGoal:

    matrixOfPath = np.full((numRows, numCols), "*")
    for item in wall:
        matrixOfPath[item[0], item[1]] = "w"

    for item in posTerm:
        matrixOfPath[item[0], item[1]] = "+"

    for item in negTerm:
        matrixOfPath[item[0], item[1]] = "-"

    matrixOfPath[start] = "s"

    i = 1
    for nod in pathToGoal:
        row, col = nod.pos

        if (not ((nod.pos[0], nod.pos[1]) == start)) and (not ((nod.pos[0], nod.pos[1]) == (posTerm[0, 0], posTerm[0, 1]))):
            row, col = nod.pos
            matrixOfPath[row, col] = str(i)
            i += 1

    print(matrixOfPath)

    workbook = xlsxwriter.Workbook('paths_From_A_star/gamma=' + str(gamma) + '.xlsx')
    worksheet = workbook.add_worksheet()

    for rows in range(numRows + 1):
        for cols in range(numCols + 1):

            if rows == 0:
                if cols > 0:
                    worksheet.write(rows, cols, cols-1)
            elif cols == 0:
                worksheet.write(rows, cols, rows - 1)
            else:
                worksheet.write(rows, cols, matrixOfPath[rows - 1, cols - 1])

    worksheet.write(numRows + 1, 0, 'Number of iterations=')
    worksheet.write(numRows + 1, 1, numIterations)
    workbook.close()


