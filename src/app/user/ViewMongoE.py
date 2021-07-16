from functools import partial
import os
import json
from . import user
from ..extension import db, docs
from flask import jsonify, request, g, render_template
from ..models import UserModel, UserSchema
from ..shared.helpers import is_exist
from ..shared.auth_views import Auth
from app.api_spec import spec

user_schema = UserSchema()

@user.route("/get_all", methods=["GET"])
# @docs(description="Return all users", tags=['User'])
def get_all_user():
    """Get all users endpoint.
    ---
    get:
      tags:
        - "User"
      summary: "get all the users present in the database."
      description: This Function returns the details of all the users present in database.
      responses:
        200:
          description: Return all users
          content:
            application/json:
              schema: UserSchema
    """
    user = UserModel.objects()
    return jsonify(user), 200

@user.route("/", methods=["POST"])
def create_user():
    """Create a user endpoint.
    ---
    post:
      tags:
        - "User"
      summary: "Create a new user."
      description: This Function returns the details of all the users present in database.
      consumes:
        - application/json
      parameters:
      - in: body
        name: body
        description: User object that needs to be registered to the database
        required: true
        schema:
          type: object
          required:
              - email
          properties:
              name:
                type: string
              email:
                type: string
              password:
                type: string
      responses:
        '200':
          description: return Success output.
          content:
            application/json:
              schema: UserSchema
        '400':
            description: "Error: BAD request"
            content:
                application/json:
                    schema: UserSchema
    """
    record = request.get_json()
    if record is None:
        return {"Error": "No data Supplied."}, 400

    schema = user_schema.load(record)

    if UserModel.objects(email=schema['email']):
        return {"Error": "User Data already exists."}, 400
    user =  UserModel(**schema)
    user.hash_password()
    user.save()
    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data["_id"])
    return {"message": "User Created Successfully", "Token": token, "id": str(user.id)}, 200

@user.route("/login", methods=["POST"])
def login_user():
    record = request.get_json()
    if record is None:
        return {"Error": "No data supplied."}, 400
    schema = user_schema.load(record, partial=True)

    user =  UserModel.objects.get(email=schema["email"])
    authorized = user.check_password(schema["password"])
    
    if not user:
        return {"Error": "User Does not Exists."}, 404
    
    if not authorized:
        return {"Error": "Invalid Credentials."}, 400

    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data["_id"])
    return {"Message": "User Logged In.", "Token": token}



@user.route("/<int:id>", methods=["GET"])
@Auth.auth_required
def get_one_user(id):
    try:
        user = UserModel.objects.get(_id=id)
        record = user_schema.dump(user)
        return {"User": record}
    except Exception:
        return {"error": "User not Found"}

@user.route("/delete/<int:id>", methods=["DELETE"])
@Auth.auth_required
def delete(id):
    try:
        user = UserModel.objects.get(_id=id)
        user.delete()
        return {"Message": "User Deleted Successfully."}
    except Exception:
        return {"Error": "User not found."}

@user.route("/update/<int:id>", methods=["PUT"])
@Auth.auth_required
def update_user(id):
    record = request.get_json()
    data = user_schema.load(record, partial=True)
    
    if data is None:
        return {"Error": "Please Enter the Data to be updated."}
    else:
        try:
            user = UserModel.objects.get(_id=id)
            user.update(**data)
            ser_user = user_schema.dump(user)
            return {"Message": "User Updated Successfully.", "User": data}
        except Exception:
            return {"Error": "User not found."}            

@user.route("/api/swagger.json")
def create_swagger_spec():
    return jsonify(spec.to_dict())
