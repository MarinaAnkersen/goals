import datetime

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_restx import Resource, reqparse
from werkzeug.security import safe_str_cmp

from project.models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='This field cant be left blank')
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='This field cant be left blank')
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help='This field cant be left blank')
_user_parser.add_argument('active',
                          type=bool,
                          required=False,
                          help='This field can be left blank')
_user_parser.add_argument('created_datetime',
                          type=datetime,
                          required=False,
                          help='This field can be left blank')


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with this username is already exists."}, 400
        elif UserModel.find_by_email(data['email']):
            return {"message": "User with this email is already exists."}, 400
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User '{}' not found.".format(user_id)}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User '{}' not found.".format(user_id)}, 404
        user.delete_from_db()
        return {'message': "User '{}' deleted.".format(user_id)}, 200


class UserList(Resource):
    def get(self):
        users = [user.json() for user in UserModel.find_all()]
        return {'users': users}


# class UserLogOut(Resource):
#     @jwt_required
#     def post(self):
#         jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
#         BLACKLIST.add(jti)
#         return {"message": "Successfully logged out"}, 200
#
#
# class UserLogIn(Resource):
#     @classmethod
#     def post(cls):
#         # get data from parser
#         data = _user_parser.parse_args()
#
#         # find user in database
#         user = UserModel.find_by_username(data['username'])
#         # check password
#         if user and safe_str_cmp(user.password, data['password']):
#             access_token = create_access_token(identity=user.id, fresh=True)
#             refresh_token = create_refresh_token(user.id)
#             return {
#                     'access_token': access_token,
#                     'refresh_token': refresh_token
#                    }, 200
#         return {'message': 'Invalid credentials'}, 401
#
#
# class TokenRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         current_user = get_jwt_identity()
#         new_token = create_access_token(identity=current_user, fresh=False)
#         return {'access_token': new_token}, 200
