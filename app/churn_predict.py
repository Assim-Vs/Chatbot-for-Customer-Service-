# app/churn_predict.py
# app/churn_predict.py

import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join("..", "models", "churn_model.joblib")

def load_model():
    data = joblib.load(MODEL_PATH)
    return data["model"], data["scaler"], data["columns"]

def predict_single(customer_dict: dict):
    """
    customer_dict – dictionary with customer fields.
    Keys similar to original CSV (gender, tenure, Contract, etc.).
    """
    model, scaler, columns = load_model()

    # Turn into DataFrame
    df = pd.DataFrame([customer_dict])

    # One-hot encode
    df = pd.get_dummies(df)

    # Add all missing columns = 0
    for col in columns:
        if col not in df.columns:
            df[col] = 0

    # Keep same column order
    df = df[columns]

    # Scale and predict
    X_scaled = scaler.transform(df)
    proba = model.predict_proba(X_scaled)[0][1]  # probability churn=1
    pred = int(proba >= 0.5)

    return {
        "churn_probability": float(proba),
        "churn_prediction": pred
    }

# manual test
if __name__ == "__main__":
    example = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 12,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 70.35,
        "TotalCharges": 845.5
    }
    print(predict_single(example))

