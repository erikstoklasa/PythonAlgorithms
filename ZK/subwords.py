import sys
from typing import List

fileName = sys.argv[1]
f = open(fileName, "rt")
wordList: List[str] = []
for l in f:
    wordList.append(l.strip())


def findShortestWord(wordList: List[str]) -> str:
    return min(wordList, key=lambda x: len(x))


shortest: str = findShortestWord(wordList)
wordList.remove(shortest)
maxMatched: int = 0
maxString: str = ""
for l in range(1, len(shortest) + 1):
    countMatched: int = 0
    for i in range(len(shortest) - l + 1):
        substr: str = shortest[i : l + i]
        # print(substr,l,i)
        matchedForAllWords: bool = True
        for w in wordList:
            if substr not in w:
                matchedForAllWords = False
        countMatched = l
        if matchedForAllWords and countMatched > maxMatched:
            maxMatched = countMatched
            maxString = substr
if len(maxString) > 0:
    print(maxString)
else:
    print("NEEXISTUJE")
