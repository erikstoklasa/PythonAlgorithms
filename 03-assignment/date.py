from typing import List, Any


helpers = ["the", "of"]

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

ordinals = [
    ["first", 1],
    ["second", 2],
    ["third", 3],
    ["fifth", 5],
    ["eighth", 8],
    ["ninth", 9],
    ["twelfth", 12],
    ["twentieth", 20],
    ["thirtieth", 30],
]

numbers = [
    ["one", 1],
    ["two", 2],
    ["three", 3],
    ["four", 4],
    ["five", 5],
    ["six", 6],
    ["seven", 7],
    ["eight", 8],
    ["nine", 9],
    ["ten", 10],
    ["eleven", 11],
    ["twelve", 12],
    ["thirteen", 13],
    ["fourteen", 14],
    ["fifteen", 15],
    ["sixteen", 16],
    ["seventeen", 17],
    ["eighteen", 18],
    ["nineteen", 19],
    ["twenty", 20],
    ["thirty", 30],
    ["forty", 40],
    ["fifty", 50],
    ["sixty", 60],
    ["seventy", 70],
    ["eighty", 80],
    ["ninety", 90],
    ["hundred", 100],
    ["thousand", 1000],
]


def numberToWord(num: int) -> str:
    # find the number in numbers, generate if not found
    if num == 0:
        return ""
    minDiff: int = num - numbers[0][1]
    indexOfMinDiff: int = 0
    for i in range(len(numbers)):
        curr: int = numbers[i][1]
        if curr == num:
            if num == 1000 or num == 100:
                return "one" + numbers[i][0]
            return numbers[i][0]
        localDiff: int = num - curr
        if localDiff <= minDiff and localDiff > 0:
            minDiff = localDiff
            indexOfMinDiff = i
    # not found, generate number
    # how many times does the num fit into the number found in array
    minDiffMultiplicator = num // numbers[indexOfMinDiff][1]
    if minDiffMultiplicator > 0 and numbers[indexOfMinDiff][1] >= 100:
        num -= minDiffMultiplicator * numbers[indexOfMinDiff][1]
        return (
            numberToWord(minDiffMultiplicator)
            + numbers[indexOfMinDiff][0]
            + numberToWord(num)
        )
    return numbers[indexOfMinDiff][0] + numberToWord(minDiff)


def ordinalToWord(num: int):
    for i in range(len(ordinals)):
        curr: int = ordinals[i][1]
        if num == curr:
            return ordinals[i][0]
    # not found in special ordinals
    # let's generate one from numbers arr
    minDiff: int = num - ordinals[0][1]
    indexOfMinDiff: int = 0
    for i in range(len(numbers)):
        localDiff: int = num - numbers[i][1]
        if localDiff < minDiff and localDiff > 0:
            minDiff = localDiff
            indexOfMinDiff = i
        if num == numbers[i][1] and localDiff == 0:
            return numbers[i][0] + "th"
    return f"{numbers[indexOfMinDiff][0]}-{ordinalToWord(minDiff)}"


def monthNumToWord(dayNum: int):
    if dayNum <= 12 and dayNum > 0:
        return months[dayNum - 1]
    return "ERR"


def convertDateToWord(s: str):
    dateNumArr: List[int] = list(map(int, s.split(".")))
    dayWord = ordinalToWord(dateNumArr[0])
    monthWord = monthNumToWord(dateNumArr[1])
    yearWord = numberToWord(dateNumArr[2])
    return f"the {dayWord} of {monthWord} {yearWord}"


# -----------------
# Word to num part
# -----------------


def monthToNum(word: str):
    for i in range(len(months)):
        if word == months[i]:
            return i + 1
    return "ERR"


def ordinalWordToNum(word: str) -> Any:
    for i in range(len(ordinals)):
        if ordinals[i][0] == word:
            return ordinals[i][1]
    word = word[:-2]  # removing "th" suffix
    for i in range(len(numbers)):
        if word == numbers[i][0]:
            return numbers[i][1]
    return None


def wordToNum(word: str) -> Any:
    for i in range(len(numbers)):
        if word == numbers[i][0]:
            return numbers[i][1]
    return None


