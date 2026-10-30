from flask import Blueprint

policy_bp = Blueprint('policy', __name__)

from . import routes
