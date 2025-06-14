from flask import Blueprint, render_template, url_for
from MedicalDashboard.utils.helpers import get_dataframe_from_session
from MedicalDashboard.services.visuals import generate_visuals

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__, url_prefix='/dashboard')

@dashboard_blueprint.route('/')
def dashboard():
    df = get_dataframe_from_session()
    if df is None:
        return render_template('dashboard.html', num_rows=0, num_cols=0, missing_values=0, table_data=None)

    num_rows, num_cols = df.shape
    missing_values = df.isnull().sum().sum()
    table_data = df.to_html(classes="table table-striped", index=False)
    heatmap_path = generate_visuals(df)

    return render_template(
        'dashboard.html',
        num_rows=num_rows,
        num_cols=num_cols,
        missing_values=missing_values,
        table_data=table_data,
        heatmap=url_for('static', filename='visuals/heatmap.png') if heatmap_path else None
    )
