# Port: 5701
# Routes: 
# -----------------------------------------------------------------------------------------

import os
import json
from flask import Blueprint, g, jsonify, request

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)