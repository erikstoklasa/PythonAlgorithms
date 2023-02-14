import sys
from typing import List, Tuple, Dict
import copy

BoardType = List[List[List[int]]]

#fileName = sys.argv[1]
fileName = "graf2.txt"
f = open(fileName, "rt")

firstLine = f.readline()
c, r, d = map(int, firstLine.split())
m: BoardType = [copy.copy([]) for di in range(d)]
allLines = f.readlines()

actions: List[List[int]] = [
        [0, -1, 0],  # up
        [0, 1, 0],  # down
        [0, 0, -1],  # left
        [0, 0, 1],  # right
        [-1, 0, 0],  # front
        [1, 0, 0],  # back
    ]


class State:
    def __init__(self, board: BoardType, d: int, r: int, c: int):
        self.board: BoardType = board
        self.d: int = d
        self.r: int = r
        self.c: int = c

    def getNextStates(self):
        nextStates: List[State] = []
        for dCh, rCh, cCh in actions:
            newD = self.d + dCh
            newR = self.r + rCh
            newC = self.c + cCh
            newState = State(self.board, newD, newR, newC)
            if State.isInsideBoard(self.board, newD, newR, newC):
                nextStates.append(newState)
        return nextStates

    @staticmethod
    def findStartingCoords(board: BoardType) -> Tuple[int, int, int]:
        for di in range(len(board)):
            for ri in range(len(board[di])):
                for ci in range(len(board[di][ri])):
                    if board[di][ri][ci] == 2:
                        return di, ri, ci
        return 0, 0, 0

    def __hash__(self) -> int:
        return hash((self.d, self.r, self.c))

    def __eq__(self, a):
        return self.d == a.d and self.r == a.r and self.c == a.c

    def __str__(self) -> str:
        return f"{self.d} {self.r} {self.c}"

    @staticmethod
    def isInsideBoard(board, d, r, c) -> bool:
        fitsInD: bool = d >= 0 and d < len(board)
        fitsInR: bool = r >= 0 and r < len(board[0])
        fitsInC: bool = c >= 0 and c < len(board[0][0])
        return fitsInC and fitsInD and fitsInR

    def goalReached(self) -> bool:
        return self.board[self.d][self.r][self.c] == 4


def print3dm(m: BoardType) -> None:
    for di in range(d):
        for ri in range(r):
            row: List[int] = m[di][ri]
            print(row)
        print(di, "-----")


def printStates(currentState: State, stateList: Dict[State, State]):
    output = []
    while currentState is not None:
        output.append(currentState)
        currentState = stateList[currentState]
    for s in reversed(output):
        print(s)


def findShortestPath(boardState: State, maxDepth: int = 100):
    visited = {}
    waiting = []
    waiting.append((boardState, None, 0))
    while len(waiting) != 0:
        state, prev, level = waiting.pop(0)
        if state not in visited:
            visited[state] = prev
            if state.goalReached():
                printStates(state, visited)
                return "FOUND"
            if level < maxDepth:
                for s in state.getNextStates():
                    waiting.append((s, state, level + 1))
    return None

for di in range(d):
    for ri in range(r):
        row: List[int] = list(map(int, allLines[di*d+ri].split()))
        m[di].append(copy.copy(row))

#print3dm(m)
d,r,c = State.findStartingCoords(m)
bs = State(m,d,r,c)
# for s in bs.getNextStates():
#     print(s)
if findShortestPath(bs) != "FOUND":
    print("NEEXISTUJE")