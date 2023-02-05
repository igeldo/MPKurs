# Machine Learning
import pandas as pd

from RandomForest import RandomForest
from daten import Daten
from feature import FeatureSelection
from testtrain import TestTrain
from Resampling import Resample

# Einlesen der Daten
data = Daten()
data = data.data_original

# Wahl der besten 10 Features
FS = FeatureSelection()
data_best_features = FS.new_data_frame(data)

# Splitten in Test- und Trainingsdatensatz
TT = TestTrain()
[Feature, Target] = TT.define_target_features(data_best_features)
[Feature_train, Feature_test, Target_train, Target_test] = TT.define_train_test(Feature, Target)

# Anwendung der SMOTE-Methode
RS = Resample()
[Feature_over, Target_over] = RS.upsampling_smote(Feature, Target)
[over_Feature_train, over_Feature_test, over_Target_train, over_Target_test] = TT.upsampling_Smote_over(Feature_over,
                                                                                                        Target_over)
# Erstellung des Random Forest Klassifikator
RFC = RandomForest()
rf_model = RFC.random_forest(over_Feature_train, over_Target_train)
prediction = rf_model.predict(Feature_test)
accuracy = RFC.accuracy(Target_test, prediction)
print(accuracy)


def question():
    # Start des Eingabe-Dialogs
    predictors = []
    parameters = ['sysBP', 'glucose', 'age', 'totChol', 'cigsPerDay', 'diaBP', 'prevalentHyp', 'diabetes', 'BPMeds',
                  'male']

    print('Input Patient Information:')
    print('Please enter the patient Information...')

    # ALTER
    age = input("Patient's age:")
    predictors.append(age)

    # GESCHLECHT
    male = input("Patient's gender (male=1, female=0):")
    predictors.append(male)
    if int(male) == 0:
        print("")
    elif int(male) == 1:
        print("")
    else:
        print("An incorrect input was given. Please enter 0 for a woman and 1 for a man.")
        raise SystemError("Exit this programm. Please start again.")

    # Zigaretten
    cigsPerDay = input("Smoked cigarettes per day:")
    predictors.append(cigsPerDay)

    # Systolischer Blutdruck
    sysBP = input("Systolic blood pressure:")
    predictors.append(sysBP)

    # Diastolischer Blutdruck
    diaBP = input("Diastolic blood pressure:")
    predictors.append(diaBP)

    # Totaler Cholesterin Wert
    totChol = input("Cholesterin level:")
    predictors.append(totChol)

    # Hypertension
    prevalentHyp = input("Hypertension? (Yes=1, No=0):")
    predictors.append(prevalentHyp)
    if int(prevalentHyp) == 0:
        print("")
    elif int(prevalentHyp) == 1:
        print("")
    else:
        print("An incorrect input was given. Please enter 1 for a Hypertension and 0 for no Hypertension.")
        raise SystemError("Exit this programm. Please start again.")

    # DIABETES
    diabetes = input("Diabetes? (Yes=1, No=0):")
    predictors.append(diabetes)
    if int(diabetes) == 0:
        print("")
    elif int(diabetes) == 1:
        print("")
    else:
        print("An incorrect input was given. Please enter 1 for Diabetes and 0 for no Diabetes.")
        raise SystemError("Exit this programm. Please start again.")

    # GLUKOSE
    glucose = input("Glucose leven?:")
    predictors.append(glucose)

    # BLUTDRUCKMEDIKAMENTE
    BPMeds = input("Blood Pressure Medication? (Yes=1, No=0):")
    predictors.append(BPMeds)
    if int(BPMeds) == 0:
        print("")
    elif int(BPMeds) == 1:
        print("")
    else:
        print("An incorrect input was given. Please enter 1 for BPMeds and 0 for no BPMeds.")
        raise SystemError("Exit this programm. Please start again.")

    # Die eingegebenen Daten werden miteinander zu einem Daten-Frame verknüpft
    patient_data = dict(zip(parameters, predictors))
    patient_data_frame = pd.DataFrame(patient_data, index=[0])
    print(patient_data_frame)

    # Vorhersage des Risikos einer Herzerkrankung
    chd_prediction = rf_model.predict(patient_data_frame)

    # Antwort-Dialog
    print("Result of the CHD-prediction:")
    if chd_prediction == 1:
        print("The patient has a CHD-risk.")
    if chd_prediction == 0:
        print("The patient has no CHD-risk.")


question()
