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


class Data(object):

    keys = []
    instances = []

    def __init__(self, filename, className):

        self.parseFromFile(filename)
        if className not in self.keys:
            raise ValueError("Could not find class '{}' in the dataset".\
                format(className))
        self.className = className

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
                if m[row][0] == entry[self.className]:
                    # Found row
                    rowInd = row

            if rowInd >= 0 and colInd >= 0:
                # Position was Found
                print("Entry: {} - {}".format(entry[attr],
                                              entry[self.className]))
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
        for row in self.instances:
            if row[self.className] not in classList:
                classList.append(row[self.className])
        return classList

    def parseFromFile(self, filename):

        reader = csv.DictReader(open(filename, mode='r'), delimiter=';')
        for row in reader:
            self.addInstance(row)


filename = '../data/dadosBenchmark_validacaoAlgoritmoAD.csv'
className = 'Joga'
data = Data(filename, className)
tree = DecisionTree(data)
# data.summarize('Tempo')
tree.calculateInfo('Tempo')

# print("Dictionary keys: {}".format(data.keys))
# print(data.summarize('Tempo'))
