"""
The input file contains n + 1 lines. The first line contains two integers: 
the first is the number of items in the problem, n; the second number is 
the capacity of the knapsack, K. The remaining lines present the data for 
each of the items. Each line, from line 2 to line n + 1, contains two 
integers, the item's value v_i followed by its weight w_i.

This code is a simple genetic algorithm (GA) implementation.
"""

from random import *


class State:
    def __init__(self, file):
        # Read the file, save the items as a list that contains each item
        # as a tuple (v_i, w_i)
        self.total, self.capacity = map(int, file.readline().split(" "))
        self.items = list(
            map(lambda x: tuple(map(int, x[:-1].split(" "))), file.readlines()))
        i = 0
        # "predicted" is the estimation of the number of ones in the solution
        self.predicted = self.capacity * self.total // sum(self.items[i][1]
                                                           for i in range(self.total))
        # "samples" generate the initial selection, with every possible solution
        # appears like "010101". 0 means the item is not selected.
        self.samples = []
        while i < 50:
            oneLoc = choices(list(range(self.total)), k=self.predicted)
            cur = "".join(
                "1" if i in oneLoc else "0" for i in range(self.total))
            if self.fitness(cur) > 0:
                self.samples.append(cur)
                i += 1

    def fitness(self, sample: str) -> int:
        # One-line code to calculate the total value of the items selected,
        # and return 0 if the total weight exceeds the requirement
        return sum(self.items[i][0] if sample[i] == "1" else 0 for i in range(self.total)) if sum(self.items[i][1] if sample[i] == "1" else 0 for i in range(self.total)) <= self.capacity else 0

    def mutation(self, sample: str) -> str:
        # Gene mutation, and you can adjust the mutation rate
        times = min(self.predicted, self.total // 10000)
        mutationLoc = [randint(0, self.total-1) for i in range(times)]
        listOfStr = list(sample)
        for i in mutationLoc:
            listOfStr[i] = "1" if listOfStr[i] == "0" else "0"
        return "".join(listOfStr)

    def crossover(self, sp1, sp2) -> str:
        return sp1[:self.total//2] + sp2[self.total//2:]

    def selection(self, spList) -> list:
        # Randomly pick solutions with fitness as weight
        return choices(spList, [self.fitness(i) for i in spList], k=max(2, self.total // 5))

    def iteration(self, spList) -> list:
        chosenParents = self.selection(spList)
        newSp = []
        num = len(chosenParents)
        i = 0
        while i < min(200, self.total):
            a, b = randint(0, num-1), randint(0, num-1)
            sp = self.mutation(self.crossover(
                chosenParents[a], chosenParents[b]))
            if self.fitness(sp) > 0:
                newSp.append(sp)
                i += 1
        return newSp

    def solution(self):
        population = self.samples
        maxValue = 0
        string = ""
        iterationTimes = 0
        # Modify 300 to adjust the number of iterations
        # Return the solution with the maximum total value
        while iterationTimes < 300:
            population = self.iteration(population)
            curMax = max(self.fitness(i) for i in population)
            if curMax > maxValue:
                maxValue = curMax
                string = population[list(
                    map(self.fitness, population)).index(maxValue)]
            iterationTimes += 1
        return maxValue, string


file = open("ks_4.txt", "r")
state = State(file)
print(state.solution())
file.close()

file = open("ks_100.txt", "r")
state = State(file)
print(state.solution())
file.close()

file = open("ks_10000.txt", "r")
state = State(file)
print(state.solution())
file.close()
