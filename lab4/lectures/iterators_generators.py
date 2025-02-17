mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))



mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))



mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x)



mystr = "banana"

for x in mystr:
  print(x)


class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))



class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
  print(x)


#----------------------------
# Generators

def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1



# Using our generator
for number in count_up_to(5):
    print(number)



# Generator expression
squares = (x**2 for x in range(5))

# Using our generator
for square in squares:
    print(square)



def div_generator(a, b):
    try:
        result = a / b
        yield result
    except ZeroDivisionError:
        yield "Cannot divide by zero!"

# Using our generator
g = div_generator(10, 2)
print(next(g))  # Prints: 5.0

g = div_generator(10, 0)
print(next(g))  # Prints: Cannot divide by zero!



# Normal function
def get_squares(n):
    squares = []
    for i in range(n):
        squares.append(i**2)
    return squares

# Generator function
def gen_squares(n):
    for i in range(n):
        yield i**2

# Using the normal function
print(get_squares(5))  # Prints: [0, 1, 4, 9, 16]

# Using the generator function
for square in gen_squares(5):
    print(square)  # Prints each square on a new line



import asyncio

async def async_gen():
    for i in range(3):
        await asyncio.sleep(1)
        yield i

async def main():
    async for item in async_gen():
        print(item)

asyncio.run(main())



def echo_generator():
    while True:
        received = yield
        print(f"Received: {received}")

g = echo_generator()
next(g)  # Prime the generator
g.send("Hello")  # Prints: Received: Hello
g.send("World")  # Prints: Received: World