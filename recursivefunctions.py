def factorial(n):
    if n == 1:
        return 1
    elif n > 1:
        return n*factorial(n-1)
    else: 
        return 0