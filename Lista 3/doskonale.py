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

Zaprogramuj jednoargumentowe funkcje doskonale_skladana(n)
i doskonale_funkcyjna(n), które zwracają listę liczb doskonałych nie większych
niż n, na przykład:

    >>> doskonale(10000)
    [6, 28, 496, 8128]
"""

from functools import reduce

def doskonale_skladana(n):
    factors = lambda x: [i for i in range(1, x) if x % i == 0]
    # pominięcie dzielenia przez samą siebie

    perfect_numbers = [number for number in range(1, n+1)\
                       if sum(factors(number)) == number]
    return perfect_numbers

def is_perfect(x):
    dividers = filter(lambda i: x % i == 0, range(1, x))
    return reduce(lambda x, y: x + y, dividers) == x

def doskonale_funkcyjna(n):
    return list(filter(lambda x: is_perfect(x), range(2, n+1)))



if __name__ == '__main__':
    import timeit
    print("A version using list comprehension executes in:",\
          timeit.timeit("doskonale_skladana(1000)",\
                        setup="from __main__ import doskonale_skladana", number=1), "secs")
    print("and a functional version executes in:",\
          timeit.timeit("doskonale_funkcyjna(1000)",\
                        setup="from __main__ import doskonale_funkcyjna", number=1), "secs")

print(doskonale_skladana(10000))
print(doskonale_funkcyjna(10000))