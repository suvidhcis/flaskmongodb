from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_apispec.extension import FlaskApiSpec

# pymongo = PyMongo(uri=os.getenv("MONGO_URI"))
# db = pymongo.db
db = MongoEngine()
api = Api()
bcrypt = Bcrypt()
docs = FlaskApiSpec()