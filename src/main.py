#!/usr/bin/python3
from data import Data
from decisionTree import DecisionNode, DecisionTree, RandomForest
import examples
import sys
# from runSuite import evaluatePerformance


data = examples.setupWine()

dic = {}
for entry in data.instances:
    if entry[data.className] in dic.keys():
        dic[entry[data.className]] += 1
    else:
        dic[entry[data.className]] = 1

print("Dic: {}".format(dic))

exit()

# -------------------------------------------------------------------
if len(sys.argv) == 1:  #No arguments
    #Run sample code
    print("----- No file supplied, running sample code! -----")
    data = examples.setupCredit()
    evaluatePerformance(data, 10, 10)
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
