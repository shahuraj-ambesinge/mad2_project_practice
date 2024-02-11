from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
import os, secrets
from flask_cors import CORS    #using flask_cors CORS module we can control type of request and authrized acces
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash, check_password_hash
from celery.schedules import crontab

from application.data.database import db
from application.data.model import *
from application.security import security, user_datastore
import application.config as config

from application.apis.book.bookApi import AllBookAPI
from application.apis.book.bookApi import BookAPI
from application.apis.auth.loginAPI import loginAPI
from application.apis.auth.registerAPI import RegisterAPI
from application.apis.auth.loginAPI import RefreshTokenAPI
from application.apis.list.listAPI import AllTheaterAPI
from application.apis.list.listAPI import ListAPI


#create flask application instance
app = Flask(__name__, template_folder= './templates')
app.config.from_object(config)
app.app_context().push()

#intitialize flask CORS to retsrict requests
CORS(app, supports_credentials=True)

#CORS headers help to prevent unauthorized cross-origin requests and enhance the security of web applications. 
#They are essential when dealing with APIs or resources hosted on different domains.
#add CORS headers to every response to authorize cross platform request on browser.
#three types headers mentionaed below inside response.headrs['']

#add CORS to every request
@app.after_request
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = "http://localhost:8080"
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE"

    return response

@app.after_request
def after_request(response):
    response = add_cors_header(response)
    return response

db.init_app(app)

api = Api(app)
api.init_app(app)

#initialize jwt manager with flask application and integrate wit your application
JWTManager(app)

security.init_app(app, user_datastore)

#"/api/book" is the URL endpoint to which the AllBookAPI resource class is mapped.
#This means that when a request is made to the /api/book endpoint, the corresponding
# methods in the AllBookAPI class will be invoked to handle the request.
api.add_resource(AllBookAPI, "/api/book")   #only for post
api.add_resource(BookAPI, "/api/book/<int:book_id>")   #for get, put, delete

api.add_resource(RegisterAPI, "/api/register")  #for new user register
api.add_resource(loginAPI, "/api/login")  #api for user log in

api.add_resource(RefreshTokenAPI, "/api/refresh_token") # api for to ensure that only requests with a valid refresh token can access this endpoint

api.add_resource(AllTheaterAPI, "/api/list")
api.add_resource(ListAPI, "/api/list/<int:list_id>")
#def new_librarian():

with app.app_context():
    db.create_all()
    #new_librarian()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
