from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = _get_picture_by_id(id)
    if not picture:
        return {"message": "Could not find picture"}, 404
    return jsonify(picture)

def _get_picture_by_id(id):
    return next(filter(lambda picture: picture['id']==id, data), None)
######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    incoming_picture = request.json
    id = incoming_picture['id']
    picture = _get_picture_by_id(id)
    if picture:
        message = f"picture with id {id} already present"
        return {"Message": message}, 302
    data.append(incoming_picture)
    return incoming_picture, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    incoming_picture = request.json
    id = incoming_picture['id']
    picture = _get_picture_by_id(id)
    if not picture:
        message = {"message": "picture not found"}
        return {"Message": message}, 404
    for i in range(len(data)):
        pic = data[i]
        if pic['id'] == id:
            data[i] = incoming_picture
            break
    return incoming_picture

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pos = -1
    for i in range(len(data)):
        if data[i]['id'] == id:
            pos = i
            break
    if pos != -1:
        del data[i]
        return "", 204
    else:
        return {"message": "picture not found"}, 404
