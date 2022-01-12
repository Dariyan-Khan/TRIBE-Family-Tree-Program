import pandas as pd
import numpy as np


def load_weight_data():
    return pd.read_csv("Final_Weight-Height-REAL-CSV-1.csv")

weight_data=load_weight_data()

weight_data.drop(['Weight'], axis=1)

print(weight_data.head())

import matplotlib.pyplot as plt

#weight_data.hist(bins=50, figsize=(20,15))
#plt.show()

## Split into training and testing data set


from zlib import crc32

def test_set_check(identifier,test_ratio):
    return crc32(np.int64(identifier))  & 0xffffffff < test_ratio * 2**32

def split_train_test_by_id(data, test_ratio, id_column):
    ids=data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]

weight_data_with_id = weight_data.reset_index()
train_set, test_set = split_train_test_by_id(weight_data_with_id, 0.2, "index")

###plot scatter plots ###

from pandas.plotting import scatter_matrix

#attributes = ["Gender","Height","Weight","Mother_Height", "Father_Height"]

#scatter_matrix(weight_data[attributes], figsize=(12,8))
#plt.show()

#Correlation matrix###

#corr_matrix=weight_data.corr()
#corr_matrix["Height"].sort_values(ascending=True)
#print(corr_matrix)


weight_data["Weight_cat"]=pd.cut(weight_data["Weight"],
                                        bins=[0,55,70,85,100,np.inf],
                                        labels=[1,2,3,4,5])

from sklearn.model_selection import StratifiedShuffleSplit
split=StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(weight_data, weight_data["Weight_cat"]):
    strat_train_set= weight_data.loc[train_index]
    strat_test_set=weight_data.loc[test_index]

#weight_data["Father_Height_cat"]=pd.cut(weight_data["Father_Height"],
#                                       bins=[0,67,69.75,70.16,72,np.inf],
#                                        labels=[1,2,3,4,5])
#
#from sklearn.model_selection import StratifiedShuffleSplit
#split=StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
#for train_index, test_index in split.split(weight_data, weight_data["Father_Height_cat"]):
#    strat_train_set= weight_data.loc[train_index]
#    strat_test_set=weight_data.loc[test_index]




weight_data.drop(['Weight'], axis=1, inplace=True)

print(weight_data.head())

print(type(weight_data))

print("WHYYYYY")


weight_data=strat_train_set.drop("Height", axis=1)
weight_labels = strat_train_set["Height"].copy()

weight_data.drop(['Weight'], axis=1, inplace=True)

print(weight_data.head())

print(weight_labels)

#print(weight_labels)

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

weight_data_cat=weight_data[["Gender"]]
print(weight_data_cat.head(10))

from sklearn.preprocessing import OrdinalEncoder


ordinal_encoder=OrdinalEncoder()

weight_data_cat_encoded = ordinal_encoder.fit_transform(weight_data_cat)

#ONE HOT ENCODER FOR GENDER ###

from sklearn.preprocessing import OneHotEncoder

cat_encoder=OneHotEncoder()
weight_data_cat_1hot=cat_encoder.fit_transform(weight_data_cat)
print(weight_data_cat_1hot)


from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

#Drop gender column

weight_data_num=weight_data.drop("Gender", axis=1)

num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),

##########   REMOVED LINE HERE ###############

    ('std_scaler', StandardScaler())

    ])

weight_data_num_tr = num_pipeline.fit_transform(weight_data_num)


from sklearn.compose import ColumnTransformer

num_attribs = list(weight_data_num)
cat_attribs=["Gender"]





full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", OneHotEncoder(), cat_attribs),

])



weight_data_prepared=full_pipeline.fit_transform(weight_data)

from sklearn.linear_model import LinearRegression




print(weight_data_prepared)




#del weight_data['Weight']

#lin_reg = LinearRegression()
#lin_reg.fit(weight_data_prepared, weight_labels)        #Off by ~1in

from sklearn.tree import DecisionTreeRegressor

tree_reg = DecisionTreeRegressor()
tree_reg.fit(weight_data_prepared, weight_labels)



#Test on test set - linear regression model

def Predict_Value(input_data,input_labels):
    some_data = input_data.iloc[:5]
    #some_labels=input_labels.iloc[:5]
    #print(some_labels)
    print(some_data)
    some_data_prepared=full_pipeline.transform(some_data)
    print("Predictions:", tree_reg.predict(some_data_prepared))   ### Gives 0 error - need to check for over-fitting
    #print("Labels:", list(some_labels))

Predict_Value(weight_data,weight_labels)

#Evaluate reliability via cross validation

from sklearn.model_selection import cross_val_score
scores=cross_val_score(tree_reg, weight_data_prepared, weight_labels, scoring = "neg_mean_squared_error", cv=10)

tree_rmse_scores=np.sqrt(-scores)

## View results of cross validation###

def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())    # Standard deviation is only ~0.058 so, decision tree is quite precise - we will use this model

display_scores(tree_rmse_scores)


#My data###

#my_data=["Male","70","60","67"]
#my_data.reshape(1,-1)
#my_labels=some_labels
#print(my_data)
#print(my_labels)
#my_data_prepared=full_pipeline.transform(my_data)
#print(lin_reg.predict(some_data_prepared))


