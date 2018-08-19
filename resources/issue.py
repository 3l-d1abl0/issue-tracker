from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.issue import IssueModel
from models.user import UserModel
from new_celery.tasks import send_email_task
from celery import Celery
import smtplib
from sqlalchemy.exc import IntegrityError

from logger import logger

class Issue(Resource):
    @jwt_required()
    def get(self,issue_id):
        issue = IssueModel.find_by_id(issue_id)
        if issue:
            assigned_to = UserModel.find_by_id(issue.assigned_to).json()
            created_by = UserModel.find_by_id(issue.created_by).json()
            return {'issue_id': issue.id, 'title':  issue.title, 'description': issue.description, 'created_by': created_by['email'], 'assigned_to': assigned_to['email'], 'status': issue.status}, 200
            #return issue.json()
        return {'message': 'Issue not found'}, 404

    @jwt_required()
    def delete(self, issue_id):
        issue = IssueModel.find_by_id(issue_id)
        #created_by = UserModel.find_by_email(issue['created_by']).json()
        #print current_identity.id
        if issue:
            if issue.created_by == current_identity.id:
                issue.delete_from_db()
                return {'message': 'Issue Deleted !'}, 200
            else:
                return {'message': 'Unauthorized !'}, 403
        else:
            return {'message': 'Issue not found !'}, 404

    @jwt_required()
    def put(self, issue_id):

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=False, help="Issue Title cannot be left blank!")
        parser.add_argument('description',type=str, required=False, help="Issue Description cannot be left blank!")
        parser.add_argument('assigned_to',type=str, required=False, help="Issue Assignee email cannot be Blank !")
        parser.add_argument('status',type=str, required=False, help="This field cannot be left blank!")

        data = parser.parse_args()
        issue = IssueModel.find_by_id(issue_id)

        if issue:
            if issue.created_by == current_identity.id:

                #print data['assigned_to']
                assigned_to = UserModel.find_by_email(data['assigned_to'])
                if assigned_to:
                    issue.title = data['title'] if data['title'] else issue.title
                    issue.description = data['description'] if data['description'] else issue.description
                    issue.assigned_to = assigned_to.id if assigned_to.id else issue.assigned_to
                    issue.status = data['status'] if data['status'] else issue.status
                    issue.save_to_db()

                    try:
                        task = send_email_task.apply_async(args=[data['assigned_to'],issue.title,issue.description],countdown=720)
                    except Exception as e:
                        logger.debug(e)

                    return issue.json()
                else:
                    return {'message': 'User with email : {} does not Exist !'.format(data['assigned_to'])},400
            else:
                return {'message': 'Unauthorized !'}, 403
        else:
            return {'message': 'Issue not found !'}, 404

class IssueCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="Issue Title cannot be left blank!")
    parser.add_argument('description',type=str, required=True, help="Issue Description cannot be left blank!")
    parser.add_argument('assigned_to',type=str, required=True, help="Issue Assignee email cannot be Blank !")
    #parser.add_argument('author',type=str, required=True, help="This field cannot be left blank!")
    #parser.add_argument('status',type=str, required=True, help="This field cannot be left blank!")


    @jwt_required()
    def post(self):
        data = IssueCreate.parser.parse_args()

        #created_by = UserModel.find_by_email(data['author']).json()
        assigned_to = UserModel.find_by_email(data['assigned_to'])

        if assigned_to is None:
            return {"message": "user : {} is not registerd !".format(data['assigned_to']) }, 400

        assigned_to = assigned_to.json()
        issue = IssueModel(data['title'], data['description'], assigned_to['id'], current_identity.id, 'OPEN')
        try:
            issue.save_to_db()
            # send the email
            #print 'TO: {}'.format(data['assigned_to'])
            try:
                task = send_email_task.apply_async(args=[data['assigned_to'],data['title'],data['description']],countdown=720)
                #print task
            except Exception as e:
                logger.debug(e)

        except IntegrityError as e:
            logger.debug(e)
            return {"message": "Check if Issue is not Duplicate."}, 400
        except Exception as e:
            return {"message": "An error occurred while creating issue."}, 500


        #print issue.json()
        return {"message" : "Issue Created", "issue_id": issue.id, "title": data['title'], "description": data['description'], "assigned_to": data['assigned_to'] }, 201
