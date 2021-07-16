import os

class Development(object):

    DEBUG=True
    SECRET_KEY=os.getenv('SECRET_KEY')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    MONGODB_SETTINGS={"DB": "mongodb1"}
    # MONGO_URI=os.getenv('MONGO_URI')
    RESTPLUS_MASK_SWAGGER=False
    RESTPLUS_JSON={'ensure_ascii': False}

class Production(object):

    DEBUG=False
    SECRET_KEY=os.getenv('SECRET_KEY')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    # MONGODB_NAME=os.getenv('MONGODB_NAME')
    MONGO_URL=os.getenv('MONGO_URL')
    RESTPLUS_MASK_SWAGGER=False
    RESTPLUS_JSON={'ensure_ascii': False}


app_config = {
    "development": Development,
    "production": Production
}