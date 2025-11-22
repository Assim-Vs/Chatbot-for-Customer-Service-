# app/churn_train.py
# app/churn_train.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Paths
DATA_PATH = os.path.join("..", "data", "telco_churn.csv")
MODEL_PATH = os.path.join("..", "models", "churn_model.joblib")

def load_and_clean(path):
    df = pd.read_csv(path)

    # Drop ID column if present
    if "customerID" in df.columns:
        df = df.drop("customerID", axis=1)

    # Convert TotalCharges to numeric
    if "TotalCharges" in df.columns and df["TotalCharges"].dtype == "O":
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

    # Encode target
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    return df

def preprocess(df):
    # One-hot encode all object columns
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    return df

def train():
    print("Loading data from:", DATA_PATH)
    df = load_and_clean(DATA_PATH)
    df = preprocess(df)

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print("Shape of X_train:", X_train.shape)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42, class_weight="balanced"
    )

    # Define hyperparameter grid
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15],
        'min_samples_split': [2, 4],
        'min_samples_leaf': [1, 2]
    }

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid,
                               cv=3, scoring='f1')

    print("Training model...")
    grid_search.fit(X_train_scaled, y_train)

    # Get best model from grid search
    best_model = grid_search.best_estimator_
    print("Best hyperparameters:", grid_search.best_params_)
    print("Evaluating model...")
    preds = model.predict(X_test_scaled)
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, preds))
    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    # Feature Importance
    importances = best_model.feature_importances_
    feature_names = X.columns
    feature_importances = pd.DataFrame({'feature': feature_names, 'importance': importances})
    feature_importances = feature_importances.sort_values('importance', ascending=False)
    print("\nFeature Importances:")
    print(feature_importances)
    # Save model + scaler + columns
    joblib.dump({"model": best_model, "scaler": scaler, "columns": X.columns.tolist()}, MODEL_PATH
    )
    print("Model saved to:", MODEL_PATH)

if __name__ == "__main__":
    train()
