from sifruj import Crypt
import numpy
import sys

def extendedEuclideanAlgorithm(a,b):
    if a == 0:
        return b, 0, 1
    gcd, u, v = extendedEuclideanAlgorithm(b % a, a)
    x = v - (b // a ) * u
    y = u
    return gcd, x, y

print(extendedEuclideanAlgorithm(10,25))


# n = sys.argv[1]
n = 865149046207
toDecode = "352566354542 704277294015 506632666345 494928356066 824421528359 325069048254 839239812833 536096809854 278474205010"
print(numpy.gcd(78, 24))
