import pandas as pd
import numpy as np
from zlib import crc32
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn import linear_model
from sklearn import metrics
import pickle


def test_set_check(identifier, test_ratio):
    return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2 ** 32 #Method to split the training and test set
                                                                        # Cannot use random module, as then items
                                                                        # in the test set may end up in the training set


def split_train_test_by_id(data, test_ratio, id_column):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))     # Actually splits into train and test data
    return data.loc[~in_test_set], data.loc[in_test_set]


def display_scores(scores):
    print("scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation", scores.std())                   ### Gave 0 error for decision tree
                                                                 # - need to check for over-fitting


def load_weight_data(file_name):
    return pd.read_csv(file_name) #load csv file into a pandas dataframe


class ConvertToMetricSystem(BaseEstimator, TransformerMixin):
    def __init__(self, add_weight_kg=True):
        self.add_weight_kg = add_weight_kg

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        weight_kg = X[:, Weight_ix] / 2.205
        return np.c_[X, weight_kg]   #Converts data from pounds to kilograms

Weight_ix=2

def Train_ML_Weight_Prediction():

    weight_data = load_weight_data("weight-height.csv")

    attr_adder = ConvertToMetricSystem(add_weight_kg=False)

    weight_data_extra_attribs = attr_adder.transform(weight_data.values) #Adds weight (kg) to program


    new_weight_data = pd.DataFrame(
        {'Gender': weight_data_extra_attribs[:, 0], 'Height': weight_data_extra_attribs[:, 1], #creats pandas dataframe
         'Weight': weight_data_extra_attribs[:, 3]})

    print(new_weight_data.head())





    new_weight_data_with_id = new_weight_data.reset_index()

    train_set, test_set = split_train_test_by_id(new_weight_data_with_id, 0.2, "index")

    new_weight_data["weight_cat"] = pd.cut(new_weight_data["Weight"],
                                           bins=[0,55,70,85,100, np.inf],
                                           labels=[1, 2, 3, 4, 5])


    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42) # Chose 20% of total for test set.
    for train_index, test_index in split.split(new_weight_data, new_weight_data["weight_cat"]):
        strat_train_set = new_weight_data.loc[train_index]
        strat_test_set = new_weight_data.loc[test_index]     #Splits into training and test data

    new_weight_data.drop('Weight', axis=1, inplace=True)

    print(new_weight_data.head())

    new_weight_data_labels = strat_train_set["weight_cat"].copy()  #actual weight category for data in pandas dataframe

    strat_train_set.drop("weight_cat", axis=1, inplace=True)
    strat_train_set.drop("Weight", axis=1, inplace=True)           #Removes weight and weight category from training set
    new_weight_data = strat_train_set

    #new_weight_data.loc[-1]= predict_data1



    ### Problem is here ####


    new_weight_data_cat = new_weight_data[["Gender"]]

    #ordinal_encoder = OrdinalEncoder()

    #new_weight_data_cat_encoded = ordinal_encoder.fit_transform(new_weight_data_cat) #Tried using an ordinal encoder



    cat_encoder = OneHotEncoder()
    new_weight_data_cat_1hot = cat_encoder.fit_transform(new_weight_data_cat) # Ended up using a onehotencoder,
                                                                                #which creates a 'Male' and 'Female'
                                                                                # column

    #print(new_weight_data_cat_1hot)

    #print(new_weight_data)

    new_weight_data_num = new_weight_data.drop("Gender", axis=1) #Getting rid of gender and just keeping numeric
                                                                 #attributes

    #predict_data_num=predict_data.drop("Gender", axis=1)

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="median")),          #Numeric pipeline
        ('std_scaler', StandardScaler()),
    ])

    new_weight_data_num_tr = num_pipeline.fit_transform(new_weight_data_num)


    # print(new_weight_data_num_tr)



    num_attribs = list(new_weight_data_num)
    print(num_attribs, "these are the num attribbs")  #Numeric attributes
    cat_attribs = ["Gender"]

    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),            #Full pipeline for numeric and categorical attributes
        ("cat", OneHotEncoder(), cat_attribs),
    ])


    #print(new_weight_data.head()

    #print(new_weight_data.head())

    new_weight_data_prepared = full_pipeline.fit_transform(new_weight_data)

    #predict_data_prepared=full_pipeline.fit_transform(predict_data)


    print(new_weight_data_prepared)

    # Linear regression

    from sklearn.linear_model import LinearRegression

    #lin_reg=LinearRegression()
    #lin_reg.fit(new_weight_data_prepared, new_weight_data_labels)



    # some_data=new_weight_data.iloc[:5]
    # some_labels=new_weight_data_labels.iloc[:5]
    # some_data_prepared=full_pipeline.transform(some_data)
    # print("Predictions:", lin_reg.predict(some_data_prepared))
    # print("Labels:", list(some_labels))

    ### Check mean squared error ####

    from sklearn.metrics import mean_squared_error

    #new_weight_predictions=lin_reg.predict(new_weight_data_prepared)
    #lin_mse=mean_squared_error(new_weight_data_labels, new_weight_predictions)
    # lin_rmse=np.sqrt(lin_mse)
    # print(lin_rmse) #### Error of ~0.2879 which is not the best considering that each interval is 1

    from sklearn.tree import DecisionTreeRegressor
    #tree_reg = DecisionTreeRegressor()
    #tree_reg.fit(new_weight_data_prepared, new_weight_data_labels)

    # Test RMSE Error with decision tree ###

    #new_weight_data_predictions = tree_reg.predict(new_weight_data_prepared)
    #tree_mse = mean_squared_error(new_weight_data_labels, new_weight_data_predictions) # Check RMSE for decision tree
    #tree_rmse = np.sqrt(tree_mse)
    #print(tree_rmse)  # 0 mean error - check for over-fitting

    print(new_weight_data_prepared)

    ## Check using cross validation ##

    from sklearn.model_selection import cross_val_score
    #scores = cross_val_score(tree_reg, new_weight_data_prepared, new_weight_data_labels,####Linear regression then rounding
    #                         scoring="neg_mean_squared_error", cv=10)

    #tree_rmse_scores = np.sqrt(-scores)  # Cross_validation

    #print(predict_data_prepared)

    #print(tree_reg.predict(predict_data_prepared))


    #MULTINOMIAL LOGISTIC REGRESSION #####################


    mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(new_weight_data_prepared, new_weight_data_labels)


    print("Multinomial Logistic regression Train Accuracy:", metrics.accuracy_score(new_weight_data_labels, mul_lr.predict(new_weight_data_prepared))) #Accuracy of 0.769

    # Multi-Classification model

    lr = linear_model.LogisticRegression()
    lr.fit(new_weight_data_prepared, new_weight_data_labels)

    print("Logistic regression Train Accuracy:", metrics.accuracy_score(new_weight_data_labels, lr.predict(new_weight_data_prepared))) #Accuracy of 0.718125


    with open('ML_Algorithms_W.pickle','wb') as handle:
        pickle.dump(mul_lr,handle, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(full_pipeline,handle, protocol=pickle.HIGHEST_PROTOCOL) # Pickle full pipeline and logistic
                                                                            #regression model




    #return mul_lr, full_pipeline

#Train_ML_Weight_Prediction()