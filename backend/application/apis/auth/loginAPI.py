from flask import jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password, hash_password
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


from application.data.model import db, User

user_post_args = reqparse.RequestParser()
user_post_args.add_argument('u_mail', type = str, required = True, help = 'user mail is required !!')
user_post_args.add_argument('password', type = str, required = True, help = 'password is required to register new user !!')


class loginAPI(Resource):
    def post(self):
        args = user_post_args.parse_args()     #parse and validate incoming JSON data for user login.
        u_mail = args.get('u_mail')
        password = args.get('password')

        user = User.query.filter_by(u_mail = u_mail).first()

        if user is None:
            return jsonify({'status': 'failed', 'message': "This email is not Registered"})
        
        if verify_password(password, user.password):
            return jsonify({'status': 'failed', 'message': "This password is wrong"})
        refresh_token = create_refresh_token(identity=user.user_id)
        access_token = create_access_token(identity=user.user_id)

        login_user(user)

        return({'status': 'failed', 'message': "This is user loged in successfully", 'access_token':access_token, 'refresh_token':refresh_token})


class RefreshTokenAPI(Resource):
    @jwt_required(refresh=True)    # to ensure that only requests with a valid refresh token can access this endpoint.
    def post(self):
        identity = get_jwt_identity()     #Get the user identity from the refresh token using get_jwt_identity.
        access_token = create_access_token(identity = identity)  #Create a new access token for the user.
        return jsonify({'access_token':access_token})       #Return a JSON response containing the new access token.
    

