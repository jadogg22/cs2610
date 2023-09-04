def fizzbuzz(n):
    for i in range(1, n):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 5 == 0:
            print("Buzz")
        elif i % 3 == 0:
            print("Fizz")
        else:
            print(i)

def constrain_middleware(next):
    def middleware(n):
        if n < 51:
            return next(n)
        else:
            return "that didnt work son"
    return middleware

def cap_middleware(next):
    def middleware(n):
        result = next(n)
        return result.upper()
    return middleware

middleware = cap_middleware(fizzbuzz)
middleware = constrain_middleware(middleware)


print(middleware(50))