from datetime import timedelta
import os
from decouple import config


# Définition des chemins de base pour les répertoires de fichiers scrapés en fonction du système d'exploitation
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
#BASE_DIR_DATA_SCRAPING_WINDOWS = (r"C:\Users\dvesa\data_scraping\data_scraping")
#BASE_DIR_DATA_SCRAPING_WINDOWS_STREAM = (r"G:\Stage M2")
BASE_DIR_DATA_SCRAPING_LINUX_STREAM = (r"/home/axelle/WebScraping")
BASE_DIR_DATA_SCRAPING_LINUX = (r"/home/axelle/WebScraping/data_scraping")

class Config:
    """
    Configuration de base pour l'application.

    Cette classe fournit les paramètres de configuration communs à toutes les configurations 
    (développement, test, production).

    ### Attributs :
    - `SECRET_KEY` : Clé secrète utilisée pour la gestion des sessions et la protection des données sensibles.
    - `JWT_ACCESS_TOKEN_EXPIRES` : Durée de validité du jeton d'accès JWT (90 jours).
    - `JWT_REFRESH_TOKEN_EXPIRES` : Durée de validité du jeton de rafraîchissement JWT (90 jours).
    - `SQLALCHEMY_TRACK_MODIFICATIONS` : Désactive le suivi des modifications pour améliorer les performances.
    - `JWT_SECRET_KEY` : Clé secrète utilisée pour signer les jetons JWT.
    """
    SECRET_KEY=config('SECRET_KEY', 'secret')
    # Token for 90 days 
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=90)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=90)
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')

class DevConfig(Config):
    """
    Configuration spécifique au développement.

    Cette classe hérite de `Config` et définit des paramètres spécifiques à l'environnement de développement.

    ### Attributs :
    - `DEBUG` : Active le mode debug pour l'application.
    - `SQLALCHEMY_ECHO` : Affiche les requêtes SQL dans les logs pour le débogage.
    - `SQLALCHEMY_DATABASE_URI` : URI de la base de données SQLite pour le développement.
    """
    DEBUG=config('DEBUG', cast=bool)
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR,'db.sqlite3')

class TestConfig(Config):
    """
    Configuration spécifique aux tests.

    Cette classe hérite de `Config` et définit des paramètres spécifiques à l'environnement de test.

    ### Attributs :
    - `TESTING` : Active le mode test pour l'application.
    - `SQLALCHEMY_DATABASE_URI` : URI de la base de données SQLite pour les tests.
    - `SQLALCHEMY_TRACK_MODIFICATIONS` : Désactive le suivi des modifications.
    - `SQLALCHEMY_ECHO` : Affiche les requêtes SQL dans les logs pour le débogage.
    """
    TESTING=True
    SQLALCHEMY_DATABASE_URI="sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True

class ProdConfig(Config):
    """
    Configuration spécifique à la production.

    Cette classe hérite de `Config` et est utilisée pour la configuration en environnement de production.
    Aucun paramètre spécifique n'est défini dans cette classe pour le moment.
    """
    pass

# Dictionnaire des configurations disponibles pour l'application
config_dict={
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}