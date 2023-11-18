from flask import Flask
from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__)

  
    # HUGE SECURITY ISSUE - DO NOT KEEP THIS IN PRODUCTION
    # Need this so that the API allows all urls to make requests.
    # Change it so that only our web client is allowed.
    CORS(app, resources={r"/*": {"origins": "*"}})


     # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app