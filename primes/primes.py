# 26.11.2022

import math
import itertools
import bitarray

primeKeys = dict()
__biggestPrime = 3
__seed = 1
primeKeys[2] = 3
primeKeys[3] = None


def clear_cash():
    global primeKeys, __biggestPrime, __seed
    primeKeys = dict()
    __biggestPrime = 3
    __seed = 1
    primeKeys[2] = 3
    primeKeys[3] = None


def is_prime(N):
    global primeKeys
    while __biggestPrime <= N:
        __ExtendListOfPrimes()
    return N in primeKeys


def factorize(N):
    global primeKeys
    dividers = []
    limit = int(math.sqrt(N)) + 1
    l = limit

    for pr in GeneratePrimesBelow(limit):
        if pr > l:
            break
        while N % pr == 0:
            N = N // pr
            dividers.append(pr)
        l = int(math.sqrt(N)) + 1

    if N != 1:
        dividers.append(N)

    return dividers

def factorize_as_powers_of_primes(N):
    powers = {}
    for f in factorize(N):
        powers.setdefault(f, 0)
        powers[f] += 1
    return powers


def is_coprime(a, b):
    return greatest_common_denominator_Euclid(a, b) == 1


def GetCoPrimes(N, upperLimit):
    factorsOfN = set(factorize(N))
    upperLimit = int(math.ceil(upperLimit))

    a = [True] * upperLimit

    for f in factorsOfN:
        a[f-1] = False
        for j in range(f + f - 1, upperLimit, f):
            a[j] = False

    result = [i + 1 for (i, isRelativelyPrime) in enumerate(a) if a[i]]

    return result


def GetTotient(N):
    factors = factorize(N)
    totientFactors = set((1 - 1 / x) for x in factors)
    return round(N * __getProduct(totientFactors))


def GetAllFactors(N):
    if N == 1:
        return {1}
    primeFactors = factorize(N)
    allPrimeFactorCombs = __powerset(primeFactors)
    allFactors = set(__getProduct(comb) for comb in allPrimeFactorCombs)
    allFactors.add(1)
    return allFactors


def GetProperFactors(N):
    if N == 1:
        return {1}
    allFactors = GetAllFactors(N)
    allFactors.remove(N)
    return allFactors


def greatest_common_denominator_Euclid(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a

    print(a + b)


def greatest_common_denominator_with_factorization(*numbers):
    if len(numbers) < 2:
        raise ValueError('Too little numbers are given tp fin GCD.')

    common_factors = []
    factor_lists = []

    for number in numbers:
        factor_lists.append(factorize(number))

    factors_of_first = factor_lists[0].copy()

    for factor in factors_of_first:
        if False not in (factor in factors for factors in factor_lists[1:]):
            common_factors.append(factor)
            for factors in factor_lists:
                factors.remove(factor)

    result = __getProduct(common_factors) if len(common_factors) > 0 else 1
    return result


def generator():
    global __biggestPrime
    i = 2
    yield 2
    while True:
        if primeKeys[i] is None:
            __ExtendListOfPrimes()
        i = primeKeys[i]
        yield i


def GeneratePrimesBelow(N):
    if N < 2:
        return []
    while __biggestPrime <= N:
        __ExtendListOfPrimes()
    activePrime = 2
    while activePrime < N:
        yield activePrime
        activePrime = primeKeys[activePrime]


def GenerateNPrimes(N):
    while len(primeKeys) < N:
        __ExtendListOfPrimes()
    activePrime = 2
    for i in range(0, N):
        yield activePrime
        activePrime = primeKeys[activePrime]


def MemorizePrimesBelowLimit(limit):
    global __biggestPrime, __seed, primeKeys
    a = bitarray.bitarray(limit, endian='little')  # Initialize the primality list
    a.setall(True)
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            for n in range(i * i, limit, i):  # Mark factors non-prime
                a[n] = False

    nextPrime = None
    for i in range(limit - 1, 4, -1):
        if a[i]:
            primeKeys[i] = nextPrime
            nextPrime = i
    primeKeys[3] = 5

    for i in range(limit - 1, 4, -1):
        if a[i]:
            __biggestPrime = i
            __seed = (limit - 1) // 6
            break


def get_biggest_memorized_prime():
    global __biggestPrime
    return __biggestPrime


def __ExtendListOfPrimes():
    global __biggestPrime, __seed
    foundSome = False
    while not foundSome:
        tested1 = __seed * 6 - 1
        tested2 = __seed * 6 + 1
        if __IsNewPrime(tested1):
            primeKeys[__biggestPrime] = tested1
            __biggestPrime = tested1
            primeKeys[tested1] = None
            foundSome = True
        if __IsNewPrime(tested2):
            primeKeys[__biggestPrime] = tested2
            __biggestPrime = tested2
            primeKeys[tested2] = None
            foundSome = True
        __seed += 1


def __getProduct(iterable):
    p = 1
    for i in iterable:
        p *= i
    return p


def __powerset(iterable):
    s = list(iterable)
    return tuple(
        itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(1,
                                                        len(s) + 1)))


def __IsNewPrime(x):
    if x % 2 == 0:
        return False
    limit = int(math.sqrt(x))

    activePrime = 2
    while activePrime <= limit:
        if x % activePrime == 0:
            return False
        if primeKeys[activePrime] is None:
            break
        activePrime = primeKeys[activePrime]

    if activePrime > limit:
        return True

    testNumber = __biggestPrime + 4
    while testNumber <= limit:
        if x % testNumber == 0:
            return False
        testNumber += 2

    return True
