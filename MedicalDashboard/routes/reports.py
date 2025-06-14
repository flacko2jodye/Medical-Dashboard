from flask import Blueprint, render_template, request, flash, redirect, url_for
from MedicalDashboard.utils.helpers import get_dataframe_from_session

reports_blueprint = Blueprint('reports_blueprint', __name__, url_prefix='/reports')

@reports_blueprint.route('/', methods=['GET', 'POST'])
def user_reports():
    df = get_dataframe_from_session()
    user_data = None
    selected_row = None

    if df is None:
        flash("No data uploaded!", "danger")
        return redirect(url_for("upload_blueprint.upload_file"))

    if request.method == "POST":
        try:
            row_number = int(request.form.get("row_number"))
            if 0 <= row_number < len(df):
                user_data = df.iloc[row_number].to_frame().T.to_html(classes="table table-striped", index=False)
            else:
                user_data = "<p>Error: Row number out of range.</p>"
        except:
            user_data = "<p>Error: Please enter a valid row number.</p>"

    return render_template("user_reports.html", user_data=user_data, selected_row=selected_row)
