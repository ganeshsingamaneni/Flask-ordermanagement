from flask import request
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from config.config import db
from config.logger import Logger
from models.views import View
from schemas.view_schema import GetAddViewSchema, AddViewValidator, UpdateViewValidator
# from seeder.seed import seedViews

class GetAddViews(Resource):
    def __init__(self):
        pass
    # View get call

    def get(self):
        try:
            obj = db.session.query(View).order_by(View.id).all()
            if obj:
                schema = GetAddViewSchema(many=True)
                data = schema.dump(obj).data
                return {"success":True,"data":data}
            else:
                return {"success":False,"message":"No data found"}
        except Exception as e:
            Logger.create_error_log("getaddviews", str(e))
            return {"success":False,"message":str(e)}
    # View post call
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()           
            req_data = request.get_json()
            req_data["createdBy"] = current_user["userId"]
            validate_schema = AddViewValidator()
            errors = validate_schema.validate(req_data)
            if errors:
                return Response.return_response('error', str(errors), 400,"Bad Request")
            view_exist = ViewUtility.check_view_name_exist(req_data['name'])
            if view_exist:
                return Response.return_response('success', {}, 200,"View already exists")
            schema = GetAddViewSchema()
            obj = schema.load(
                req_data, session=db.session).data
            db.session.add(obj)
            db.session.commit()
            data = schema.dump(obj).data
            return Response.return_response('success', data, 200)
        except Exception as e:
            Logger.create_error_log("getaddviews", str(e))
            return Response.return_response('Error', None, 500)


class GetUpdateViews(Resource):
    def __init__(self):
        pass

    # View get call based on id
    def get(self, id):
        try:
            obj = View.query.filter(View.id == id).one_or_none()
            if obj is not None:
                schema = GetAddViewSchema()
                data = schema.dump(obj).data
                return Response.return_response('success', data, 200)
            else:
                return Response.return_response('success', [], 200,"No data found")
        except Exception as e:
            Logger.create_error_log("getupdateviews", str(e))
            return Response.return_response('Error', None, 500)



    # View update call
    @jwt_required
    def put(self, id):
        try:
            current_user = get_jwt_identity()
            req_data= request.get_json()
            req_data["updatedBy"] = current_user["userId"]
            obj = db.session.query(View).filter_by(id = id).first()
            if not obj:
                return Response.return_response('success', [], 200,"No data found")
            validate_schema = UpdateViewValidator()
            errors = validate_schema.validate(req_data)
            if errors:
                return Response.return_response('error', str(errors), 400,"Bad Request")
            view_exist = ViewUtility.check_view_name_exist_for_update(req_data['name'], id)
            if view_exist:
                return Response.return_response('success', {}, 200,"View already exists")
            obj_view = db.session.query(View).filter_by(id = id).update(req_data)
            db.session.commit()
            view_obj = View.query.filter(View.id == id).one()
            view_schema = GetAddViewSchema()
            data = view_schema.dump(view_obj).data
            return Response.return_response('success', data, 200)
        except Exception as e:
            Logger.create_error_log("getupdateviews", str(e))
            return Response.return_response('Error', None, 500)


class ViewSeed(Resource):
    '''
    call to seed the role data
    '''

    def get(self):
        try:
            a = seedViews()
            if a:
                return Response.return_response('success', [], 200, "Roles seeded")
            else:
                return Response.return_response('success', [], 200, 'no data seeded')
        except Exception as e:
            # Logger.create_error_log("getupdateroles", str(e))
            return Response.return_response('Error', None, 500)
