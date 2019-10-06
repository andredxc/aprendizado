#!/usr/bin/python3
from data import Data
from decisionTree import DecisionNode, DecisionTree, RandomForest

def evaluatePerformance(data, nForests=3):
    #Splits instances into folds
    folds = data.generateStratifiedFolds(nForests)

    allPerformances = []
    allPrecisions = []
    allRecalls = []
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

        #Analizes results
        iterationPerformances = []
        iterationPrecisions = []
        iterationRecalls = []
        #Calculates performance, recall and precision for every class
        for classValue in forest.testingData.listClassValues():
            positiveClass = classValue

            truePositives = 0
            falsePositives = 0
            trueNegatives = 0
            falseNegatives = 0
            for i in range(len(predictions)):
                if predictions[i] == positiveClass:   #Predicted positive
                    if forest.testingData.instances[i][forest.testingData.className] == positiveClass:    #Supposed to be positive
                        truePositives += 1
                    else:    #Supposed to be negative
                        falsePositives +=1
                else:   #Predicted negative
                    if forest.testingData.instances[i][forest.testingData.className] != positiveClass:    #Supposed to be negative
                        trueNegatives +=1
                    else:    #Supposed to be positive
                        falseNegatives += 1

            iterationPerformances.append((truePositives+trueNegatives)/len(predictions))    #Right guesses
            iterationPrecisions.append(truePositives / (truePositives + falsePositives))    #Right guesses from instances guessed positive
            iterationRecalls.append(truePositives / (truePositives + falseNegatives))   #Right guesses from instances that were supposed to be positive

        #Calculates average performance, recall and precision for this iteration
        iterationAvgPerformance = sum(iterationPerformances)/len(iterationPerformances)
        iterationAvgPrecision = sum(iterationPrecisions)/len(iterationPrecisions)
        iterationAvgRecall = sum(iterationRecalls)/len(iterationRecalls)

        print("----- Forest {} -----".format(iteration))
        forest.evaluateTreesPerformance()
        print("Forest performance: {:.2f}% of guesses (precision: {:.2f}% / recall: {:.2f}%)".format(iterationAvgPerformance*100, iterationAvgPrecision*100, iterationAvgRecall*100))

        allPerformances.append(iterationAvgPerformance)   #Adds this iteration's performance to the list
        allPrecisions.append(iterationAvgPrecision)   #Adds this iteration's precision to the list
        allRecalls.append(iterationAvgRecall)   #Adds this iteration's recall to the list

    #Calculates averages for all iterations
    avgPerformance = sum(allPerformances)/len(allPerformances)
    avgPrecision = sum(allPrecisions)/len(allPrecisions)
    avgRecall = sum(allRecalls)/len(allRecalls)
    #Calculates F1-Measure for all iterations
    f1 = (2*avgPrecision*avgRecall) / (avgPrecision+avgRecall)

    print("----------")
    print("Model's average performance: {:.2f}% (precision: {:.2f}% / recall: {:.2f}%)".format(avgPerformance*100, avgPrecision*100, avgRecall*100))
    print("F1-measure from averages: {:.2f}%".format(f1*100))
    print("----------")


# -------------------------------------------------------------------
# Credit g
filename = '../data/credit-g.csv'
className = 'class'
data = Data(className, numeric=['duration', 'credit_amount', 'installment_commitment', 
                                'residence_since', 'age', 'existing_credits', 
                                'num_dependents'])
data.parseFromFile(filename, delimiter=',', quotechar='"')

# Print instance info for debug
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
