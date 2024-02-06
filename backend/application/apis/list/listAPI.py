import json
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from flask_jwt_extended import jwt_required

from application.data.model import db,List

resource_field = {
    'list_id' : fields.Integer,
    'list_name' : fields.String,
    'list_disc' : fields.String,
}

list_post_args = reqparse.RequestParser()
list_post_args.add_argument('list_name', type=str)
list_post_args.add_argument('list_disc', type=str)

class AllTheaterAPI(Resource):
    @marshal_with(resource_field)
    def get(resources):
        lists = List.query.all()
        list_dict = []
        for list in lists:
            list_dict.append({'list_id' : list.list_id, 'list_name' : list.list_name, 'list_disc' : list.list_disc})
        return list_dict
  
    @marshal_with(resource_field)
    def post(resources):
        args = list_post_args.parse_args()
        list =List.query.filter_by(list_name = args['list_name']).first()
        if list:
            abort(409, message="List already exist")
        input = List(list_name = args['list_name'], list_disc = args['list_disc'])
        db.session.add(input)
        db.session.commit()
        return input, 201

class ListAPI(Resource):
    @marshal_with(resource_field)
    def get(self, list_id):
        list = List.query.filter_by(list_id = list_id).first()
        if not list:
            abort(404,message="There is no list with list_id:" +str(list_id))
        return list
    
    @marshal_with(resource_field)
    def put(self, list_id):
        args = list_post_args.parse_args()
        list = List.query.filter_by(list_id = list_id).first()
        if not list:
            abort(404, message="There is no list with list_id:" +str(list_id))

        if args['list_name']:
            list.list_name = args['list_name']
        
        if args['list_disc']:
            list.list_disc = args['list_disc']
        
        db.session.commit()
        return jsonify({'status':'success', 'message':"list is updated"})
    
    @marshal_with(resource_field)
    def delete(self, list_id):
        delete_list = List.query.filter_by(list_id = list_id).first()
        if delete_list:
            db.session.delete(delete_list)
            db.session.commit()
            return jsonify({'status':'success', 'message': "list is deleted in database"})
        else:
            return jsonify({'status':'failed', 'message': "list_id doesn't exists" + str(list_id)})

    


