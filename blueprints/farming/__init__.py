from flask import Blueprint

farming_bp = Blueprint('farming', __name__)

from . import routes
