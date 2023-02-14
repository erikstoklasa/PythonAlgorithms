from typing import Dict, List, Tuple
import sys
import copy

BoardType = List[List[int]]
f = open(sys.argv[1], "r")
#f = open("skate1.txt", "r")
m: BoardType = []
for line in f.readlines():
    m.append(list(map(int, line.split())))


class State:
    def __init__(self, maze: BoardType, y: int, x: int):
        self.y: int = y
        self.x: int = x
        self.maze: BoardType = maze

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self,a):
        return self.x==a.x and self.y==a.y

    movements = [
        [0, -1, "S"],  # up
        [1, 0, "V"],  # right
        [0, 1, "J"],  # bottom
        [-1, 0, "Z"],  # left
    ]

    @staticmethod
    def isInsideBoard(maze, x, y) -> bool:
        return x >= 0 and x < len(maze[0]) and y >= 0 and y < len(maze)

    def goalReached(self) -> bool:
        return self.maze[self.y][self.x] == 4

    def nextStateList(self):
        output: List[State] = []
        for xCh, yCh, _ in self.movements:
            x, y = self.skate((xCh, yCh))
            output.append(State(self.maze, y, x))
        return output

    def skate(self, movement: Tuple[int, int]) -> Tuple[int, int]:
        xCh, yCh = movement
        x = self.x
        y = self.y
        x += xCh
        y += yCh
        while State.isInsideBoard(self.maze, x, y) and self.maze[y][x] in [
            0,
            4,
            2,
        ]:
            x += xCh
            y += yCh
        else:
            # reverting last unsuccesful movement
            x -= xCh
            y -= yCh
        return x, y

    def __str__(self) -> str:
        temp: BoardType = copy.deepcopy(self.maze)
        temp[self.y][self.x] = 9
        coords = f"X:{self.x} Y:{self.y}"
        boardToPrint = ""
        for r in temp:
            boardToPrint += f"{r}\n"
        return coords + "\n" + boardToPrint


def findStart(matrix: BoardType) -> Tuple[int, int]:
    for ri in range(len(matrix)):
        for ci in range(len(matrix[ri])):
            if matrix[ri][ci] == 2:
                return ci, ri
    return 0, 0


def findPath(state: State, visited: Dict[State, State]):
    path = []
    while state is not None:
        path.append(state)
        state = visited[state]
    return list(reversed(path))


def solve(mazeState: State, maxdepth=100):
    visited: Dict[State, State] = {}
    waiting = []
    waiting.append((mazeState, None, 0))
    while len(waiting) != 0:
        state, prev, level = waiting.pop(0)
        if state not in visited:
            visited[state] = prev
            if state.goalReached():
                return findPath(state, visited)
            if level < maxdepth:
                for s in state.nextStateList():
                    waiting.append((s, state, level + 1))
    return None

def getDiff(state:State, newState:State) -> str:
    for xCh,yCh,letter in state.movements:
        x,y = state.skate((xCh,yCh))
        if x == newState.x and y == newState.y:
            return letter

    return ""

x, y = findStart(m)
state = State(m, y, x)
arr = solve(state)
if arr is None:
    print("NOTHING FOUND")
else:
    actionsMade = ""
    for si in range(len(arr)-1):
        actionsMade+=getDiff(arr[si],arr[si+1])
    print(actionsMade)