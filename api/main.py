from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import RevokedTokenError, JWTDecodeError
from flask_redoc import Redoc
from flask_restx import Api
from flask_restx.reqparse import HTTPStatus
from flask_talisman import Talisman
from jwt.exceptions import ExpiredSignatureError

from core.config import config
from core.redis import access_blocklist, refresh_blocklist

ACCESSS_EXPIRES = timedelta(weeks=1)
LOG_FILE = "/etc/flask-api/out.log"

######################
# Setup Flask Server #
######################
app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["JWT_SECRET_KEY"] = config.get("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["PROPOGATE_EXCEPTIONS"] = True

csp = {
    'default-src': ['\'self\''],
    'frame-ancestors': ['\'none\'']
}

CORS(app)
Redoc(app, "../postman/schemas/index.yaml")
Talisman(
    app,
    force_https=False,
    frame_options='DENY',
    content_security_policy=csp,
    referrer_policy='no-referrer',
    x_xss_protection=False,
    x_content_type_options=True
)
api = Api(app)
jwt = JWTManager(app)
jwt._set_error_handler_callbacks(api)

# Check if token has been revoked
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(_, jwt_payload):
    jti = jwt_payload["jti"]
    access_revoked = access_blocklist.get(jti) is not None
    refresh_revoked = refresh_blocklist.get(jti) is not None
    return access_revoked or refresh_revoked

# Response for requests made useing revoked tokens
@api.errorhandler(RevokedTokenError)
def handle_revoked_token(_):
    return {"message": "Token has been revoked", "success": False, "data": {}}, 403

@api.errorhandler(JWTDecodeError)
def handle_decoder_error(_):
    return {"message": "Error decoding token", "success": False, "data": {}}, HTTPStatus.INTERNAL_SERVER_ERROR

@api.errorhandler(ExpiredSignatureError)
def handle_expired_signature_error(_):
    return {"message": "Token has expired", "success": False, "data": {}}, 401

# Response for requests made using invalid tokens
@jwt.token_verification_failed_loader
def handle_failed_verification(_, jwt_payload):
    return {"message": "Token verification failed", "success": False, "data": {}}, 403

@app.after_request
def add_headers(response):
    response.headers['X-XSS-Protection'] = '0'
    response.headers['Cache-Control'] = 'no-store, max-age=0, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

#####################
# Setup API Routes #
#####################
from routes.auth import api as auth

api.add_namespace(auth, path="/auth")
