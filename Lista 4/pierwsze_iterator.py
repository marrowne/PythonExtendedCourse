"""
Zaimplementuj to samo zadanie które wykonałaś/wykonałeś z listy 3., ale
wykorzystaj do tego iteratory. Zbadaj, która teraz wersja jest najszybsza.
Przetestuj działanie implementacji dla różnych argumentów, np. dla 10, 100,
1000 etc. Wypisz na konsolę czasy działania dla poszczególnych danych
i implementacji w ładnie sformatowany sposób, na przykład

        | funkcyjna | skladana  | iterator
     10 | 0.001     | 0.002     | 0.003
    100 | 0.010     | 0.020     | 0.030
   1000 | 0.100     | 0.200     | 0.300

Można też plik sformatować tak, aby wynik mógł być wejściem dla jakiegoś programu
rysującego wykresy, np. gnuplot czy arkusz kalkulacyjny.
"""

from math import sqrt
from functools import reduce
from itertools import islice

def pierwsze_skladana(n):
    no_primes = [not_prime for interval in range(2, int(sqrt(n)+1)) for\
                 not_prime in range(interval*2, n+1, interval)]
    primes = [interval for interval in range(2, n+1) if interval not in no_primes]
    return primes

def pierwsze_funkcyjna(n):
    not_in_list = lambda _list: lambda x: x not in _list

    list1 = list(map(lambda i: list(range(i*2, n+1, i)),\
                 range(2, n+1)))
    list2 = reduce(lambda x, y: x + list(filter(not_in_list(x), y)),\
               list1)
    list3 = filter(not_in_list(list2), range(2, n+1))

    return list(list3)


class PierwszeIterator:
    def __init__(self):
        self.current = 1

    def __next__(self):
        self.current += 1
        while 1:
            if self.current == 2:
                return self.current
            for i in range(2, self.current):
                if self.current % i == 0:
                    return None
            return self.current

    def __iter__(self):
        return self

def pierwsze_iterowane(n):
    p = PierwszeIterator()
    res = []

    for prime in islice(p, n-1):
        if prime:
            res.append(prime)
    return res

if __name__ == '__main__':
    import timeit
    print("[10]")
    print("A version using list comprehension executes in:",\
          timeit.timeit("pierwsze_skladana(10)",\
                        setup="from __main__ import pierwsze_skladana", number=1), "secs,")
    print("a functional version executes in:",\
          timeit.timeit("pierwsze_funkcyjna(10)",\
                        setup="from __main__ import pierwsze_funkcyjna", number=1), "secs")
    print("and a version using an iterator executes in:",\
          timeit.timeit("pierwsze_iterowane(10)",\
                        setup="from __main__ import pierwsze_iterowane", number=1), "secs")
    print("[100]")
    print("A version using list comprehension executes in:",\
          timeit.timeit("pierwsze_skladana(100)",\
                        setup="from __main__ import pierwsze_skladana", number=1), "secs,")
    print("a functional version executes in:",\
          timeit.timeit("pierwsze_funkcyjna(100)",\
                        setup="from __main__ import pierwsze_funkcyjna", number=1), "secs")
    print("and a version using an iterator executes in:",\
          timeit.timeit("pierwsze_iterowane(100)",\
                        setup="from __main__ import pierwsze_iterowane", number=1), "secs")
    print("[1000]")
    print("A version using list comprehension executes in:",\
          timeit.timeit("pierwsze_skladana(1000)",\
                        setup="from __main__ import pierwsze_skladana", number=1), "secs,")
    print("a functional version executes in:",\
          timeit.timeit("pierwsze_funkcyjna(1000)",\
                        setup="from __main__ import pierwsze_funkcyjna", number=1), "secs")
    print("and a version using an iterator executes in:",\
          timeit.timeit("pierwsze_iterowane(1000)",\
                        setup="from __main__ import pierwsze_iterowane", number=1), "secs")

print("\n", pierwsze_iterowane(20))