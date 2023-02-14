# numberInputArr = list(map(int, input().split()))
numberInput = input()
goal: int = int(input())
result = ""


def removeZeroes(string):
    out = ""
    for s in string.split(" "):
        if not s.lstrip("0"):
            out += "0"
        else:
            out += s.lstrip("0")
    return out


def getCombinationString(seq: str, curr: str, rest: str):
    global goal
    global result
    if not rest:
        if eval(removeZeroes(seq + " + " + curr)) == goal:
            result = seq + " + " + curr
            return
        elif eval(removeZeroes(seq + " * " + curr)) == goal:
            result = seq + " * " + curr
            return
        elif eval(removeZeroes(seq + "" + curr)) == goal:
            result = seq + "" + curr
            return
        else:
            return
    if result:
        return
    if eval(removeZeroes(seq)) != goal and len(rest) == 0:
        return None
    if eval(removeZeroes(seq)) > goal and not ("0" in rest or curr == "0"):
        return None
    getCombinationString(seq + " + " + curr, rest[0], rest[1:])
    getCombinationString(seq + " * " + curr, rest[0], rest[1:])
    getCombinationString(seq + "" + curr, rest[0], rest[1:])


getCombinationString(numberInput[0], numberInput[1], numberInput[2:])
if result:
    print(result.replace(" ", ""))
else:
    print("NO_SOLUTION")
