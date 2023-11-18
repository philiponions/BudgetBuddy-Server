from app.main import bp
from flask import abort, request
from werkzeug.exceptions import HTTPException


@bp.route('/')
def index():
    return 'Hello World'