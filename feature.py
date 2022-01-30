import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import ExtraTreesClassifier

class Clean():

    def __init__(self, p):
        self.path = p
    
    def FeatureSelection(self):
    
        data = pd.read_csv(self.path).drop(["Attrition_c", "ID"], axis=1)
        target = pd.read_csv(self.path)["Attrition_c"]

        scaler = MinMaxScaler()
        data_scaled = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index)
        
        #Univariate Selection

        best_features = SelectKBest(score_func=chi2, k=10).fit(data_scaled, target)

        dfscores = pd.DataFrame(best_features.scores_)
        dfcolumns = pd.DataFrame(data.columns)

        #concat two dataframes for better visualization 
        featureScores = pd.concat([dfcolumns,dfscores], axis=1)
        featureScores.columns = ["Specs","Score"]  #naming the dataframe columns

        print(featureScores.nlargest(19,"Score"))
        
        #Tree-based feature selection
        tree = ExtraTreesClassifier()
        tree.fit(data, target)

        df_feature_importances = pd.Series(tree.feature_importances_, index=data.columns)
        #print(df_feature_importances.nlargest(19))
        df_feature_importances.nlargest(19).plot(kind="barh")

        #Correlation matrix
        combine = pd.concat([data, target], axis=1)
        corr_mat = combine.corr()

        plt.figure(figsize=(19,19))
        g=sns.heatmap(corr_mat,annot=True,cmap="RdYlGn")

        to_drop = ["educationfield__Life Sciences", "NumCompaniesWorked", "WorkLifeBalance_c", "educationfield__Other", "department__Human Resources", "Education_c", "DistanceFromHome", "MaritalStatus_c"]
        data.drop(to_drop, inplace=True, axis=1)
        combine = pd.concat([data,target], axis=1)
        combine.to_csv("Clean_Selected.csv",index = 0)

path = "Result.csv"
obj = Clean(path)
obj.FeatureSelection()
