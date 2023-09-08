def fizzbuzz(num):
  if num % 15 == 0:
    return "FizzBuzz" 
  elif num % 3 == 0:
    return "Fizz"
  elif num % 5 == 0: 
    return "Buzz"
  else:
    return str(num)

# Logging middleware
def log(next_func):
  def wrapper(num):
    print("Logging...")
    result = next_func(num)
    print("Logged!")
    return result
  return wrapper

# Input validation middleware  
def validate(next_func):
  def wrapper(num):
    if not isinstance(num, int):
      return "Invalid input"
    return next_func(num)
  return wrapper  

# Compose function
def compose(f, middlewares):

  # Start with core fizzbuzz function
  def composed(x):
    return f(x)
  
  # Wrap middlewares around it 
  for m in reversed(middlewares):
    composed = m(composed)

  return composed

# Create middleware chain
chain = compose(fizzbuzz, [log, validate])

# Test it
print(chain(3))
print(chain('3'))