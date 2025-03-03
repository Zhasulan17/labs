# 1
import math

numbers = [2, 3, 4, 5]
result = math.prod(numbers)
print(result)


# 2
import math     

def counter(s):
    upper = sum(1 for c in s if c.isupper())
    lower = sum(1 for c in s if c.islower())
    return upper, lower
string = "HelloWorld"
upper, lower = counter(string)
print("Uppercase letters:", upper)
print("Lowercase letters:", lower)


# 3
palindrome = "madam"

is_palindrome = palindrome == palindrome[::-1]
print("Is palindrome:", is_palindrome)
'''     
"madam" → True
"racecar" → True
"hello" → False
'''


# 4
import time
import math

num, delay = 25100, 2123
time.sleep(delay / 1000) 
result = math.sqrt(num)
print(f"Square root of {num} after {delay} milliseconds is", result)


# 5
tuple_data = (True, True, False)
result = all(tuple_data)
print("All elements are True:", result)








