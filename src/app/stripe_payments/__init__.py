from flask import Blueprint

stripe_payments = Blueprint('stripe_payments', __name__)

from . import stripe_views