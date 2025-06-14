import io
import base64
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_model_pipeline(df, target_col):
    result = {
        "model_name": None,
        "prediction": None,
        "accuracy": None,
        "report": None,
        "confusion_plot": None,
        "feature_cols": None,
        "feature_importance": None,
        "best_params": None,
        "feature_plot": None
    }

    if target_col not in df.columns:
        result['error'] = "Invalid target column selected."
        return result

    numeric_df = df.select_dtypes(include=['number']).copy()
    feature_cols = [col for col in numeric_df.columns if col != target_col]

    if not feature_cols:
        result['error'] = "Not enough numeric columns to train model."
        return result

    # Fill missing
    X = numeric_df[feature_cols].fillna(numeric_df.mean())
    y = numeric_df[target_col].fillna(numeric_df[target_col].mode()[0])

    # Feature engineering
    if "BMI" in X.columns and "Age" in X.columns:
        X["BMI_Age"] = X["BMI"] * X["Age"]
    if "Glucose" in X.columns and "Insulin" in X.columns:
        X["Glucose_Insulin"] = X["Glucose"] * X["Insulin"]

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Classifiers + hyperparams
    models = {
        "RandomForest": (RandomForestClassifier(class_weight="balanced", random_state=42), {
            'n_estimators': [100],
            'max_depth': [None, 10],
            'min_samples_split': [2],
            'min_samples_leaf': [1]
        }),
        "LogisticRegression": (LogisticRegression(class_weight="balanced", solver='liblinear'), {
            'C': [0.01, 0.1, 1.0, 10.0]
        }),
        "GradientBoosting": (GradientBoostingClassifier(random_state=42), {
            'n_estimators': [100],
            'learning_rate': [0.1, 0.05],
            'max_depth': [3, 5]
        }),
    }

    best_score = -1
    best_model_name = None
    best_model = None
    best_params = None
    best_y_pred = None

    for name, (model, params) in models.items():
        try:
            grid = GridSearchCV(model, params, cv=3, scoring='accuracy', n_jobs=-1)
            grid.fit(X_train, y_train)
            acc = grid.best_score_
            if acc > best_score:
                best_score = acc
                best_model_name = name
                best_model = grid.best_estimator_
                best_params = grid.best_params_
        except Exception as e:
            print(f"Model {name} failed:", e)

    if best_model is None:
        result["error"] = "All models failed during training."
        return result

    # Evaluate
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    result.update({
        "model_name": best_model_name,
        "prediction": y_pred[0],
        "accuracy": accuracy,
        "report": classification_report(y_test, y_pred),
        "confusion": confusion_matrix(y_test, y_pred).tolist(),
        "feature_cols": list(X.columns),
        "feature_importance": getattr(best_model, "feature_importances_", [0]*len(X.columns)),
        "best_params": best_params
    })

    # Plot: feature importance
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=result['feature_importance'], y=result['feature_cols'], ax=ax)
    ax.set_title("Feature Importance")
    buf = io.BytesIO(); plt.savefig(buf, format='png'); buf.seek(0)
    result['feature_plot'] = base64.b64encode(buf.getvalue()).decode(); plt.close()

    # Plot: confusion matrix heatmap
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Predicted'); ax.set_ylabel('Actual'); ax.set_title('Confusion Matrix')
    buf = io.BytesIO(); plt.savefig(buf, format='png'); buf.seek(0)
    result['confusion_plot'] = base64.b64encode(buf.getvalue()).decode(); plt.close()

    return result