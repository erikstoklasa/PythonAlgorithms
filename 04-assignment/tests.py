# import date


def testFunction(f, arr):
    total = len(arr)
    successful = 0
    for row in arr:
        inp = row[0]
        output = f(inp)
        expected = row[1]
        if output == expected:
            successful += 1
        else:
            print("FAIL")
            print(f"Input:{inp}")
            print(f"Output:{output}")
            print(f"Expected:{expected}")
    print(f"SUCCESSFULLY {successful}/{total}")


numToWordArr = [
    ["18.1.4106", "the eighteenth of January fourthousandonehundredsix"],
    ["8.5.5200", "the eighth of May fivethousandtwohundred"],
    ["15.10.191", "the fifteenth of October onehundredninetyone"],
    ["31.12.6450", "the thirty-first of December sixthousandfourhundredfifty"],
    ["30.6.1000", "the thirtieth of June onethousand"],
]
wordToNumArr = [
    ["the eighteenth of January fourthousandonehundredsix", "18.1.4106"],
    ["the eighth of May fivethousandtwohundred", "8.5.5200"],
    ["the fifteenth of October onehundredninetyone", "15.10.191"],
    ["the tenth of October fivehundrednine", "10.10.509"],
    ["the sixth of August ninethousandeight", "6.8.9008"],
    ["the thirtieth-first of March twohundredthirtyfour", "ERROR"],
    ["the first January onehundredtwentythree", "ERROR"],
    ["the first of January onehundreddtwentythree", "ERROR"],
    ["the thirty-first of December one", "31.12.1"],
    ["the first of January onehundredthreetwenty", "ERROR"],
]

testFunction(date.convertBidirectional, numToWordArr)
testFunction(date.convertBidirectional, wordToNumArr)
