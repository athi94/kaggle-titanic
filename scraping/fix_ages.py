import csv
import re
import pprint
import pandas as pd
from fuzzywuzzy import fuzz

titanica_db = []
with open('output.csv', 'r+') as titanica_f:
    titanica = csv.DictReader(titanica_f)

    for passenger in titanica:
        titanica_db.append(passenger)


def sanitizeName(name):
    return name.lower().replace(".", "").replace(",", "")


def sanitizeAge(age):
    if age[-1] == 'm':
        age = '1'
    
    return age


def getBestMatch(name):
    fuzz_scores = list(map(lambda x: fuzz.ratio(sanitizeName(name), sanitizeName(x['Name'])), titanica_db))
    return titanica_db[fuzz_scores.index(max(fuzz_scores))]


def missingAge(passenger):
    if passenger['Age'] == "":
        return True

    return False

newTrain = []
with open('../input/train.csv', 'r+') as train:
    train_rd = csv.DictReader(train)

    for passenger in train_rd:
        if missingAge(passenger):
            passenger['Age'] = sanitizeAge(getBestMatch(passenger['Name'])['Age'])

        newTrain.append(passenger)


with open('../input/train_pp.csv', 'w') as train_pluf_f:
    train_plus = csv.DictWriter(train_pluf_f, newTrain[0].keys())

    train_plus.writeheader()
    train_plus.writerows(newTrain)


newTest = []
with open('../input/test.csv', 'r+') as test:
    test_rd = csv.DictReader(test)

    for passenger in test_rd:
        if missingAge(passenger):
            passenger['Age'] = sanitizeAge(getBestMatch(passenger['Name'])['Age'])

        newTest.append(passenger)


with open('../input/test_pp.csv', 'w') as test_pluf_f:
    test_plus = csv.DictWriter(test_pluf_f, newTest[0].keys())

    test_plus.writeheader()
    test_plus.writerows(newTest)





