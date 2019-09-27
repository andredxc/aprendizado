#!/usr/bin/python3

import csv
from math import log


class DecisionTree(object):

    data = None

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "<DecisionTree {}>".format(self.name)

    def calculateInfo(self, keyName=""):

        m = self.data.summarize('Tempo')

        print(m)


        # if len(keyName) == 0:
        #     # Calculate entropy for the class
        #     keyName = self.data.getClassName()
        #
        # dic = self.data.summarize(keyName)
        # info = 0
        # total = len(self.data.instances)
        # for value in dic.values():
        #     info -= value/total*log(value/total, 2)
        #
        # print(dic)
        # print("Info for '{}': {}".format(keyName, info))
        # return info


class Data(object):

    keys = []
    instances = []

    def __init__(self):
        pass

    def addInstance(self, newInstance):

        if len(self.instances) == 0:
            # First instance
            [self.keys.append(x) for x in newInstance.keys()]

        elif self.instances[-1].keys() != newInstance.keys():
            # Validate keys
            raise ValueError("Keys for new instance '{}' don`t match previous instances".format(newInstance))

        self.instances.append(newInstance)

    def summarize(self, attr, class_restriction=False):

        if attr not in self.keys:
            raise ValueError("Attr '{}' does not exist in the dictionary".format(attr))

        # dic = {}    # KEYS: attribute values. VALUES: number of occurances
        # l = []
        # attrValues = []

        attrDic = {}
        classDic = {}
        colFound = False
        rowFound = False

        # Matrix format
        # [[0, 'Ensolarado', 'Nublado', 'Chuvoso'], 
        #  ['Falso', 0, 0, 0], 
        #  ['Verdadeiro', 0, 0, 0]]


        # Initialize the matrix
        m = []
        m.append(self.listAttributeValues(attr))
        numValues = len(self.listAttributeValues(attr))
        m[0].insert(0, 0)
        for val in self.listClassValues():
            newRow = [0]*numValues
            newRow.insert(0, val)
            m.append(newRow)

        # Summarize every instance
        className = self.getClassName()
        for entry in self.instances:
            # Calculate matrix positions
            colInd = rowInd = -1
            # Iterate over the columns (possible values)
            for col in range(1, len(m[0])):
                if entry[attr] == m[0][col]:
                    # Found column with the same attribute value
                    colInd = col

            # Iterate over the rows (classes)
            for row in range(1, len(m)):
                if m[row][0] == entry[className]:
                    # Found row
                    rowInd = row

            if rowInd >= 0 and colInd >= 0:
                # Position was Found
                print("Entry: {} - {}".format(entry[attr], entry[className]))
                # print("Incrementing position: [{}, {}]".format(rowInd, colInd))
                m[rowInd][colInd] += 1
                # print("New matrix: {}".format(m))
            else:
                raise ValueError("Error finding position in matrix: col: {}, row: {}".format(colInd, rowInd))

        print('Resulting matrix:')
        print(m)

        return m

    def listAttributeValues(self, attr):
        """
        Returns a list contaning all the possible value labels for a given
        attribute.
        """
        valueList = []
        for row in self.instances:
            if row[attr] not in valueList:
                valueList.append(row[attr])
        return valueList

    def listClassValues(self):
        """
        Returns a list containing all the possible class values
        """
        classList = []
        className = self.getClassName()
        for row in self.instances:
            if row[className] not in classList:
                classList.append(row[className])
        return classList

    def getClassName(self):
        return self.keys[-1] if len(self.keys) > 1 else None


def parseFile(filename):
    """
    :returns: Data
    """

    reader = csv.DictReader(open(filename, mode='r'), delimiter=';')
    dataset = Data()

    for row in reader:
        dataset.addInstance(row)

    return dataset


data = parseFile('../data/dadosBenchmark_validacaoAlgoritmoAD.csv')
tree = DecisionTree(data)
# data.summarize('Tempo')
tree.calculateInfo('Tempo')

# print("Dictionary keys: {}".format(data.keys))
# print(data.summarize('Tempo'))