def dayToNum(word: str) -> int:
    arr: List[str] = word.split("-")
    out: int = 0
    if len(arr) == 2:
        out += wordToNum(arr[0])
        out += ordinalWordToNum(arr[1])
    elif len(arr) == 1:
        out = ordinalWordToNum(arr[0])
    return out


def indexOfLastWord(word: str):
    for i in range(len(word) - 1, -1, -1):
        curr = word[i:]
        if wordToNum(curr) != None:
            return i
    return None


def yearToNum(word: str):
    # checking from end, removing words found in numbers array and summing them up
    out = 0
    index = indexOfLastWord(word)
    while index != None:
        firstWord = word[index:]
        num = wordToNum(firstWord)
        nextWordIndex = indexOfLastWord(word[:index])
        nextWord = word[nextWordIndex:index]
        nextNum = wordToNum(nextWord)
        if nextNum == None and num == 1:
            return 1
        if nextNum > num and out != 0:
            return None
        if nextNum == None:
            return num
        if (num >= 10 or nextNum == 1000 or nextNum == 100) and num < 100:
            out += num
            word = word[:index]
        else:
            if nextNum > num:
                out += num + nextNum
            else:
                out += num * nextNum

            word = word[:nextWordIndex]
        index = indexOfLastWord(word)
    return out


def convertWordToDate(word: str):
    word = word.replace("the ", "")
    word = word.replace("of ", "")
    wordArr: List[str] = list(map(str, word.split(" ")))
    monthNum = monthToNum(wordArr[1])
    dayNum = dayToNum(wordArr[0])
    return f"{dayNum}.{monthNum}.{yearToNum(wordArr[2])}"


# validation


def isInNumFormat(inp: str) -> bool:
    try:
        numArr: List[int] = list(map(int, inp.split(".")))
    except:
        return False
    return True


def numDateIsValid(date: str) -> bool:
    try:
        numArr: List[int] = list(map(int, date.split(".")))
    except:
        return False
    if len(numArr) != 3:
        return False
    if numArr[1] > 12 or numArr[1] <= 0:
        return False
    if not dayIsValid(numArr[0], numArr[1]):
        return False
    if numArr[2] > 9999 or numArr[2] <= 0:
        return False
    return True


def dayIsValid(day: int, month: int) -> bool:
    if month <= 7:
        if month % 2 == 0:
            maxDaysInMonth = 30
        else:
            maxDaysInMonth = 31

        if month == 2:
            maxDaysInMonth = 29
    else:
        if month % 2 == 1:
            maxDaysInMonth = 30
        else:
            maxDaysInMonth = 31
    if day <= 0 or day > maxDaysInMonth:
        return False
    return True


def isPartOfAllowedWords(s: str) -> bool:
    if s in helpers:
        return True
    if s in months:
        return True
    found = False
    for row in numbers:
        if row[0] == s or (row[0] + "th") == s:
            found = True
        if found:
            return True
    found = False
    for row in ordinals:
        if row[0] == s:
            found = True
        if found:
            return True
    return False


def validateString(inp: str):
    return validateStringHelpler(inp, 0)


def validateStringHelpler(inp, i):
    outer = inp
    if isPartOfAllowedWords(inp):
        return True
    while not isPartOfAllowedWords(inp):
        inp = outer[len(outer) - i - 1 :]
        if len(inp) == len(outer):
            return False
        i += 1
    return validateStringHelpler(outer[: len(outer) - i], 0)


def wordDateIsValid(s: str) -> bool:
    # TODO: check if string consists only of stated words
    if validateString(s.replace(" ", "").replace("-", "")) == False:
        return False
    if s.find("of") < 0:
        return False
    if s.find("the") < 0:
        return False
    return True


def convertBidirectional(s: str) -> str:
    if isInNumFormat(s):  # formatted like "the tenth of October fivehundrednine"
        if not numDateIsValid(s):
            return "ERROR"
        else:
            return convertDateToWord(s)
    else:  # formatted like "15.10.191"
        num: str = ""
        try:
            num = convertWordToDate(s)
        except:
            return "ERROR"
        if not numDateIsValid(num):
            return "ERROR"
        elif not wordDateIsValid(s):
            return "ERROR"
        else:
            return str(num)


if __name__ == "__main__":
    # dateString = "the thirty-first of December one"
    dateString = input()
    print(convertBidirectional(dateString))
