from math import log, sqrt
from random import shuffle


class DecisionTree(object):

    def __init__(self, data, m=0):
        """
        :param data: dataset used by the root node
        :param m: size of the sample of features considered for the node
                  attribute
        """
        self.data = data
        self.root = None
        self.m = m

    def train(self):

        self.root = self.generateNode(self.data)

    def generateNode(self, data):
        """
        Recursive function which creates the DecisionNode for a given data along with its
        children nodes.
        """
        curNode = DecisionNode(data, self.m)
        curNode.evaluate()
        if len(curNode.children) == 0:
            # Leaf node
            return curNode
        else:
            # Split data for children nodes
            splitDic = curNode.splitData()
            for keyName in splitDic:
                print("Size of attribute list: {}".format(len(splitDic[keyName].instances)))
                curNode.children[keyName] = self.generateNode(splitDic[keyName])

            return curNode

    def print(self, valName='', indent=0, start=None):

        if not start:
            start = self.root

        # Recursively print nodes
        s = "   "*indent
        if len(start.children) == 0:
            print("{}- {} -> {}".format(s, valName, start.guess))
        else:
            print("{}- {} -> {}".format(s, valName, start.attribute))

        for key in start.children:
            if start.children[key]:
                self.print(key, indent+1, start.children[key])

    def classify(self, instance, node=None):
        """
        Recursively navigates the tree to classify a new instance
        :returns: predicted class name for the given instance
        """
        if not self.root:
            raise AttributeError("The decision tree has not yet been trained")

        if not node:
            node = self.root

        if len(node.children) == 0:
            # Leaf node
            return node.guess
        else:
            nextNode = node.children[instance[node.attribute]]
            return self.classify(instance, node=nextNode)


class DecisionNode(object):

    def __init__(self, data, m=0):
        """
        :param data: dataset used by the node
        :param m: size of the sample of features considered for the node
                  attribute
        """
        # dataset
        self.data = data
        # attribute selected as a division criteria for this node
        self.attribute = None
        # dic with values as keys and DecisionNodes as values
        self.children = {}
        # For a leaf node, value guessed as output
        self.guess = None
        # Number of random features to be considered when splitting the node
        if m == 0:
            self.m = int(sqrt(len(self.data.attributes)))
        else:
            self.m = m if m <= len(self.data.instances) else len(self.data.instances)

        print("Node initialized with m = {} and {} instances".format(self.m, len(self.data.instances)))

    def __repr__(self):
        return "<DecisionNode {}>".format(self.attribute)

    def attributeInfo(self, attrName):
        """
        Calculates the information value for a given attribute.
        """
        m = self.data.summarize(attrName)
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
        """
        Calculates the class information value.
        """
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

    def infoGain(self, attrName):
        """
        Calculates the information gain for a attribute, which is defined as the class
        information - attribute information.
        """
        infoGain = self.classInfo() - self.attributeInfo(attrName)
        return infoGain

    def evaluate(self):
        """
        Set the attribute variable to whichever attribute provides the most
        information and initializes the children dictionary.
        """
        if self.data.uniformClass():
            # Node is a leaf
            self.guess = self.data.instances[0][self.data.className]
            # print("Leaf node with guess: {}".format(self.guess))
        else:
            # Use a sample of m random attributes
            attrList = self.data.attributes
            shuffle(attrList)
            if len(attrList) == 0:
                raise SystemError("Attribute list is empty")
            # print("Selecting attribute amongst: {}".format(attrList[0:self.m]))
            # Find the attribute with the highest amount of information
            highest = ("", 0)
            for attr in attrList[0:self.m]:
                infoGain = self.infoGain(attr)
                if infoGain > highest[1] or highest[0] == "":
                    # Found better attribute or initialzes
                    highest = (attr, infoGain)

            self.attribute = highest[0]
            # Initialize the children dictionary
            for value in self.data.listAttributeValues(self.attribute):
                self.children[value] = None

            print("Attribute for DecisionNode: {0} with {1:.3f} bits".\
                format(highest[0], highest[1]))

    def splitData(self):
        """
        Splits the dataset amongst the children nodes according to the attribute
        previously set.
        """
        if not self.attribute:
            raise ValueError("Attribute value is not yet set")

        # Split dataset
        splitDic = self.data.split(self.attribute)
        return splitDic
