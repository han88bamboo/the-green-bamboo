import os
from flask import Blueprint, jsonify


file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


@blueprint.route("", methods=["GET"])
def info():
    return jsonify({"code": 200, "data": "OK"}), 200
