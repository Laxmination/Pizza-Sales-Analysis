import joblib

LOGISTIC_MODEL_PATH ='Cardio/models/Logistics/logistic_model.pkl'
LOGISTIC_SCALER_PATH ='Cardio/models/Logistics/logistic_scaler.pkl'

SVM_MODEL_PATH ='Cardio/models/SVM/svm_model.pkl'
SVM_SCALER_PATH ='Cardio/models/SVM/svm_scaler.pkl'

def read_logistic():
    model = joblib.load(LOGISTIC_MODEL_PATH)
    scaler = joblib.load(LOGISTIC_SCALER_PATH)
    
    return model, scaler

def read_svm():
    model = joblib.load(SVM_MODEL_PATH)
    scaler = joblib.load(SVM_SCALER_PATH)
    
    return model, scaler





















# Logistic Model
# import numpy as np
# import pandas as pd

# from sklearn.svm import SVC
# # Train Test Split
# from sklearn.model_selection import train_test_split
# # Feature Scaling
# from sklearn.preprocessing import StandardScaler
# # Classification Metrics
# from sklearn.metrics import classification_report, confusion_matrix
# import joblib

# df = pd.read_csv('Data/Cardiovascular_Disease.csv')
# df.head()

# df['age'] = df['age']//365

# filtered_df = df[
#     (df['height'].between(150, 190)) &
#     (df['weight'].between(45, 110)) &
#     (df['ap_hi'].between(90, 180)) &
#     (df['ap_lo'].between(50, 90))
# ]

# # LOGISTIC_MODEL_PATH ='models/Logistics/logistic_model.pkl'
# # LOGISTIC_SCALER_PATH ='models/Logistics/logistic_scaler.pkl'

# SVM_MODEL_PATH ='models/SVM/svm_model.pkl'
# SVM_SCALER_PATH ='models/SVM/svm_scaler.pkl'


# def svmModel():
#     features =['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active']
#     target = 'cardio'
    
#     X = filtered_df[features]
#     Y = filtered_df[target]
    
#     X_train, X_test, Y_train, Y_test = train_test_split(
#         X, Y, test_size=0.2, random_state=42, stratify=Y
#     )
    
#     scaler = StandardScaler()
#     X_train_scale = scaler.fit_transform(X_train)
#     X_test_scale = scaler.transform(X_test)
    
#     model = SVC(
#         kernel='linear',
#         C = 1.0,
#         gamma= 'scale'
#     )
#     model.fit(X_train_scale, Y_train)
    
#     model.predict(X_test_scale)
    
#     joblib.dump(model,SVM_MODEL_PATH)
#     joblib.dump(model, SVM_SCALER_PATH)
    
#     return scaler, model
