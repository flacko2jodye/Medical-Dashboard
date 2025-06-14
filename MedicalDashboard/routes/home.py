from flask import Blueprint, render_template

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route('/')
def home():
    return render_template('index.html')
