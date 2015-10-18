"""
Wyjątki mogą służyć nie tylko do sygnalizacji jakiejś niepożądanej sytuacji,
ale także do zakończenia działania funkcji i przekazania obliczonej wartości.
Na przykład funkcja obliczająca rekurencyjnie silnię w końcowym etapie obliczeń
wymaga wielokrotnego wykonania instrukcji return wyrażenie aby zwinąć stos
wywołań rekurencyjnych. Zamiast tego wystarczy na końcu obliczeń zgłosić
wyjątek raise wynik zawierający wynik obliczeń i w odpowiednim miejscu obsłużyć
ten wyjątek. Zaprogramuj wersję rekurencyjną i z wywołaniem wyjątku
funkcji obliczających

    • silnię liczby n;
    • n-ty element ciągu Fibonacciego.

Zbadaj (na przykład za pomocą modułu timeit) która wersja jest szybsza.
"""

# Below are popular versions of functions

def factorial_classic(arg):
    if arg > 0:
        return arg * factorial_classic(arg-1)
    else:
        return 1

def fibonacci_number_classic(nth):
    if nth>2:
        return fibonacci_number_classic(nth-1)+fibonacci_number_classic(nth-2)
    else:
        return 1



# There are exception version functions below

def factorial(arg, res = 1):
    if arg > 0:
        res *= arg
        factorial(arg-1, res)
    else:
        raise Exception(res)

def factorial_exception(arg):
    try:
        factorial(arg)
    except Exception as res:
        return res


def fibonacci(nth, prev1 = 0, prev2 = 1):
    if nth > 0:
        (prev2, prev1) = (prev1, prev1+prev2)
        fibonacci(nth-1, prev1, prev2)
    else:
        raise Exception(prev1)

def fibonacci_number_exception(nth):
    try:
        fibonacci(nth)
    except Exception as res:
        return res


# Time of execution

if __name__ == '__main__':
    import timeit
    print("A casual factorial function executes in:",\
          timeit.timeit("factorial_classic(50)", \
                        setup="from __main__ import factorial_classic"),"secs")
    print("and an another using exception executes in:",\
          timeit.timeit("factorial_exception(50)", \
                        setup="from __main__ import factorial_exception"),"secs\n")
    print("A casual Fibonacci function executes in:",\
          timeit.timeit("fibonacci_number_classic(15)", \
                        setup="from __main__ import fibonacci_number_classic"),"secs")
    print("and an another unsing exeception executes in:",\
          timeit.timeit("fibonacci_number_exception(15)", \
                        setup="from __main__ import fibonacci_number_exception"),"secs")