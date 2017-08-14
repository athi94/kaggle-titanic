import numpy as np
import pandas as pd

class FeatureEngineering():
    def __init__(self):
        self._cabinKnown = False
        self._title = False
        self._familySize = False
        self._isMinor = False
        self._isMinorThresh = 0

    def _familyCategorise(self, s):
        if s>= 4:
            return 'large'
        if s == 0:
            return 'alone'
        if s > 0 and s < 4:
            return 'normal'
    

    def cabinKnown(self, df):
        self._cabinKnown = True
        return pd.Categorical(df['Cabin'].isnull() == False)


    def title(self, df):
        self._title = True
        titles = df['Name'].str.split(", ", expand=True)[1].str.split(".", expand=True)[0]

        mr_alias = ['Don', 'Rev', 'Dr', 'Major', 'Sir', 'Col', 'Capt', 'Jonkheer']
        miss_alias = ['Mlle', 'Ms']
        mrs_alias = ['Mme', 'Lady', 'the Countess']

        titles[titles.isin(mr_alias)] = 'Mr'
        titles[titles.isin(miss_alias)] = 'Miss'
        titles[titles.isin(mrs_alias)] = 'Mrs'
        return titles.astype('category')


    def familySize(self, df):
        self._familySize = True
        family = df['Parch'] + df['SibSp']
        return pd.Categorical(list(map(self._familyCategorise, family)), ordered=True)


    def isMinor(self, df, threshold):
        # Try thresholds 14 and 9 to start off with, aim is to balanced 
        # maximising difference between groups while also capturing 
        # most information possible
        self._isMinor = True
        self._isMinorThresh = threshold
        return pd.Categorical(np.digitize(df['Age'], [threshold, 0]))


    def getSummary(self):
        s = "cabinKnown:\t\t{}\ntitle:\t\t\t{}\nfamilySize:\t\t{}\nisMinor (age < {}):\t{}".format(
            self._cabinKnown, self._title, self._familySize, self._isMinorThresh, self._isMinor)
        
        return s
