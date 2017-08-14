import numpy as np
import pandas as pd
import seaborn as sns
from features import FeatureEngineering
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

FE = FeatureEngineering()

def engineer_features(df):
    print("Engineering Features...")
    ndf = df.copy()
    ndf['CabinKnown'] = FE.cabinKnown(ndf)
    ndf['Title'] = FE.title(ndf)
    ndf['FamilySize'] = FE.familySize(ndf)
    ndf['IsMinor'] = FE.isMinor(ndf, 14)
    print(''.join(['\t' + ln for ln in FE.getSummary().splitlines(True)]))
    return ndf


def fill_missing(df):
    print("Filling missing values ...")
    ndf = df.copy()
    # Fill missing Fare with median of the corresponding Passenger Class
    missing_fares = ndf[ndf['Fare'].isnull()].index.tolist()

    for fare in missing_fares:
        pclass = ndf.iloc[fare]['Pclass']
        ndf.set_value(fare, 'Fare', ndf[ndf['Pclass'] == pclass]['Fare'].mean())

    print('\tFare:\t\t\tMean of Corresponding Pclass')

    # Fill missing locations with most common
    missing_embarks = ndf[ndf['Embarked'].isnull()].index.tolist()
    mcl = ndf['Embarked'].value_counts().idxmax()
    for eb in missing_embarks:
        ndf.set_value(eb, 'Embarked', mcl)

    print('\tEmbarked:\t\tMode of Embarked')
    return ndf


def transform_features(df):
    print("Transforming features...")
    ndf = df.copy()
    ndf['Fare'] = df["Fare"].map(lambda i: np.log(i) if i > 0 else 0)
    print("\tFare:\t\t\tlog")
    return ndf


def prep_data_for_tree_model(df):
    print("Prepping data for tree model training... no dummies, all cat to codes")
    ndf = pd.DataFrame(df['PassengerId'])
    # Pclass (ordered cat)
    ndf['Pclass'] = pd.to_numeric(df['Pclass'])
    # Sex (binary cat)
    ndf['IsMale'] = df['Sex'].cat.codes
    # Fare (num)
    ndf['Fare'] = df['Fare']
    # Embarked (unordered multilevel cat)
    ndf['Embarked'] = df['Embarked'].cat.codes
    # CabinKnown (binary cat)
    ndf['CabinKnown'] = df['CabinKnown'].cat.codes
    # Title (unordered multilevel cat)
    ndf['Title'] = df['Title'].cat.codes
    # FamilySize (ordered cat)
    ndf['FamilySize'] = df['FamilySize'].cat.codes
    # isMinor (binary cat)
    ndf['IsMinor'] = df['IsMinor'].cat.codes
    return ndf


def prep_data_for_sv_model(df):
    print("Prepping data for scale variant model training...")
    ndf = pd.DataFrame(df['PassengerId'])
    # Pclass (ordered cat)
    ndf = pd.concat([ndf, pd.get_dummies(df['Pclass'], prefix='Pclass')], axis=1)
    # Sex (binary cat)
    ndf['IsMale'] = df['Sex'].cat.codes
    # Fare (num)
    ndf['Fare'] = df['Fare']
    # Embarked (unordered multilevel cat)
    ndf = pd.concat([ndf, pd.get_dummies(df['Embarked'], prefix='Embarked')], axis=1)
    # CabinKnown (binary cat)
    ndf['CabinKnown'] = df['CabinKnown'].cat.codes
    # Title (unordered multilevel cat)
    ndf = pd.concat([ndf, pd.get_dummies(df['Title'], prefix='Title')], axis=1)
    # FamilySize (ordered multilevel cat)
    ndf = pd.concat([ndf, pd.get_dummies(df['FamilySize'], prefix='FamilySize')], axis=1)
    # isMinor (binary cat)
    ndf['IsMinor'] = df['IsMinor'].cat.codes
    return ndf

def coerce_types(df):
    ndf = df.copy()
    ndf.Pclass = ndf.Pclass.astype("category", categories=[1, 2, 3], ordered=True)
    ndf.Sex = ndf.Sex.astype("category")
    ndf.Embarked = ndf.Embarked.astype("category")
    return ndf


def naSummary(df):
    return df.isnull().sum()


if __name__ == "__main__":
    # start the pipeline
    train = pd.read_csv('../input/train_pp.csv')
    test = pd.read_csv('../input/test_pp.csv')

    combine = pd.concat([train.drop('Survived', 1), test])
    combine.reset_index(inplace=True, drop=True) 
    combine = coerce_types(combine)

    combine = engineer_features(combine)
    combine = fill_missing(combine)

    combine = transform_features(combine)
    combine = prep_data_for_model(combine)

    x_train = combine[:len(train)]
    x_test = combine[len(train):]
    y_train = train['Survived']
















