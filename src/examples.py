from data import Data
from decisionTree import DecisionNode, DecisionTree, RandomForest

# ------------------------------------------------ Credit g (https://www.openml.org/d/31)
def setupCredit():
    filename = '../data/credit-g.csv'
    className = 'class'
    data = Data(className, numeric=['duration', 'credit_amount', 'installment_commitment', 
                                    'residence_since', 'age', 'existing_credits', 
                                    'num_dependents'])
    data.parseFromFile(filename, delimiter=',', quotechar='"')
    return data

# ------------------------------------------------ Spambase (https://www.openml.org/d/44)
def setupSpambase():
    filename = '../data/spambase.csv'
    className = 'class'
    data = Data(className, numeric=['word_freq_make','word_freq_address','word_freq_all',
    'word_freq_3d','word_freq_our','word_freq_over','word_freq_remove',
    'word_freq_internet','word_freq_order','word_freq_mail','word_freq_receive',
    'word_freq_will','word_freq_people','word_freq_report','word_freq_addresses',
    'word_freq_free','word_freq_business','word_freq_email','word_freq_you',
    'word_freq_credit','word_freq_your','word_freq_font','word_freq_000',
    'word_freq_money','word_freq_hp','word_freq_hpl','word_freq_george','word_freq_650',
    'word_freq_lab','word_freq_labs','word_freq_telnet','word_freq_857','word_freq_data',
    'word_freq_415','word_freq_85','word_freq_technology','word_freq_1999',
    'word_freq_parts','word_freq_pm','word_freq_direct','word_freq_cs',
    'word_freq_meeting','word_freq_original','word_freq_project','word_freq_re',
    'word_freq_edu','word_freq_table','word_freq_conference','char_freq_%3B',
    'char_freq_%28','char_freq_%5B','char_freq_%21','char_freq_%24','char_freq_%23',
    'capital_run_length_average','capital_run_length_longest','capital_run_length_total'])
    data.parseFromFile(filename, delimiter=',', quotechar='"')
    return data

# --------------------------------------- Vertebra Column (https://www.openml.org/d/1523)
def setupVertebra():
    filename = '../data/vertebra-column.csv'
    className = 'Class'
    data = Data(className, numeric=['V1','V2','V3','V4','V5','V6'])
    data.parseFromFile(filename, delimiter=',', quotechar='"')
    return data

# ------------------------------------------------- Wine (https://www.openml.org/d/187)
def setupWine():
    filename = '../data/wine.csv'
    className = 'class'
    data = Data(className, numeric=['Alcohol','Malic_acid','Ash','Alcalinity_of_ash',
                                    'Magnesium','Total_phenols','Flavanoids',
                                    'Nonflavanoid_phenols','Proanthocyanins',
                                    'Color_intensity','Hue',
                                    'OD280%2FOD315_of_diluted_wines','Proline'])
    data.parseFromFile(filename, delimiter=',', quotechar='"')
    return data

# -------------------------------------------------- Benchmark
def setupBenchmark():
    filename = '../data/dadosBenchmark_validacaoAlgoritmoAD.csv'
    className = 'Joga'
    data = Data(className)
    data.parseFromFile(filename, delimiter=';', quotechar='"')
    return data
