from time import time


#  one of the main things is that generators are functions
#  so if generators are functions, what is the main difference between them and regular functions?

#  here we will create a generator function and after
def gen(s):
    for i in s:
        yield i


g = gen('oleg')

#  we can also open this file in interactive mode (-i, it means that all code from file
#  will be uploaded to the terminal) in cmd with the following command:
# path\asynchronicity-basics-python python -i 04_generators.py

#  it is possible to pause function gen and continue its execution from the same place later
#  it's impossible to achieve the same delay print with the use of regular functions,
#  they will give all the sequence at once

# it is important to understand that next(g) for example is a unique way of transferring execution control, in
# this way postponing it's execution later in the code

# now we will create a function for generating unique file names:

def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() * 1000)  # here we will get number of seconds that passed from 01.01.1970 (Unix time)

        yield pattern.format(str(t))

        sum = 234 + 234
        print(sum)

        # differences between yield and return:
        # 1) after return function execution is over, but yield only stops it and
        # following next() continues it later from the point after yield. It will print sum and pattern before the
        # next yield
        # 2) several yield are possible within the same function


# Round Robin cycle

# example: there are two swimming pools, one is full, other is empty. You have several friends and several buckets,
# you give to each friend one bucket and say them to fill another pool. They fill a bucket from
# pool with water, go to an empty pool and fill it, after that they stand in line with empty bucket
# and wait when it will be there turn to fill the bucket

# previous generator
def gen1(s):
    for i in s:
        yield i


# generator with numbers
def gen2(n):
    for i in range(n):
        yield i


g1 = gen1('oleg')
g2 = gen2(4)

# after that we create a list of tasks and place our generators there
tasks = [g1, g2]

# after that we write a cycle by itself
while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass

# as an output we will get letters crossing with numbers

# this example illustrates that we are regulating execution of functions by their order. Instead of using simple
# print(), it is possible to send signals or smth else.
# in this way we are controlling execution



