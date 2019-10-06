#!/usr/bin/python3
from data import Data
from decisionTree import DecisionNode, DecisionTree, RandomForest

def evaluatePerformance(data):
    #Splits instances into folds
    folds = data.generateStratifiedFolds(3)
    allPerformances = []
    #Repeats using each fold as testing data once
    for iteration in range(len(folds)):
        #Adds one fold as testing data
        testingData = Data(data.className, data.numericAttr)
        for instance in folds[iteration]:
            testingData.addInstance(instance)

        #Adds the other folds as training data
        trainingData = Data(data.className, data.numericAttr)
        for i in range(len(folds)):
            if i != iteration:  #Skips the fold used as testing set
                for instance in folds[i]:
                    trainingData.addInstance(instance)

        #Creates and trains the forest
        forest = RandomForest(trainingData, testingData)
        forest.generateForest(5)

        #Classifies the testing set
        predictions = []
        for instance in forest.testingData.instances:
            predictions.append(forest.classify(instance))

        rightGuesses = 0
        for i in range(len(predictions)):
            if predictions[i] == forest.testingData.instances[i][forest.testingData.className]:
                rightGuesses += 1

        print("----- Forest {} -----".format(iteration))
        forest.evaluateTreesPerformance()
        print("Forest performance: {:.2f}%".format((rightGuesses/len(predictions))*100))

        allPerformances.append(rightGuesses/len(predictions))   #Adds this iteration's performance to the list

    print("----------")
    print("Model's average performance: {:.2f}%".format(sum(allPerformances)/len(allPerformances)))
    print("----------")


# -------------------------------------------------------------------
# Credit g
filename = '../data/credit-g.csv'
className = 'class'
data = Data(className, numeric=['duration', 'credit_amount', 'installment_commitment', 
                                'residence_since', 'age', 'existing_credits', 
                                'num_dependents'])
data.parseFromFile(filename, delimiter=',', quotechar='"')


# for key in data.instances[0]:
#     if key == data.className:
#         print("\t{}: {} (CLASS)".format(key, data.instances[0][key]))
#     elif data.isNumeric(key):
#         print("{}: {} (numeric)".format(key, data.instances[0][key]))
#     else:
#         print("{}: {} (categoric)".format(key, data.instances[0][key]))



tree = DecisionTree(data, m=15)
tree.train()
# tree.print()

correctGuesses = 0
wrongGuesses = 0
for entry in data.instances:
    right = entry[data.className]
    guess = tree.classify(entry)

    if right == guess:
        correctGuesses += 1
    else:
        wrongGuesses += 1

print("CORRECT: {correct}, WRONG: {wrong}".format(correct=correctGuesses, 
                                                  wrong=wrongGuesses))




# Exemplo
# filename = '../data/dadosBenchmark_validacaoAlgoritmoAD.csv'
# className = 'Joga'
# data = Data(className, numeric=["Numero"])
# data.parseFromFile(filename)
# tree = DecisionTree(data)
# tree.train()
# tree.print()

# evaluatePerformance(data)
# Tempo;Temperatura;Umidade;Ventoso;Joga
# Ensolarado;Quente;Alta;Falso;Nao
#entry = {'Tempo': 'Ensolarado', 'Temperatura': 'Quente', 'Umidade': 'Alta', 'Ventoso': 'Falso'}
#print("Classificação: {}".format(tree.classify(entry)))

# correctGuesses = 0
# wrongGuesses = 0
# for entry in data.instances:
#     right = entry[data.className]
#     guess = tree.classify(entry)

#     if right == guess:
#         correctGuesses += 1
#     else:
#         wrongGuesses += 1


# if wrongGuesses > 0:
#     print("Number of correct guesses: {}".format(correctGuesses))
#     raise SystemError("WRONG GUESSES: {}".format(wrongGuesses))
# else:
#     print("SUCCESS, {} correct guesses".format(correctGuesses))


# evaluatePerformance(data)
# forest = RandomForest(data)
# forest.generateForest(5)
# forest.evaluateTreesPerformance()


