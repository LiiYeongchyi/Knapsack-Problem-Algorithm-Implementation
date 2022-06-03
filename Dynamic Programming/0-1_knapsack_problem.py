"""
The input file contains n + 1 lines. The first line contains two integers: 
the first is the number of items in the problem, n; the second number is 
the capacity of the knapsack, K. The remaining lines present the data for 
each of the items. Each line, from line 2 to line n + 1, contains two 
integers, the item's value v_i followed by its weight w_i.

This code is a simple dynamic programming implementation.
"""


class State:
    def __init__(self, file):
        # Read the file, save the items as a list that contains each item
        # as a tuple (v_i, w_i)
        self.total, self.capacity = map(int, file.readline().split(" "))
        self.items = list(
            map(lambda x: tuple(map(int, x[:-1].split(" "))), file.readlines()))

    def solutionByDP(self):
        f = [0]*(self.capacity+1)
        for i in range(0, self.total):
            l = self.capacity
            while l >= self.items[i][1]:
                if f[l] < f[l - self.items[i][1]] + self.items[i][0]:
                    f[l] = f[l - self.items[i][1]] + self.items[i][0]
                l -= 1
        return f[self.capacity]


file = open("ks_4.txt", "r")
state = State(file)
print(state.solutionByDP())
file.close()

file = open("ks_100.txt", "r")
state = State(file)
print(state.solutionByDP())
file.close()

file = open("ks_10000.txt", "r")
state = State(file)
print(state.solutionByDP())
file.close()
