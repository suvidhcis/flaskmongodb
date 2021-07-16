from flask import Blueprint

shared = Blueprint('shared', __name__)

from . import auth_views
from . import helpers