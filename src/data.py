import csv
import random
from math import floor


class Data(object):

    def __init__(self, className, numeric=[]):
        self.className = className
        self.keys = []
        self.instances = []
        self.attributes = []
        self.numericAttr = numeric

    def __repr__(self):
        return "<Data {} -> {}>".format(self.attributes, self.className)

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
        """
        Returns a matrix which has formatted useful data used to calculate the amount of 
        information for an attribute.
        """
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
        #  [0, sum, sum, sum]]

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
            # row is an OrderedDict by default
            self.addInstance(dict(row))

    def uniformClass(self):
        """
        Checks if there is more than one class value in the dataset.
        :returns: True if data is uniform, False otherwise
        """
        value = self.instances[0][self.className]
        for entry in self.instances:
            if entry[self.className] != value:
                return False

        return True

    def split(self, attrName):
        """
        Splits the data into however Data objecst is dictated by the number of values for 
        the specified attribute name. And deletes all the values correponding to the 
        specified attribute from the returned instances.
        :returns: dictionary containing the values as keys and Data instances as values
        """
        splitDic = {}
        for entry in self.instances:
            newEntry = entry.copy()
            del newEntry[attrName]
            if entry[attrName] not in splitDic.keys():
                # Create a new Data instance
                newData = Data(self.className)
                splitDic[entry[attrName]] = newData

            splitDic[entry[attrName]].addInstance(newEntry)

        return splitDic

    def generateFolds(self, k=1, discardExtras=False):
        '''
        Generates 'k' sets of instances without repetition.
        WARNING: setting 'discardExtras' to False will cause folds to have different sizes if the number of instances isn't divisible by 'k'.
        Returns the list of folds.
        '''

        instancesCopy = self.instances.copy()
        folds = []
        for i in range(k):
            folds.append([])    #New fold

            #Adds 'instances/k' (rounded down) random instances to each fold
            for j in range(floor(len(self.instances)/k)):
                folds[i].append(instancesCopy.pop(random.randint(0, len(instancesCopy)-1)))

        #Evenly distributes the remaining instances. Will cause some folds to have 1 more instance than others if the number of instances isn't divisible by 'k'.
        if discardExtras == False:
            while len(instancesCopy) != 0:
                for i in range(k):
                    if(len(instancesCopy) != 0):
                        folds[i].append(instancesCopy.pop(random.randint(0, len(instancesCopy)-1)))    

        return folds

    def generateStratifiedFolds(self, k=1, discardExtras=False):
        '''
        Generates 'k' stratified sets of instances without repetition.
        WARNING: setting 'discardExtras' to False will cause folds to have different sizes if the number of instances isn't divisible by 'k'.
        Returns the list of folds.
        '''

        classValueDistribution = {}
        for value in self.listClassValues(): #For each possible class value
            matchingInstances = [instance for instance in self.instances if instance[self.className] == value] #Instances that have the matching value
            classValueDistribution[value] = len(matchingInstances)/len(self.instances)  #Percentage of instances that have this value

        instancesCopy = self.instances.copy()   #Pool of instances that haven't been picked
        folds = []
        for i in range(k):
            folds.append([])    #New fold

            for value in self.listClassValues(): #For each possible class value
                matchingInstances = [instance for instance in instancesCopy if instance[self.className] == value] #Instances that have the matching value

                #Adds matching instances to the fold keeping the same value proportion as the full data set
                for j in range(floor((len(self.instances)/k) * classValueDistribution[value])):
                    selectedInstance = matchingInstances.pop(random.randint(0, len(matchingInstances)-1))   #Selects random matching instance
                    folds[i].append(selectedInstance)   #Adds selected instance to the fold
                    instancesCopy.remove(selectedInstance)  #Removes selected instance from the pool

        #Evenly distributes the remaining instances. Will cause some folds to have 1 more instance than others if the number of instances isn't divisible by 'k'.
        if discardExtras == False:
            while len(instancesCopy) != 0:
                for i in range(k):
                    if(len(instancesCopy) != 0):
                        folds[i].append(instancesCopy.pop(random.randint(0, len(instancesCopy)-1)))

        return folds

    def generateBootstraps(self, k=1):
        '''
        Randomly generates 'k' sets of instances with repetition for the training set and sets of instances that aren't in the training set for the testing set.
        Returns the list of bootstraps.
        '''
        bootstraps = []
        for i in range(k):
            bootstraps.append( ([], []) )   #Adds a new bootstrap. Each bootstrap is a tuple with a list of training instances (index 0) and a list of testing instances (index 1)

            for j in range(len(self.instances)):    #Bootstraps have the same number of instances as the original data set
                bootstraps[i][0].append(self.instances[random.randint(0, len(self.instances)-1)]) #Adds a random instance to the current's bootstrap training list

            for j in range(len(self.instances)): #Goes through every instance again
                if self.instances[j] not in bootstraps[i][0]:    #Checks for instances that weren't picked for the training list
                    bootstraps[i][1].append(self.instances[j])   #Adds the instance to the testing list

        return bootstraps

    def generateStratifiedBootstraps(self, k=1):
        '''
        Generates 'k' stratfied sets of instances with repetition for the training set and sets of instances that aren't in the training set for the testing set.
        Returns the list of bootstraps. Each bootstrap is a tuple with a list of training instances (index 0) and a list of testing instances (index 1).
        '''
        bootstraps = []
        for i in range(k):  #For each bootstrap
            bootstraps.append( ([], []) )   #Adds a new bootstrap

            for value in self.listClassValues(): #For each possible class value
                matchingInstances = [instance for instance in self.instances if instance[self.className] == value] #Instances that have the matching value

                #Add to the bootstrap the same number of instances with that value that are in the data set
                for j in range(len(matchingInstances)):
                    bootstraps[i][0].append(matchingInstances[random.randint(0, len(matchingInstances)-1)])    #Adds a random instance from the matching instances to the training list

            for j in range(len(self.instances)):    #Goes through every instance again
                if self.instances[j] not in bootstraps[i][0]:   #Checks for instances that weren't picked for the training list
                    bootstraps[i][1].append(self.instances[j])  #Adds the instance to the testing list

        return bootstraps
