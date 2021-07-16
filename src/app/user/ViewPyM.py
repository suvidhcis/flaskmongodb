# import os
# from . import user
# from app import db, pymongo
# from flask import jsonify, request

# @user.route("/one")
# def add_one():
#     pymongo.db.user.insert_one({"_id": 1, "Name": "Solaris", "Email": "solaris@gmail.com"})
#     return jsonify(message="success inserted single data")

# @user.route("/many")
# def add_many():
#     pymongo.db.user.insert_many([
#         {"_id": 2, "Name": "SampleName1", "Email": "sample1@mailinator.com"},
#         {"_id": 3, "Name": "SampleName2", "Email": "sample2@mailinator.com"},
#         {"_id": 4, "Name": "SampleName3", "Email": "sample3@mailinator.com"},
#         {"_id": 5, "Name": "SampleName4", "Email": "sample4@mailinator.com"},
#         {"_id": 6, "Name": "SampleName5", "Email": "sample5@mailinator.com"},
#         {"_id": 7, "Name": "SampleName6", "Email": "sample6@mailinator.com"},
#     ])
#     return jsonify(message="Successfully added multiple data!!!!")

# @user.route("/records", methods=["GET"])
# def get_records():
#     output = []
#     records = pymongo.db.user.find()
#     for record in records:
#         output.append({'_id':record['_id'], 'name': record['Name'], 'Email': record['Email']})
#     return {"message":"Success", "records": output}

# @user.route("/replace/<int:id>")
# def replace(id):
#     user = pymongo.db.user.find_one_and_replace({'_id': id}, {'Name': "modified Name 2 04", "Email": "sample1@mailiantor.com"})
#     return {"user": user, "message": "Successfully Updated"}

# @user.route("/update/<int:id>")
# def update(id):
#     user = pymongo.db.user.update_one({'_id': id}, {"$set": {'Name': "updated Name 2 05", "Email": "sample1@mailiantor.com"}})
#     return {"user": user.raw_result, "message": "Successfully Updated"}

# @user.route("/delete/<int:id>", methods=["DELETE"])
# def delete(id):
#     user = pymongo.db.user.find_one_and_delete({'_id': id})
#     if user is None:
#         return {"Error": "User ID not found."}
#     else:
#         return {"user": user, "message": "Successfully deleted"}
