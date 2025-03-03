# Routes: 
#   [pointSystemRules] 
#   /getPointSystemRules (GET), /getSpecificPointSystemRule/<id> (GET), 
#   /createPointSystemRule (POST), 
#   /updatePointSystemRule/<id> (PUT), 
#   /deletePointSystemRule/<id> (DELETE)
# 
#   [pointsRecorder]
#   /getPointsForUser/<id>/<userType> (GET), 
#   /createPointsForUser (POST),
#   /addPointsForUser (PUT), /deductPointsForUser (PUT)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

