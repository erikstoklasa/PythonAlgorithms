from typing import List
import copy
import sys

BoardType = List[List[str]]


def pm(m: List) -> None:
    for l in m:
        print(l)


def getNextTurnUser(m: BoardType) -> str:
    crossCount = 0
    circleCount = 0
    for r in m:
        for cell in r:
            if cell == "o":
                circleCount += 1
            elif cell == "x":
                crossCount += 1
    # print(circleCount, crossCount)
    if circleCount == crossCount:
        return "o"
    if crossCount + 1 == circleCount:
        return "x"
    else:
        return f"circle:{circleCount},cross:{crossCount}"
        # TODO: replace by empty string, then check if string is not empty


streak = 0
colIndexResult = 0
rowIndexResult = 0


def computeWinnerStreaks(board, row, col, mode=[1, 1]):
    # mode = offset
    global streak
    global colIndexResult
    global rowIndexResult
    localStreak = 0
    localColIndexCandidate = 0
    localRowIndexCandidate = 0
    condition = len(board) > row and 0 <= row and len(board[row]) > col and col >= 0
    lastVal = None
    while condition:
        currVal = board[row][col]
        if (lastVal == None and (currVal == "x" or currVal == "o")) or (
            currVal == lastVal and (currVal == "x" or currVal == "o")
        ):
            localStreak += 1
            if localStreak > streak:
                streak = localStreak
                colIndexResult = localColIndexCandidate
                rowIndexResult = localRowIndexCandidate
            if localStreak == 1:
                localColIndexCandidate = col
                localRowIndexCandidate = row
        else:
            break
        lastVal = currVal
        # if there are more rows and columns, continue
        # if mode == [1, 1]:
        #     row += mode[0]
        #     col += mode[1]
        #     # condition = len(board) > row and len(board[row]) > col
        # else:
        row += mode[0]
        col += mode[1]
        # condition = len(board) > row and col >= 0
        # condition = len(board) > row and len(board[row]) > col
        condition = len(board) > row and 0 <= row and len(board[row]) > col and col >= 0


def getWinner(m: BoardType) -> str:
    def getNumOfCellsNeededForWin(m: BoardType) -> int:
        # numOfRows: int = len(m)
        # numOfCols: int = len(m[0])
        return 5
        # return min(numOfCols, numOfRows)

    def getWinnerHelper(m: BoardType) -> str:
        for ri in range(len(m)):
            for ci in range(len(m[ri])):
                computeWinnerStreaks(m, ri, ci, mode=[1, 1])
                computeWinnerStreaks(m, ri, ci, mode=[-1, 1])
                computeWinnerStreaks(m, ri, ci, mode=[0, 1])
                computeWinnerStreaks(m, ri, ci, mode=[1, 0])
        if streak >= neededForWin:
            return m[rowIndexResult][colIndexResult]
        else:
            return ""

    neededForWin: int = getNumOfCellsNeededForWin(m)
    usr: str = getWinnerHelper(m)
    if usr:
        return usr
    else:
        return ""


f = open(sys.argv[1], "r")
board: BoardType = [l.split() for l in f]


def mainChecking():
    usrToCheck = getNextTurnUser(board)
    for ri in range(len(board)):
        for ci in range(len(board[ri])):
            localBoard: BoardType = copy.deepcopy(board)
            if board[ri][ci] == ".":
                localBoard[ri][ci] = usrToCheck
                usr = getWinner(localBoard)
                if usr:
                    print(ri, ci)
                    return


mainChecking()
