from flask import Flask,request
from config import config
from models.revokeToken import BlockTokenModel
from flask_cors import CORS
from models.revokeToken import BlockTokenModel
from config.config import *
from models.users import Users
import sys
# from middlewares.before_request_middileware import PermissionMiddleware

from routes import *
app =  config.app
# api = Api(app, security = 'apikey',authorizations=authorizations)

import connexion
from connexion.resolver import RestyResolver
app = connexion.FlaskApp(__name__,port=5000,specification_dir='swagger_yaml/')
app.app.CORS_HEADERS = "Content-Type"
app.add_api('api_doc_swagger.yaml',resolver=RestyResolver('api'))
CORS(app.app,resources={r"/api/*": {"origins": "*"}},headers="Content-Type")
@app.app.after_request
def set_default_headers(response): # pylint: disable=unused-variable
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers,Authorization, X-Requested-With, x-rh-identity"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS, PATCH, POST,PUT,DELETE"
    return response



jwt = config.jwt
blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return BlockTokenModel.is_jti_blacklisted(jti)

# CORS(app)

if __name__ == "__main__":
    app.run(host=config.host, port=config.port,debug=True)
