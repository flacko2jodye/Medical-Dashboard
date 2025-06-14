#  Medical Dashboard

A web-based interactive dashboard for uploading and analyzing medical datasets. Built with **Flask**, **Pandas**, and **Scikit-Learn** — this app enables users to upload CSV files, view dataset insights, generate visualizations, and train machine learning models.

---

##  Features

 Upload CSV medical data  
 View dataset statistics (rows, columns, missing values)  
 Correlation heatmap for numeric features  
 Per-row patient report viewer  
 Train a `RandomForestRegressor` with hyperparameter tuning  
 Get predictions + evaluation metrics (MSE, R²)  
 Visualize feature importance and predicted vs actual

---

##  Project Structure

MedicalDashboard/ ├── app/ │ ├── init.py │ ├── routes/ # Flask Blueprints │ ├── services/ # Model and plot logic │ ├── utils/ # Helpers (file save, session DataFrame) │ ├── templates/ # HTML pages (Jinja2) │ └── static/ # CSS and image outputs ├── uploads/ # Where CSVs are saved ├── static/visuals/ # Correlation heatmap, etc. ├── requirements.txt ├── app.py └── README.md