import numpy as np
import xlsxwriter

"""Transition model"""
p_right = 0.1
p_left = 0.1
p_straigth = 0.8

transition_model = np.array([p_straigth, p_right, p_left])

"""Determination of values for gamma, epsilon, R(s) for non-terminal s"""
gamma = 0.9
epsilon = 0.0001
Rs = -0.04

"""Dimensions of environment"""
numRows = 3
numCols = 4

"""Position of the wall and of terminal states"""
wall = np.array([[1, 1]])

pos_term_states = np.array([[0, 3]])
neg_term_states = np.array([[1, 3]])

"""Possible actions"""
actions = np.array([["up", "down", "left", "right"]])

"""Creation of reward array"""
R = np.full((numRows, numCols), Rs)

"""Positive exit has reward +1 and negative exit -1"""
for item in pos_term_states:
    R[item[0], item[1]] = 1.0
for item in neg_term_states:
    R[item[0], item[1]] = -1.0
for item in wall:
    R[item[0], item[1]] = np.NaN

"""Determination of terminal states in a boolean array"""
terminalState = np.zeros((numRows, numCols), np.bool)
for item in pos_term_states:
    terminalState[item[0], item[1]] = True
for item in neg_term_states:
    terminalState[item[0], item[1]] = True

"""Initialize utilities"""
Util = R


"""Creation of an array with non-terminal states"""
notTerminalOrWall = np.array([[-1, -1]], dtype=int)

for i in range(numRows):
    for j in range(numCols):
        ifWall = np.array([i, j])

        if terminalState[i, j] == False and (wall == ifWall).all(1).any() == False:
            if notTerminalOrWall[0, 0] == -1:
                notTerminalOrWall[0, 0] = i
                notTerminalOrWall[0, 1] = j

            else:
                notTerminalOrWall = np.append(notTerminalOrWall, [[i, j]], axis=0)




"""Possible next states in relation with the current state and chosen action"""
def possible_next_states(action, row, col):
    row_nxt_st_str = -1
    col_nxt_st_str = -1
    row_nxt_st_right = -1
    col_nxt_st_right = -1
    row_nxt_st_left = -1
    col_nxt_st_left = -1

    if action == "up":
        row_nxt_st_str = row - 1
        col_nxt_st_str = col

        if row_nxt_st_str < 0 or isWall(row_nxt_st_str, col_nxt_st_str):
            row_nxt_st_str = row

        row_nxt_st_right = row
        col_nxt_st_right = col + 1

        if col_nxt_st_right > numCols - 1 or isWall(row_nxt_st_right, col_nxt_st_right):
            col_nxt_st_right = col

        row_nxt_st_left = row
        col_nxt_st_left = col - 1

        if col_nxt_st_left < 0 or isWall(row_nxt_st_left, col_nxt_st_left):
            col_nxt_st_left = col

    elif action == "down":

        row_nxt_st_str = row + 1
        col_nxt_st_str = col

        if row_nxt_st_str > numRows - 1 or isWall(row_nxt_st_str, col_nxt_st_str):
            row_nxt_st_str = row

        row_nxt_st_right = row
        col_nxt_st_right = col - 1

        if col_nxt_st_right < 0 or isWall(row_nxt_st_right, col_nxt_st_right):
            col_nxt_st_right = col

        row_nxt_st_left = row
        col_nxt_st_left = col + 1

        if col_nxt_st_left > numCols - 1 or isWall(row_nxt_st_left, col_nxt_st_left):
            col_nxt_st_left = col

    elif action == "right":

        row_nxt_st_str = row
        col_nxt_st_str = col + 1

        if col_nxt_st_str > numCols - 1 or isWall(row_nxt_st_str, col_nxt_st_str):
            col_nxt_st_str = col

        row_nxt_st_right = row + 1
        col_nxt_st_right = col

        if row_nxt_st_right > numRows - 1 or isWall(row_nxt_st_right, col_nxt_st_right):
            row_nxt_st_right = row

        row_nxt_st_left = row - 1
        col_nxt_st_left = col

        if row_nxt_st_left < 0 or isWall(row_nxt_st_left, col_nxt_st_left):
            row_nxt_st_left = row

    elif action == "left":

        row_nxt_st_str = row
        col_nxt_st_str = col - 1

        if col_nxt_st_str < 0 or isWall(row_nxt_st_str, col_nxt_st_str):
            col_nxt_st_str = col

        row_nxt_st_right = row - 1
        col_nxt_st_right = col

        if row_nxt_st_right < 0 or isWall(row_nxt_st_right, col_nxt_st_right):
            row_nxt_st_right = row

        row_nxt_st_left = row + 1
        col_nxt_st_left = col

        if row_nxt_st_left > numRows - 1 or isWall(row_nxt_st_left, col_nxt_st_left):
            row_nxt_st_left = row


    str_dir = np.array([row_nxt_st_str, col_nxt_st_str])
    right_dir = np.array([row_nxt_st_right, col_nxt_st_right])
    left_dir = np.array([row_nxt_st_left, col_nxt_st_left])

    return str_dir, right_dir, left_dir



def isWall(row, col):
    bool_if_wall = False
    for items in wall:
        r = items[0]
        c = items[1]
        if r == row and c == col:
            bool_if_wall = True
    return bool_if_wall



"""Iteration value algorithm"""
numIter = 0
Util_new = Util.copy()
delta = 0
cond = True

while cond:

    Util = Util_new.copy()
    delta = 0

    for notTermOrWallStates in notTerminalOrWall:
        summary = np.zeros(4, np.float)

        for act, i in zip(np.nditer(actions), range(4)):
            pos_next_st = np.array(possible_next_states(act, notTermOrWallStates[0], notTermOrWallStates[1]))


            for possib_nxt_st, j in zip(pos_next_st, range(3)):
                summary[i] += Util[possib_nxt_st[0], possib_nxt_st[1]] * transition_model[j]


        """Update utility values"""
        Util_new[notTermOrWallStates[0], notTermOrWallStates[1]] = R[notTermOrWallStates[0], notTermOrWallStates[1]] + (gamma * np.max(summary))
        """R[notTermOrWallStates[0], notTermOrWallStates[1]]"""

        """Compute delta"""
        if abs(Util_new[notTermOrWallStates[0], notTermOrWallStates[1]] - Util[notTermOrWallStates[0], notTermOrWallStates[1]]) > delta:
            delta = abs(Util_new[notTermOrWallStates[0], notTermOrWallStates[1]] - Util[notTermOrWallStates[0], notTermOrWallStates[1]])

    numIter += 1


    """Check if algorithm has to stop according to the below condition:"""
    if delta < (epsilon * (1 - gamma)) / gamma:
        cond = False


print(Util)


"""Print results in a .xlsx file"""
workbook = xlsxwriter.Workbook('utilities/gamma='+str(gamma)+'.xlsx')
worksheet = workbook.add_worksheet()

for rows in range(numRows+1):
    for cols in range(numCols+1):

        if rows == 0:
            if cols > 0:
                worksheet.write(rows, cols, cols-1)
        elif cols == 0:
            worksheet.write(rows, cols, rows-1)
        else:
            worksheet.write(rows, cols, str(round(Util[rows-1, cols-1], 2)))

worksheet.write(numRows+1, 0, 'Number of iterations=')
worksheet.write(numRows+1, 1, numIter+1)
workbook.close()