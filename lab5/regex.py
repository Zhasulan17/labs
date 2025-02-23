# 1
import re
text = "Yesterday I went to the park"

x = re.findall("Yes.*y", text)
print(x)


# 2
import re

bob = r'ab{2,3}'
examples = ["abb", "abbb", "abbbb", "ab", "a", "b", "aaabb"]

for i in examples:
    if re.search(bob, i):  
        print(f"{i} - True")
    else:
        print(f"{i} - False")

# 3
import re
text = "Do_you want_to become_gamer?"
x = re.findall(r'\b[a-z]+_[a-z]+\b', text)
print(x)


# 4
import re

text = "Hello Zhasulan Zhambyluly"
print(re.findall(r'[A-Z][a-z]+', text))


# 5
import re 

text = input()
x = re.findall(r'^a.*b$' , text)
print(x)


# 6
import re
text = input()
text = re.sub(r'[ ,.]', ':', text)
print(text)


# 7
import re

text = "hello_world_test_string"
p = ''.join(word.title() if i > 0 else word for i, word in enumerate(text.split('_')))
print(p)


# 8
import re
text = input()
x = re.findall(r'[A-Z][a-z]*', text)
print(x)


# 9
import re

text = "Hello,MyNameIsZhasulan"
p = re.sub(r'([A-Z])', r' \1', text)
print(p)


# 10
import re

text = "Hello,MyNameIsZhasulan"
p = re.sub(r'([A-Z])', r'_\1', text).lower().lstrip('_')
print(p)
