import os
from flask import Flask, jsonify
from config import app_config
from .extension import db, api, bcrypt, docs
import stripe
from app.api_spec import spec
from app.user.ViewMongoE import get_all_user

def create_app(env_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[env_name])
    app.config.from_object(app_config)

    register_extension(app)
    register_blueprints(app)
    return app

def register_extension(app):

    # pymongo.init_app(app)
    db.init_app(app)
    api.init_app(app)
    bcrypt.init_app(app)
    docs.init_app(app)
    stripe.api_key = os.getenv("SK_TEST_KEY")
    return None

def register_blueprints(app):
    
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .shared import shared as shared_blueprint
    app.register_blueprint(shared_blueprint)

    from .stripe_payments import stripe_payments as stripe_blueprint
    app.register_blueprint(stripe_blueprint)

    from .swagger import swagger_ui_blueprint, SWAGGER_URL
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    with app.test_request_context():
    # register all swagger documented functions here
        for fn_name in app.view_functions:
            print("!!!!!!!!!!!!!!!!!!", fn_name)
            if fn_name == 'static':
                continue
            print(f"Loading swagger docs for function: {fn_name}")
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)

    return None