import os
import pandas as pd
from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from werkzeug.utils import secure_filename
from MedicalDashboard.utils.helpers import allowed_file, save_uploaded_file

upload_blueprint = Blueprint('upload_blueprint', __name__, url_prefix='/upload')

@upload_blueprint.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = save_uploaded_file(file, filename)
            session['csv_path'] = filepath  
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('dashboard_blueprint.dashboard'))

    return render_template('upload.html')
