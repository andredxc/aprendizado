#!/usr/bin/python3
from data import Data
from decisionTree import DecisionNode, DecisionTree, RandomForest
import examples
import sys

def evaluatePerformance(data, nForests=10):
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
        forest.generateForest(10)

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
if len(sys.argv) == 1:  #No arguments
    #Run sample code
    print("----- No file supplied, running sample code! -----")
    data = examples.setupSpambase()
    evaluatePerformance(data, 10)
elif len(sys.argv) == 4:    #Three arguments: training dataset, target class and numeric attributes
    #Run performance evaluation on the supplied dataset
    print("----- Running performance evaluation with the supplied dataset! -----")
    numericAttributes = sys.argv[3].split(',')  #Splits numeric attributes into a list

    data = Data(sys.argv[2], numericAttributes)
    data.parseFromFile(sys.argv[1], delimiter=',', quotechar='"')   #Parses data from supplied dataset

    evaluatePerformance(data)
elif len(sys.argv) == 5:    #Four arguments: training dataset, target class, numeric attributs, testing dataset
    #Trains the model with the training dataset and then classifies the instances in the testing dataset
    print("----- Training model and classifiying supplied instances! -----")
    numericAttributes = sys.argv[3].split(',')  #Splits numeric attributes into a list

    trainingData = Data(sys.argv[2], numericAttributes)
    trainingData.parseFromFile(sys.argv[1], delimiter=',', quotechar='"')   #Parses training data
    testingData = Data(sys.argv[2], numericAttributes)
    testingData.parseFromFile(sys.argv[4], delimiter=',', quotechar='"')    #Parses testing data

    forest = RandomForest(trainingData, testingData)
    forest.generateForest() #Trains the model

    #Classifies training data
    for instance in forest.testingData.instances:
        print(forest.classify(instance))
else:
    print("Invalid arguments! Please use one of the options below:")
    print("")
    print('"python main.py"')
    print("    Providing no arguments will run sample code")
    print('"python main.py <dataset> <target class> <comma separated list of numeric attributes>"')
    print("    Providing a dataset, target class and numeric attributes will run performance evaluation on the specified dataset")
    print('"python main.py <training dataset> <target class> <comma separated list of numeric attributes> <testing dataset>"')
    print("    Providing a dataset, target class, numeric attributes and testing dataset will train the model and classify the instances in the testing dataset")


# Print instance info for debug
# for key in data.instances[0]:
#     if key == data.className:
#         print("\t{}: {} (CLASS)".format(key, data.instances[0][key]))
#     elif data.isNumeric(key):
#         print("{}: {} (numeric)".format(key, data.instances[0][key]))
#     else:
#         print("{}: {} (categoric)".format(key, data.instances[0][key]))
