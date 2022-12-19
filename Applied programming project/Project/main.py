# Machine Learning
import pandas as pd

from RandomForest import RandomForest
from daten import Daten
from feature import FeatureSelection
from testtrain import TestTrain
from Resampling import Resample

data = Daten()
data = data.data

new_data = FeatureSelection()
new_data = new_data.new_data_frame(data)

r = Resample()
new_data = r.resample(new_data)

k = TestTrain()
[X, y] = k.define_target_features(new_data)
[X_train, X_test, y_train, y_test] = k.define_train_test(X, y)

rf = RandomForest()
rf_model = rf.random_forest(X_train, y_train)


def question():
    predictors = []
    parameters = ['sysBP', 'glucose', 'age', 'totChol', 'cigsPerDay', 'diaBP', 'prevalentHyp', 'diabetes', 'BPMeds',
                  'male']

    print('Input Patient Information:')

    age = input("Patient's age:")
    predictors.append(age)
    male = input("Patient's gender (male=1, female=0):")
    predictors.append(male)
    cigsPerDay = input("Smoked cigarettes per day:")
    predictors.append(cigsPerDay)
    sysBP = input("Systolic blood pressure:")
    predictors.append(sysBP)
    diaBP = input("Diastolic blood pressure:")
    predictors.append(diaBP)
    totChol = input("Cholesterin level:")
    predictors.append(totChol)
    prevalentHyp = input("Hypertension? (Yes=1, No=0):")
    predictors.append(prevalentHyp)
    diabetes = input("Diabetes? (Yes=1, No=0):")
    predictors.append(diabetes)
    glucose = input("Glucose leven?:")
    predictors.append(glucose)
    BPMeds = input("Blood Pressure Medication? (Yes=1, No=0):")
    predictors.append(BPMeds)

    patient_data = dict(zip(parameters, predictors))
    patient_data_frame = pd.DataFrame(patient_data, index=[0])
    print(patient_data_frame)

    chd_prediction = rf_model.predict(patient_data_frame)

    print("Result of the CHD-prediction:")
    if chd_prediction == 1:
        print("The patient has a CHD-risk.")
    if chd_prediction == 0:
        print("The patient has no CHD-risk.")



question()
