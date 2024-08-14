from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed

def create_app(config=config_dict['dev']):

    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    authorizations={
        "Bearer Auth":{
            'type':"apiKey",
            'in':'header',
            'name':"Authorization",
            'description':"Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }

    migrate = Migrate(app,db)

    api=Api(app, title="Web Scraping API",
        description="A REST API for  data Web Scraping",
        authorizations=authorizations,
        security="Bearer Auth")

    api.add_namespace(auth_namespace, path='/auth')

    jwt=JWTManager(app)


    @api.errorhandler(NotFound)
    def method_not_allowed(error):
        return {"error": "Not Found"},404
    
    @api.errorhandler(MethodNotAllowed)
    def not_found(error):
        return {"error": "Method Not Allowed"},405

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User':User,
        }
    
    return app

