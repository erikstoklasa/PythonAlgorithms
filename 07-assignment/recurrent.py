from typing import Dict, Union

n: int = int(input())
x: float = float(input())

outputDict: Dict[int, float] = {
    0: -1,
}


def computeVal(x: float, n: int) -> float:
    global outputDict
    existingResult: Union[float, None] = outputDict.get(n)
    if existingResult:
        return existingResult
    if n == 1:
        return x
    if n == 2:
        # can insert since already checked for existance
        outputDict[2] = -(x + 1) / 3
        return outputDict[2]
    computedVal = (
        n / x * computeVal(x, n - 1)
        + pow(-1, n) * (n + 1) / (n - 1) * computeVal(x, n - 2)
        + (n - 1) / (2 * x) * computeVal(x, n - 3)
    )
    outputDict[n] = computedVal
    return computedVal


print(computeVal(x, n))
