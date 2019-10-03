#!/usr/bin/python3
from data import Data
from decisionTree import DecisionNode, DecisionTree


filename = '../data/dadosBenchmark_validacaoAlgoritmoAD.csv'
className = 'Joga'
data = Data(className)
data.parseFromFile(filename)

tree = DecisionTree(data)
tree.train()
tree.print()


correctGuesses = 0
wrongGuesses = 0
for entry in data.instances:
    right = entry[data.className]
    guess = tree.classify(entry)

    if right == guess:
        correctGuesses += 1
    else:
        wrongGuesses += 1


if wrongGuesses > 0:
    print("Number of correct guesses: {}".format(correctGuesses))
    raise SystemError("WRONG GUESSES: {}".format(wrongGuesses))
else:
    print("SUCCESS, {} correct guesses".format(correctGuesses))
