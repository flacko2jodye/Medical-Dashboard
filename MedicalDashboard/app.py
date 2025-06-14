from flask import Flask
from MedicalDashboard.routes.home import home_blueprint
from MedicalDashboard.routes.upload import upload_blueprint
from MedicalDashboard.routes.dashboard import dashboard_blueprint
from MedicalDashboard.routes.reports import reports_blueprint
from MedicalDashboard.routes.predict import predict_blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'
    app.config['UPLOAD_FOLDER'] = 'uploads/'

    # Register all modular Blueprints (feature-based)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(upload_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(reports_blueprint)
    app.register_blueprint(predict_blueprint)

    return app

# Run the app directly (development mode)
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
