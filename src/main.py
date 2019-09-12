import csv

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
        
        dic = {}    # KEYS: attribute values. VALUES: number of occurances

        for vector in self.instances:

            if vector[attr] not in dic.keys():
                # Store a new possible attribute value
                dic[vector[attr]] = 1
            else:
                # Increment number of occurances
                num = dic[vector[attr]]
                dic[vector[attr]] = num + 1

        return dic


def parseFile(filename) -> Data:

    reader = csv.DictReader(open(filename, mode='r'), delimiter=';')
    dataset = Data()
    
    for row in reader:
        dataset.addInstance(row)

    return dataset


dataset = parseFile('../data/dadosBenchmark_validacaoAlgoritmoAD.csv')

# for d in dataset.instances:
#     print("Dict: {}".format(d))

print("Dictionary keys: {}".format(dataset.keys))

print(dataset.summarize('Tempo'))
