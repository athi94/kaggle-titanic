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
        age = age[:-1]
    
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


with open('../input/train_plus.csv', 'w') as train_pluf_f:
    train_plus = csv.DictWriter(train_pluf_f, newTrain[0].keys())

    train_plus.writeheader()
    train_plus.writerows(newTrain)





