from flask import Blueprint

community_bp = Blueprint('community', __name__)

from . import routes
