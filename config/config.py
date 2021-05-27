import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
# from middlewares.tokenDecode import TokenDecoder


app = Flask(__name__)
# app.wsgi_app = TokenDecoder(app.wsgi_app)


db_url = "mysql://root:123456@localhost:3306/sample"
port = 5000
host = "0.0.0.0"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# selecting app environment
# if os.getenv("ENV") == "test":
#     db_url = "mysql://root:123456@localhost:3306/sample"
#     port = 5000
#     host = "0.0.0.0"



# elif os.getenv("ENV") == "development":
#     db_url = "mysql://root:123456@localhost:3306/sample"
#     port = 5000
#     host = "0.0.0.0"
  


# elif os.getenv("ENV") == "production":
#     db_url = "mysql://root:123456@localhost:3306/sample"
#     port = 5000
#     host = "0.0.0.0"



# elif os.getenv("ENV") == "staging":
#     db_url = 'mysql://root:Welcome@123@104.199.146.29:3306/ordermanagement'
#     elastic_search_url = ''
#     port = 5000
#     host = "0.0.0.0"
#     web_url = ""



app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config['SECRET_KEY'] = '3b8d7b303173189153979542'
app.config['JWT_SECRET_KEY'] = 'ILOVECARATRED'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
# es = Elasticsearch(hosts=elastic_search_url)
# print(es)

jwt = JWTManager(app)



app.secret_key = "ILOVECARATRED"
ma = Marshmallow(app)
db.init_app(app)

