"""
Poniżej są zadania polegające na implementacji funkcji zwracających listy
liczb naturalnych. Każde z zadań należy wykonać w dwóch wersjach: w wersji
z listą składaną i wersję funkcyjną.

Wersja z listą składaną powinna być w postaci jednej listy składanej,
zawierającej być może inną listę składaną. W przypadku bardzo długich wyrażeń
akceptowane będzie wydzielenie podlisty składanej

    def zadana_funkcja(n):
        lista_tymcz = [ lista skladana ]
        return [ lista_składana_zawierająca lista_tymcz ]

Implementacja funkcyjna powinna korzystać z funkcji dedykowanych do operacji
na listach: filter, map czy reduce.

Zbadaj, która wersja jest szybsza.

Do zaprogramowania powyższych zadań wystarczą standardowe funkcje i operatory,
nie ma potrzeby korzystania z dodatkowych modułów

-------------------------------------------------------------------------------

Zaprogramuj jednoargumentowe funkcje pierwsze_skladana(n) i
pierwsze_funkcyjna(n), które zwracają listę liczb pierwszych nie większych niż
n, na przykład:

    >>> pierwsze(20)
    [2, 3, 5, 7, 11, 13, 17, 19]
"""

from math import sqrt
from functools import reduce

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

if __name__ == '__main__':
    import timeit
    print("A version using list comprehension executes in:",\
          timeit.timeit("pierwsze_skladana(20)",\
                        setup="from __main__ import pierwsze_skladana", number=1), "secs")
    print("and a functional varsion executes in:",\
          timeit.timeit("pierwsze_funkcyjna(20)",\
                        setup="from __main__ import pierwsze_funkcyjna", number=1), "secs")