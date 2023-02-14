from typing import List

BoardType = List[List[str]]

DIRECTIONS: List[List[int]] = [
    # y,x coords
    [0, -1],  # left
    [-1, 0],  # top
    [0, 1],  # right
    [1, 0],  # bottom
]


def loadBoard(filename: str):
    b = []
    f = open(filename, "r")
    for line in f:
        cells: List[str | None] = list(line.split())
        for i in range(len(cells)):
            if "none" == cells[i]:
                cells[i] = None
        b.append(cells)
    f.close()
    return b


def isInsideBoard(x: int, y: int, board: BoardType) -> tuple[bool, int | None]:
    # 0 = left
    # 1 = top
    # 2 = right
    # 3 = bottom
    if len(board) <= y:
        return (False, 3)
    if y < 0:
        return (False, 1)
    if len(board[y]) <= x:
        return (False, 2)
    if x < 0:
        return (False, 0)
    return (True, None)


def canTravel(cell: str, comingFromDirection: int, nextDirection: int) -> bool:
    if cell[comingFromDirection] == cell[nextDirection]:
        return True
    else:
        return False


def getOppositeDirection(direction: int) -> int:
    return (direction + 2) % 4


def getOpenRoad(cell: str, comingFromDirection: int) -> int:
    for i in range(len(cell)):
        if cell[comingFromDirection] == cell[i] and comingFromDirection != i:
            return i
    return 0


def computePaths(filename):
    board: BoardType = loadBoard(filename)

    def getDistanceLeftToRight(roadType: str):
        # -1 means no way was found
        max_distance = -1
        for y in range(len(board)):
            # travelling only for specified roads
            currCell = board[y][0]
            if currCell and roadType != currCell[0]:
                continue
            distance = travel(
                x=0, y=y, distance=0, comingFromDirection=0, goalDirection=2
            )
            if max_distance < distance:
                max_distance = distance
        return max_distance

    def getDistanceTopToBottom(roadType: str):
        # -1 means no way was found
        max_distance = -1
        if len(board) == 0:
            raise Exception("Board is empty")
        for x in range(len(board[0])):
            # travelling only for specified roads
            currCell = board[0][x]
            if currCell and roadType != currCell[1]:
                continue
            distance = travel(
                x=x, y=0, distance=0, comingFromDirection=1, goalDirection=3
            )
            if max_distance < distance:
                max_distance = distance
        return max_distance

    def travel(
        x: int, y: int, distance: int, comingFromDirection: int, goalDirection: int
    ) -> int:
        isInsideBoardBool, direction = isInsideBoard(x, y, board)
        if isInsideBoardBool:
            currentCell = board[y][x]
            if currentCell == None:
                return -1
            nextDirection = getOpenRoad(currentCell, comingFromDirection)
            if canTravel(
                currentCell,
                comingFromDirection,
                nextDirection,
            ):
                yOffset, xOffset = DIRECTIONS[nextDirection]
                return travel(
                    x + xOffset,
                    y + yOffset,
                    distance + 1,
                    getOppositeDirection(nextDirection),
                    goalDirection,
                )
        else:
            if direction == goalDirection:
                # we found the way
                return distance
            else:
                # there is no way
                return -1

    return (
        getDistanceLeftToRight("l"),
        getDistanceLeftToRight("d"),
        getDistanceTopToBottom("l"),
        getDistanceTopToBottom("d"),
    )


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    # filename = "input.txt"
    b = loadBoard(filename)

    for n in computePaths(filename):
        print(n, end=" ")
    print()
