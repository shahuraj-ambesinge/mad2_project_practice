from flask import jsonify
import secrets
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from application.data.model import db, User

user_post_args = reqparse.RequestParser()
user_post_args.add_argument('u_mail', type = str, required = True, help = 'user mail is required !!')
user_post_args.add_argument('password', type = str, required = True, help = 'password is required to register new user !!')

class RegisterAPI():
    def post(resource):
        args = user_post_args.parse_args()
        u_mail = args.get('u_mail')
        password = args.get('password')

#check for user if already registered
        user = User.query.filter_by(u_mail=u_mail).first()
        if user:
            return jsonify({'status':'failed', 'message': "this email is already registered"})
        
        #generate encoding of password for user privacy using 'secret' module
        hash_password = generate_password_hash(password)
        
        # fs_uniquifier helps in creating secure and unique sessions for users.
        fs_uniquifier = secrets.token_hex(16)

        #add new user to User table if not registered already
        new_user = User(u_mail = u_mail, password = hash_password, fs_uniquifier = fs_uniquifier)

        #add and commit the changes made in database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'statues':'success', 'message':"user is successfully registered"})

