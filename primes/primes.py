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
        __extend_list_of_primes()
    return N in primeKeys


def is_prime_no_memo(N):
    if N == 2 or N == 3:
        return True
    if N < 2 or N % 2 == 0:
        return False
    if N < 9:
        return True
    if N % 3 == 0:
        return False
    a = math.isqrt(N)
    b = 5
    while b <= a:
        if N % b == 0:
            return False
        if N % (b + 2) == 0:
            return False
        b = b + 6
    return True


def factorize(N):
    global primeKeys
    dividers = []
    limit = int(math.sqrt(N)) + 1
    l = limit

    for pr in generate_primes_below(limit):
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
    return __greatest_common_denominator_Euclid(a, b) == 1


def get_co_primes(N, upper_limit):
    factorsOfN = set(factorize(N))
    upper_limit = int(math.ceil(upper_limit))

    a = [True] * upper_limit

    for f in factorsOfN:
        a[f - 1] = False
        for j in range(f + f - 1, upper_limit, f):
            a[j] = False

    result = [i + 1 for (i, isRelativelyPrime) in enumerate(a) if a[i]]

    return result


def get_totient(N):
    factors = factorize(N)
    totientFactors = set((1 - 1 / x) for x in factors)
    return round(N * __get_product(totientFactors))


def get_all_factors(N):
    if N == 1:
        return {1}
    primeFactors = factorize(N)
    allPrimeFactorCombs = __powerset(primeFactors)
    allFactors = set(__get_product(comb) for comb in allPrimeFactorCombs)
    allFactors.add(1)
    return allFactors


def get_proper_factors(N):
    if N == 1:
        return {1}
    allFactors = get_all_factors(N)
    allFactors.remove(N)
    return allFactors


def __greatest_common_denominator_Euclid(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a

    return a + b


def greatest_common_denominator(numbers):
    if len(numbers) < 2:
        raise ValueError('Too little numbers are given tp fin GCD.')
        
    if len(numbers) == 2:
        return __greatest_common_denominator_Euclid(numbers[0], numbers[1])

    common_factors = []
    factor_lists = []

    for number in numbers:
        factor_lists.append(factorize(number))

    factors_of_first = factor_lists[0].copy()

    for factor in factors_of_first:
        if all(factor in factors for factors in factor_lists[1:]):
            common_factors.append(factor)
            for factors in factor_lists:
                factors.remove(factor)

    result = __get_product(common_factors) if len(common_factors) > 0 else 1
    return result


def generator():
    global __biggestPrime
    i = 2
    yield 2
    while True:
        if primeKeys[i] is None:
            __extend_list_of_primes()
        i = primeKeys[i]
        yield i


def generate_primes_below(N):
    if N < 2:
        return []
    while __biggestPrime <= N:
        __extend_list_of_primes()
    active_prime = 2
    while active_prime < N:
        yield active_prime
        active_prime = primeKeys[active_prime]


def generate_N_primes(N):
    while len(primeKeys) < N:
        __extend_list_of_primes()
    activePrime = 2
    for i in range(0, N):
        yield activePrime
        activePrime = primeKeys[activePrime]


def memorize_primes_below_limit(limit):
    global __biggestPrime, __seed, primeKeys
    a = bitarray.bitarray(limit, endian='little')  # Initialize the primality list
    a.setall(True)
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            for n in range(i * i, limit, i):  # Mark factors non-prime
                a[n] = False

    next_prime = None
    for i in range(limit - 1, 4, -1):
        if a[i]:
            primeKeys[i] = next_prime
            next_prime = i
    primeKeys[3] = 5

    for i in range(limit - 1, 4, -1):
        if a[i]:
            __biggestPrime = i
            __seed = (limit - 1) // 6
            break


def get_biggest_memorized_prime():
    global __biggestPrime
    return __biggestPrime


def __extend_list_of_primes():
    global __biggestPrime, __seed
    found_some = False
    while not found_some:
        tested1 = __seed * 6 - 1
        tested2 = __seed * 6 + 1
        if __is_newfound_prime(tested1):
            primeKeys[__biggestPrime] = tested1
            __biggestPrime = tested1
            primeKeys[tested1] = None
            found_some = True
        if __is_newfound_prime(tested2):
            primeKeys[__biggestPrime] = tested2
            __biggestPrime = tested2
            primeKeys[tested2] = None
            found_some = True
        __seed += 1


def __get_product(iterable):
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


def __is_newfound_prime(x):
    if x % 2 == 0:
        return False
    limit = int(math.sqrt(x))

    active_prime = 2
    while active_prime <= limit:
        if x % active_prime == 0:
            return False
        if primeKeys[active_prime] is None:
            break
        active_prime = primeKeys[active_prime]

    if active_prime > limit:
        return True

    test_number = __biggestPrime + 4
    while test_number <= limit:
        if x % test_number == 0:
            return False
        test_number += 2

    return True
