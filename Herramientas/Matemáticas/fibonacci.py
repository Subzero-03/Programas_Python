import sys
sys.set_int_max_str_digits(65536)

def fibonacci(n):
    x = [0, 1]
    for i in range(n - 2):
        x.append(x[i] + x[i + 1])
    return x

n = int(input())
print(fibonacci(n))
