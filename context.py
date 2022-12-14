from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from flask import Blueprint
from diophila import OpenAlex
from flask_mail import Mail

import config

# Create Flask App and Swagger UI
app = FlaskAPI("TTTT", template_folder='result')
app_blueprint = Blueprint('api', __name__, url_prefix='/v1')
swagger = Api(app_blueprint, version='1.0', doc='/swagger',
              title='TTTT Literature Search Backend API')
app.register_blueprint(app_blueprint)
CORS(app)  # 接受跨域


app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://'+config.db_user + ':' + config.db_passwd + \
    '@'+config.db_host+':' + \
    str(config.db_port)+'/'+config.db_database+'?charset=utf8'
app.secret_key = 'Buaa2022'
db = SQLAlchemy(app)

openAlex = OpenAlex()

app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False
app.config["MAIL_SERVER"] = "smtp.qq.com"
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config["MAIL_USERNAME"] = "2318942949@qq.com"
app.config["MAIL_PASSWORD"] = "efenlcaarkbidjgf"

mail = Mail(app)
