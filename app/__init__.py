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

    # Register blueprints here
    from app.sample import bp as sample_bp
    app.register_blueprint(sample_bp, url_prefix="/sample")

    # Register blueprints here
    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    # Register blueprints here
    from app.store import bp as store_bp
    app.register_blueprint(store_bp, url_prefix="/store")

    # Register blueprints here
    from app.items import bp as items_bp
    app.register_blueprint(items_bp, url_prefix="/items")
    return app
