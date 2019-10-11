#!/usr/bin/python3
from data import Data
from decisionTree import DecisionNode, DecisionTree, RandomForest
import examples
import sys
import logging

def evaluatePerformance(data, nForests=10, nTrees=10):
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
        forest.generateForest(nTrees)

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

        # print("----- Forest {} -----".format(iteration))
        forest.evaluateTreesPerformance()
        # print("Forest performance: {:.2f}% of guesses (precision: {:.2f}% / recall: {:.2f}%)".format(iterationAvgPerformance*100, iterationAvgPrecision*100, iterationAvgRecall*100))

        allPerformances.append(iterationAvgPerformance)   #Adds this iteration's performance to the list
        allPrecisions.append(iterationAvgPrecision)   #Adds this iteration's precision to the list
        allRecalls.append(iterationAvgRecall)   #Adds this iteration's recall to the list

    #Calculates averages for all iterations
    avgPerformance = sum(allPerformances)/len(allPerformances)
    avgPrecision = sum(allPrecisions)/len(allPrecisions)
    avgRecall = sum(allRecalls)/len(allRecalls)
    #Calculates F1-Measure for all iterations
    f1 = (2*avgPrecision*avgRecall) / (avgPrecision+avgRecall)

    # print("----------")
    # print("Model's average performance ({} trees): {:.2f}% (precision: {:.2f}% / recall: {:.2f}%)".format(nTrees, avgPerformance*100, avgPrecision*100, avgRecall*100))
    # print("F1-measure from averages: {:.2f}%".format(f1*100))
    # print("----------")
    dic = {'nTrees': nTrees, 'avgPerformance': avgPerformance*100, 
           'avgPrecision': avgPrecision*100, 'avgRecall': avgRecall*100,
           'f1measure': f1*100}
    return dic


logging.basicConfig(filename='out.log', filemode='w', format='%(message)s', level=logging.INFO)
start = 41
maxTrees = 50
numRep = 3
print("------------------------- German Credit Data Set")
logging.info("German Credit Data Set")
data = examples.setupCredit()
for i in range(start, maxTrees+1):
    print("Running with {} trees".format(i))
    sumDic = {}
    for j in range(numRep):
        curDic = evaluatePerformance(data, nForests=10, nTrees=i)
        # Accumulate values in sum dictionary
        for key in curDic:
            if key in sumDic:
                sumDic[key] += curDic[key]  
            else:
                sumDic[key] = curDic[key]

    # Calculate average for each value
    for key in sumDic:
        sumDic[key] = sumDic[key]/numRep

    # Log results
    logging.info(sumDic)