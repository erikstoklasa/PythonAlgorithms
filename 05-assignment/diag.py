import sys

# f = open("/home/eriks/Documents/ALPY/05-assignment/diag.txt", "r")
f = open(sys.argv[1], "r")
arr = []
streak = 0
colIndexResult = 0
rowIndexResult = 0
for l in f:
    arr += [list(map(int, l.split()))]
f.close()
# for i in arr:
#     for y in i:
#         print(f"{int(y):>2}", end=" ")
#     print()


def isEvenInDiag(row, col, rtl=True):
    global arr
    global streak
    global colIndexResult
    global rowIndexResult
    localStreak = 0
    localColIndexCandidate = 0
    localRowIndexCandidate = 0
    condition = False
    if rtl:
        condition = len(arr) > row and len(arr[row]) > col
    else:
        condition = row >= 0 and col >= 0
    while condition:
        currVal = arr[row][col]
        if currVal % 2 == 0:
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
        # if there are more rows and columns, continue
        if rtl:
            row += 1
            col += 1
            condition = len(arr) > row and len(arr[row]) > col
        else:
            row += 1
            col -= 1
            condition = len(arr) > row and col >= 0


for i in range(len(arr[0])):
    for y in range(len(arr)):
        isEvenInDiag(y, i)
for i in range(len(arr[0]) - 1, -1, -1):
    for y in range(len(arr)):
        isEvenInDiag(y, i, rtl=False)

print(rowIndexResult, colIndexResult, streak)
