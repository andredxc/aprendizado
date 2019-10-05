#!/usr/bin/python3
from data import Data
from decisionTree import DecisionNode, DecisionTree, RandomForest

def evaluatePerformance(data):
    #Splits instances into folds
    folds = data.generateStratifiedFolds(3)

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
        positiveClasses = ["Sim"]   #MUST BE SET MANUALLY FOR EACH DATASET
        negativeClasses = ["Nao"]   #MUST BE SET MANUALLY FOR EACH DATASET
        truePositives = 0
        falsePositives = 0
        trueNegatives = 0
        falseNegatives = 0
        for i in range(len(predictions)):
            if predictions[i] in positiveClasses:   #Predicted positive
                if forest.testingData.instances[i][forest.testingData.className] in positiveClasses:    #Supposed to be positive
                    truePositives += 1
                if forest.testingData.instances[i][forest.testingData.className] in negativeClasses:    #Supposed to be negative
                    falsePositives +=1
            if predictions[i] in negativeClasses:   #Predicted negative
                if forest.testingData.instances[i][forest.testingData.className] in negativeClasses:    #Supposed to be negative
                    trueNegatives +=1
                if forest.testingData.instances[i][forest.testingData.className] in positiveClasses:    #Supposed to be positive
                    falseNegatives += 1

        performance = (truePositives+trueNegatives)/len(predictions)    #Right guesses
        precision = truePositives / (truePositives + falsePositives)    #Right guesses from instances guessed positive
        recall = truePositives / (truePositives + falseNegatives)   #Right guesses from instances that were supposed to be positive


        print("----- Forest {} -----".format(iteration))
        print(predictions)
        for instance in forest.testingData.instances:
            print(instance)
        print("TP: {}, FP: {}, TN: {}, FN: {}".format(truePositives, falsePositives, trueNegatives, falseNegatives))
        forest.evaluateTreesPerformance()
        print("Forest performance: {:.2f}% of guesses (precision: {:.2f}% / recall: {:.2f}%)".format(performance*100, precision*100, recall*100))

        allPerformances.append(performance)   #Adds this iteration's performance to the list
        allPrecisions.append(precision)   #Adds this iteration's precision to the list
        allRecalls.append(recall)   #Adds this iteration's recall to the list

    avgPerformance = sum(allPerformances)/len(allPerformances)
    avgPrecision = sum(allPrecisions)/len(allPrecisions)
    avgRecall = sum(allRecalls)/len(allRecalls)

    f1 = (2*avgPrecision*avgRecall) / (avgPrecision+avgRecall)

    print("----------")
    print("Model's average performance: {:.2f}% (precision: {:.2f}% / recall: {:.2f}%)".format(avgPerformance*100, avgPrecision*100, avgRecall*100))
    print("F1-measure from averages: {:.2f}%".format(f1*100))
    print("----------")


# -------------------------------------------------------------------
filename = '../data/dadosBenchmark_validacaoAlgoritmoAD.csv'
className = 'Joga'
data = Data(className)
data.parseFromFile(filename)

evaluatePerformance(data)
# forest = RandomForest(data)
# forest.generateForest(5)
# forest.evaluateTreesPerformance()


