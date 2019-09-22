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
        m = []

        # Create dicionaries containing row a column numbers for the matrix
        count = 0
        for x in self.listAttributeValues(attr):
            attrDic[x] = count
            count += 1
        count = 0
        for x in self.listAttributeValues(self.getClassName()):
            classDic[x] = count
            count += 1
        # Initialize the matrix
        m = [[0 for i in range(len(attrDic)+1)] for j in range(len(classDic)+1)]
        # Insert values on the first row and classes on the first column
        for valueName in attrDic.values():
            m[0][attrDic[valueName]] = valueName
        for className in classDic.values():
            m[classDic[className], 0] = className
        # Increment matrix positions according to the values
        for vector in self.instances:

            row = classDic[vector[self.getClassName()]]
            col = attrDic[vector[attr]]
            m[row][col] += 1

            # ------------------- old
            # if vector[attr] not in dic.keys():
            #     # Store a new possible attribute value
            #     dic[vector[attr]] = 1
            # else:
            #     # Increment number of occurances
            #     num = dic[vector[attr]]
            #     dic[vector[attr]] = num + 1

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
