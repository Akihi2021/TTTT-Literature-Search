from flask import Blueprint
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS

import config


# create Flask App and Swagger UI
app = FlaskAPI("tttt", template_folder='result')
app_blueprint = Blueprint('api', __name__, url_prefix='/tttt/v1')
api = Api(app_blueprint, version='1.0', doc='/api', title='TTTT API', description='API for TTTT Literature Search')
app.register_blueprint(app_blueprint)
CORS(app)  # 接受跨域


# db = SQLAlchemy(app)
db = SQLAlchemy()
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://'+config.db_user + ':' + config.db_passwd + \
    '@'+config.db_host+':' + \
    str(config.db_port)+'/'+config.db_database+'?charset=utf8'


