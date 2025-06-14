from flask import Blueprint, render_template, request, flash, redirect, url_for
from MedicalDashboard.utils.helpers import get_dataframe_from_session
from MedicalDashboard.services.ml_model import train_model_pipeline

predict_blueprint = Blueprint('predict_blueprint', __name__, url_prefix='/predict')

@predict_blueprint.route('/', methods=['GET', 'POST'])
def predict():
    df = get_dataframe_from_session()
    if df is None:
        flash("No data uploaded!", "danger")
        return redirect(url_for("upload_blueprint.upload_file"))

    result = {}
    if request.method == 'POST':
        target_col = request.form.get('target_column')
        result = train_model_pipeline(df, target_col)

    return render_template('predictions.html', **result)
