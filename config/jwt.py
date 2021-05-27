import jwt
import datetime
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


def jwt_token(check_user_exist, userId):
    '''
    create access_token and refresh token
    '''
    try:
        access_expires = datetime.timedelta(minutes=20)
        refresh_token = datetime.timedelta(hours=10)
        access_token = create_access_token(identity={"userdetails": check_user_exist, "userId": userId}, expires_delta=access_expires)
        refresh_token = create_refresh_token(identity={"userdetails": check_user_exist, "userId": userId}, expires_delta=refresh_token)
        return {
            "accessToken": access_token,
            "refreshToken": refresh_token
        }

    except Exception as identifier:
        # Logger.create_error_log('jwt', str(e))
        return {"success":False,"message":str(identifier)}


def encode_auth_token(id) -> str:
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': id
        }
        return jwt.encode(
            payload,
            'ILOVECARATRED',
            algorithm='HS256'
        )
    except Exception as e:
        # Logger.create_error_log('jwt', str(e))
        return {"success":False,"message":str(e)}


def decode_auth_token(auth_token: str) -> str:
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, 'ILOVECARATRED',)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return {"success":False,"message":'Signature expired. Please log in again.'}
    except jwt.InvalidTokenError:
        return {"success":False,"message":'Invalid token. Please log in again'}


def jwt_response_token(data):
    '''
    create access_token and refresh token
    '''
    try:
        access_expires = datetime.timedelta(days=1)
        token = create_access_token(identity={"data":data}, expires_delta=access_expires)
        return {"token": token}

    except Exception as identifier:
        # Logger.create_error_log('jwt', str(e))
        return {"success":False,"message":str(identifier)}
