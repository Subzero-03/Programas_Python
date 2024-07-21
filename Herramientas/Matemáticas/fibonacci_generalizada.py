import sys
sys.set_int_max_str_digits(65536)

def fibonacci(n):
    number1 = int(input("Ingresa el primer número: "))
    number2 = int(input("Ingresa el segundo número: "))
    x = [number1, number2]
    for i in range(n - 2):
        x.append(x[i] + x[i + 1])
    return x

n = int(input())
print(fibonacci(n))