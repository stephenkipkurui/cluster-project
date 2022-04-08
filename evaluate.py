# Import feature engineering libraries
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE, SequentialFeatureSelector
import sklearn.preprocessing
from sklearn.preprocessing import StandardScaler


def select_kbest_feature_engineering(predictors, target):
    
    '''
        This function takes in predictors, and the target variables and the number of 
        features desired and returns the names of the top k selected features based on the SelectKBest class. 
    '''
    num_features = int(input('Enter count of SelectKBest features to return: '))
    
    kbest = SelectKBest(f_regression, k = num_features)
    
    kbest.fit(predictors, target)
    
    return predictors.columns[kbest.get_support()]