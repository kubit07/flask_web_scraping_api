from flask_restx import Namespace, Resource, fields
from flask import request
from api.models.users import User 
from werkzeug.security import generate_password_hash,check_password_hash
from http import HTTPStatus
from flask_jwt_extended import (create_access_token,
create_refresh_token,jwt_required,get_jwt_identity)
from werkzeug.exceptions import Conflict,BadRequest

# Définition de l'espace de noms pour l'authentification
auth_namespace=Namespace('auth', description='a namespace for authentification')

# Modèle pour la création d'un nouvel utilisateur
signup_model=auth_namespace.model(
    'User',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'password_hash':fields.String(required=True,description="A password"),
    }
)

# Modèle pour représenter un utilisateur (utilisé dans les réponses)
user_model=auth_namespace.model(
    'User',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'password_hash':fields.String(required=True,description="A password"),
        'is_active':fields.Boolean(description="This shows that User is active"),
        'is_admin':fields.Boolean(description="This shows that User is admin")
    }

)

# Modèle pour les informations de connexion (login)
login_model=auth_namespace.model(
    'Login',{
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password")
    }
)

@auth_namespace.route('/signup')
class SignUp(Resource):
    """
    Endpoint pour créer un nouveau compte utilisateur.
    """

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
            Create a new user account
        """
        data = request.get_json()

        try:
            
            new_user=User(
                username=data.get('username'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password'))
            )

            new_user.save()
            return new_user , HTTPStatus.CREATED

        except Exception as e:
            raise Conflict(f"User with email {data.get('email')} exists")

@auth_namespace.route('/login')
class Login(Resource):
    """
    Endpoint pour générer un paire de jetons JWT (accès et rafraîchissement).
    """

    def post(self):
        """
            Generate a JWT pair
        """
        pass

        data=request.get_json()


        email=data.get('email')
        password=data.get('password')

        user=User.query.filter_by(email=email).first()


        if (user is not None) and check_password_hash(user.password_hash,password):
            access_token=create_access_token(identity=user.email)
            refresh_token=create_refresh_token(identity=user.email)

            response={
                'acccess_token':access_token,
                'refresh_token':refresh_token
            }

            return response, HTTPStatus.OK
        
        raise BadRequest("Invalid Username or password")

@auth_namespace.route('/refresh')
class Refresh(Resource):
    """
    Endpoint pour rafraîchir le jeton d'accès JWT en utilisant un jeton de rafraîchissement.
    """

    @jwt_required(refresh=True)
    def post(self):

        email=get_jwt_identity()
        access_token=create_access_token(identity=email)

        return {'access_token':access_token},HTTPStatus.OK
