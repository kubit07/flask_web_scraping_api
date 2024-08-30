from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .scraping.views import get_departure_time_arrival_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed

def create_app(config=config_dict['dev']):
    """
    Crée et configure une instance de l'application Flask.

    Cette fonction initialise une instance de l'application Flask avec la configuration spécifiée,
    configure la base de données, les migrations, l'API avec les espaces de noms et la gestion des erreurs.

    ### Paramètres :
    - `config` (object) : Configuration à appliquer à l'application Flask. Par défaut, utilise 
      la configuration de développement définie dans `config_dict['dev']`.

    ### Retourne :
    - `Flask` : L'application Flask configurée.

    ### Détails :
    1. Initialise l'application Flask.
    2. Applique la configuration fournie à l'application.
    3. Initialise la connexion à la base de données avec `db`.
    4. Configure la gestion des migrations de la base de données avec `Migrate`.
    5. Configure l'API REST avec `Api`, y compris les autorisations JWT pour l'authentification.
    6. Ajoute les espaces de noms pour les routes API.
    7. Configure la gestion des erreurs pour les erreurs 404 et 405.
    8. Configure le contexte de shell pour faciliter l'accès à la base de données et aux modèles.

    ### Configuration de l'API :
    - **Bearer Auth** : Authentification par jeton JWT avec un en-tête `Authorization` de type `apiKey`.

    ### Gestion des erreurs :
    - **404 Not Found** : Retourne un message d'erreur lorsque la route demandée n'existe pas.
    - **405 Method Not Allowed** : Retourne un message d'erreur lorsque la méthode HTTP demandée n'est pas autorisée.

    ### Contexte du shell :
    - Ajoute les objets `db` et `User` au contexte du shell pour un accès facile en ligne de commande.
    """

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
    api.add_namespace(get_departure_time_arrival_namespace)

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

