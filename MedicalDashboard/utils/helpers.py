import os
import pandas as pd
from flask import current_app, session

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, filename):
    folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    file.save(filepath)
    return filepath


def get_dataframe_from_session():
    csv_path = session.get('csv_path')
    if csv_path and os.path.exists(csv_path):
        try:
            return pd.read_csv(csv_path)
        except Exception as e:
            print("Error reading CSV from path:", e)
    return None
