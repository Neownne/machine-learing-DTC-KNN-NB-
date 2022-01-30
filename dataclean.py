from ast import Index
import pandas as pd
import datetime

class Clean():
    def __init__(self, p):
        self.path = p

    def DataImport(self):
        try:
            df = pd.read_csv(self.path, encoding ="utf-8")
        except IOError:
            print("ERROR")
        else:
            print("SUCCESS")
            return df
    
    def ChangeDate(self):

        df = self.DataImport()

        for i in range(len(df)):
            tmp = str(df["StartDate"][i])
            date = tmp.split("/")
            a = datetime.datetime(2022, 1, 27)
            b = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            df["StartDate"][i] = (a - b).days
        
        return df

    def ChangeNum(self):

        df = self.ChangeDate()

        AttritionDict = {"Yes": 0, "No": 1}
        EductionDict = {"Below College": 0, "College": 1, "Bachelors": 2, "Masters": 3, "PhD": 4}
        EnvironmentSatisfactionDict = {"Low": 0, "Medium": 1, "High": 2, "Very High": 3}
        JobSatisfactionDict = {"Low": 0, "Medium": 1, "High": 2, "Very High": 3}
        MaritalStatusDict = {"Divorced": 0, "Single": 1, "Married": 2}
        WorkLifeBalanceDict = {"Bad": 0, "Good": 1, "Better": 2, "Best": 3}

        df["Attrition_c"]= pd.Series([AttritionDict.get(Attrition, "None") for Attrition in df["Attrition"]], index = df.index)
        df["Education_c"]= pd.Series([EductionDict.get(Education, "None") for Education in df["Education"]], index = df.index)
        df["EnvironmentSatisfaction_c"]= pd.Series([EnvironmentSatisfactionDict.get(EnvironmentSatisfaction, "None") for EnvironmentSatisfaction in df["EnvironmentSatisfaction"]], index = df.index)
        df["JobSatisfaction_c"]= pd.Series([JobSatisfactionDict.get(JobSatisfaction, "None") for JobSatisfaction in df["JobSatisfaction"]], index = df.index)
        df["MaritalStatus_c"]= pd.Series([MaritalStatusDict.get(MaritalStatus, "None") for MaritalStatus in df["MaritalStatus"]], index = df.index)
        df["WorkLifeBalance_c"]= pd.Series([WorkLifeBalanceDict.get(WorkLifeBalance, "None") for WorkLifeBalance in df["WorkLifeBalance"]], index = df.index)
        
        df = df.drop(["Attrition","Education","EnvironmentSatisfaction", "JobSatisfaction", "MaritalStatus", "WorkLifeBalance"], axis = 1)

        return df

    def ChangeBool(self):

        df = self.ChangeNum()
        df = pd.get_dummies(df, columns=["Department"], prefix=["department_"])
        df = pd.get_dummies(df, columns=["EducationField"], prefix=["educationfield_"])
        return df
    
    def DeleteChar(self):

        df = self.ChangeBool()

        for i in range(len(df)):
            tmp = str(df["DistanceFromHome"][i])
            tmp = list(filter(str.isdigit, tmp))
            tmp = int(tmp[0])
            df["DistanceFromHome"][i] = tmp
        for i in range(len(df)):
            tmp = str(df["MonthlyIncome"][i])
            tmp = list(filter(str.isdigit, tmp))
            A = ""
            for num in tmp:
                A += str(num)
            df["MonthlyIncome"][i] = A
        
        return df
    
    def SaveData(self):

        df = self.DeleteChar()
        df.to_csv("Result.csv", index = 0)

path = "IMA2.csv"
obj = Clean(path)
obj.SaveData()