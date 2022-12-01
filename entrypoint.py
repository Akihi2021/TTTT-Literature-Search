import config


##################################################
# project main entrypoint
##################################################

from flask import Blueprint
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from routes import hello, paper
import config
from main import app, swagger
from rest import AppJSONEncoder

if __name__ == "__main__":
    # run Flask App
    app.json_encoder = AppJSONEncoder
    app.run(debug=True, port=config.server_port, host="0.0.0.0", use_reloader=True)
