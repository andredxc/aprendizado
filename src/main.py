#!/usr/bin/python3

import csv
from math import log


class DecisionTree(object):

    root = None
    data = None

    def __init__(self, data):
        self.data = data

    def create(self):

        self.root = self.generateNode(self.data)

        # for key in splitDic.keys():

    def generateNode(self, data):
        """
        Recursive function which creates the DecisionNode for a given data along with its 
        children nodes.
        """
        # TODO: test this
        curNode = DecisionNode(data)
        curNode.findAttribute()
        splitDic = curNode.splitData()
        for keyName in splitDic:
            if not splitDic[keyName].uniformClass():
                curNode.children[keyName] = generateNode(splitDic[keyName])

        return curNode


class DecisionNode(object):

    data = None
    attribute = None
    children = {}

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "<DecisionNode {}>".format(self.name)

    def attributeInfo(self, keyName):

        m = self.data.summarize(keyName)
        n = len(self.data.instances)
        info = 0

        # Calculate each part of the sum
        for col in range(1, len(m[0])):
            # Each attribute value
            sum = 0
            for row in range(1, len(m)):
                # Each row
                x = float(m[row][col])/float(m[-1][col])
                if x != 0:
                    sum = sum - x*log(x, 2)

            info += (m[-1][col]/n)*sum

        return info

    def classInfo(self):

        n = len(self.data.instances)
        sum = 0
        classDic = {}
        className = self.data.className
        # Count the occurances of all class values
        for entry in self.data.instances:
            if entry[className] not in classDic.keys():
                # Class value not yet added
                classDic[entry[className]] = 1
            else:
                num = classDic[entry[className]]
                classDic[entry[className]] = num + 1

        # Calculate information
        for key in classDic.keys():
            x = float(classDic[key])/float(n)
            sum -= x*log(x, 2)

        return sum

    def infoGain(self, keyName):

        infoGain = self.classInfo() - self.attributeInfo(keyName)
        return infoGain

    def findAttribute(self):
        """
        Set the attribute variable to whichever attribute provides the most
        information and initializes the children dictionary.
        """
        # Find the attribute with the highest information
        highest = ("", 0)
        for attr in self.data.attributes:
            infoGain = self.infoGain(attr)
            if infoGain > highest[1]:
                # Found better attribute
                highest = (attr, infoGain)

        self.attribute = highest[0]

        # Initialize the children dictionary
        for value in self.data.listAttributeValues(self.attribute):
            self.children[value] = None

        print("Attribute for DecisionNode: {0} with {1:.3f} bits".\
            format(highest[0], highest[1]))
        
        print("Children dic created: {}".format(self.children))

    def splitData(self):
        """
        Splits the dataset amongst the children nodes according to the attribute
        previously set.
        """
        # TODO: return Data objects instead of dic lists
        if not self.attribute:
            raise ValueError("Attribute value is not yet set")

        # Split dataset
        splitDic = {}
        for entry in self.data.instances:
            # TODO: remove the current node's attribute from chilren datasets
            newEntry = entry.copy()
            del newEntry[self.attribute]
            if entry[self.attribute] in splitDic.keys():
                # Value had already been found
                splitDic[entry[self.attribute]].append(newEntry)
            else:
                # Value found for the first time
                splitDic[entry[self.attribute]] = [newEntry]

        for key in splitDic.keys():
            print("Dictionaries for key: {}".format(key))
            [print(x) for x in splitDic[key]]

        return splitDic

    def process(self):

        self.findAttribute()

class Data(object):

    keys = []
    instances = []
    attributes = []
    className = ""

    def __init__(self, className):
        self.className = className

    def addInstance(self, newInstance):

        if len(self.instances) == 0:
            # First instance
            [self.keys.append(x) for x in newInstance.keys()]

            for x in newInstance.keys():
                if x != self.className:
                    self.attributes.append(x)

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
        #  ['Verdadeiro', 0, 0, 0],
        #  [0, sum, sum, sums]]

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
                # print("Entry: {} - {}".format(entry[attr], entry[self.className]))
                # print("Incrementing position: [{}, {}]".format(rowInd, colInd))
                m[rowInd][colInd] += 1
                # print("New matrix: {}".format(m))
            else:
                raise ValueError("Error finding position in matrix: col: {}, row: {}".format(colInd, rowInd))

        # Calculate the number of occurances for each value
        sumRow = [0]*len(m[0])
        for row in range(1, len(m)):
            for col in range(1, len(m[0])):
                sumRow[col] += m[row][col]

        m.append(sumRow)

        # print('Resulting matrix:')
        # print(m)

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

    def uniformClass(self):
        """
        Checks if there is more than one class value in the dataset.
        :returns: True if data is uniform, False otherwise
        """
        value = self.instances[self.className]
        for entry in self.instances:
            if entry[self.className] != value:
                return False

        return False

    def copyWithoutAttribute(self, attrName):
        """
        Copies the Data insntance without the dic entries for a specific attribute name.
        """
        # TODO: test this
        copy = self.copy()
        for entry in copy.instances:
            del entry[attrName]



# ---------------------------------------

filename = '../data/dadosBenchmark_validacaoAlgoritmoAD.csv'
className = 'Joga'
data = Data(className)

data.parseFromFile(filename)
node = DecisionNode(data)

node.findAttribute()
# d = node.splitData()


# data.summarize('Tempo')
# tree.attributeInfo('Tempo')


# print(tree.classInfo())

# print("Dictionary keys: {}".format(data.keys))
# print(data.summarize('Tempo'))
