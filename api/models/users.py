from ..utils import db


class User(db.Model):
    """
    Représente un utilisateur dans la base de données.

    La classe `User` définit le modèle de données pour les utilisateurs dans la table `users`. 
    Elle utilise SQLAlchemy pour interagir avec la base de données.

    ### Attributs :
    - `id` (int) : Identifiant unique de l'utilisateur, clé primaire.
    - `email` (str) : Adresse e-mail de l'utilisateur, unique et non nul.
    - `username` (str) : Nom d'utilisateur, non nul.
    - `password_hash` (str) : Hash du mot de passe, non nul.
    - `is_active` (bool) : Indicateur si le compte est actif (par défaut : `True`).
    - `is_admin` (bool) : Indicateur si l'utilisateur est administrateur (par défaut : `False`).

    ### Méthodes :
    - `__repr__(self)` :
      Retourne une chaîne de caractères représentant l'objet `User` pour un affichage lisible,
      incluant l'identifiant et le nom d'utilisateur.

    - `save(self)` :
      Enregistre l'objet `User` dans la base de données. Ajoute l'utilisateur à la session et 
      valide les changements avec `db.session.commit()`.

    - `get_by_id(cls, id)` :
      Méthode de classe pour récupérer un utilisateur par son identifiant. Utilise `get_or_404` 
      pour obtenir l'utilisateur correspondant à l'identifiant fourni ou renvoie une erreur 404 
      si l'utilisateur n'existe pas.

    """
    __tablename__= 'users'

    id=db.Column(db.Integer(),primary_key=True)
    email=db.Column(db.String(80),nullable=False,unique=True)
    username = db.Column(db.String(25),nullable=False)
    password_hash=db.Column(db.Text(),nullable=False)
    is_active=db.Column(db.Boolean(),default=True)
    is_admin=db.Column(db.Boolean(),default=False)

    def __repr__(self):
        f"<User {self.id} {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)