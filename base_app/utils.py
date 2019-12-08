import random
import string

def random_string_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# 
# print(random_string_generator())
#
# print(random_string_generator(size=50))
