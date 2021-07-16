from .extension import db
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
from marshmallow import fields, Schema


class UserModel(db.Document):
    _id = db.SequenceField(primary_key=True)
    name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    modified_at = db.DateTimeField(default=datetime.datetime.utcnow)
    active = db.BooleanField(default=True)

    def to_json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at
        }

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_one_user(_id):
        return UserModel.objects(_id=_id)

class UserSchema(Schema):
    
    _id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)

class StripeDetail(db.Document):
    _id = db.SequenceField(primary_key=True)
    user_id = db.ReferenceField(UserModel)
    payment_id = db.StringField()
    amount = db.FloatField()

    def to_json(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "payment_id": self.payment_id,
            "amount": self.amount
        }

class StripeSchema(Schema):
    user_id = fields.Int(dump_only=True)
    payment_id = fields.Str(dump_only=True)
    amount = fields.Str(required=True)