from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta
from flask import jsonify
#from flask.ext.mail import Mail, Message
from celery import Celery

from security import authenticate, identity
from resources.user import UserRegister
from resources.issue import Issue, IssueCreate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'some_secret_key'


#JWT endpoint for authentication
app.config['JWT_AUTH_URL_RULE'] = '/authenticate'
# config JWT to expire in an hour
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /authenticate

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                        'access_token': access_token.decode('utf-8'),
                        'user_id': identity.email
                   })
@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
                       'message': error.description,
                       'code': error.status_code
                   }), error.status_code

api.add_resource(UserRegister, '/register')
#@user.route('/<user_id>', defaults={'username': None})
#api.add_resource(Issue, '/issue/', defaults={'issue_id' : None})
#api.add_resource(Issue, '/issue/<int:issue_id>', defaults={'issue_id' : None})
#api.add_resource(Issue, '/issue', '/issue/<int:issue_id>')
api.add_resource(IssueCreate, '/issue/')
api.add_resource(Issue, '/issue/<int:issue_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=8000, debug=True)
