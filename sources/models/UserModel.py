"""
Fait par Marin
Création du model User, représentant une table dans la base de données
"""
from sqlalchemy import Column, Integer, String, DateTime, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
import uuid
from pytz import timezone

Base = declarative_base()

# Définition de la classe User, représentant une table dans la base de données
class User(Base):
    # Nom de la table dans la base de données
    __tablename__ = 'user'

    # Définition des colonnes de la table
    uuid = Column(UUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)  # Colonne UUID, clé primaire, générée automatiquement
    username = Column(String, nullable=False)  # Colonne Name en String
    email = Column(String, nullable=False, unique=True)  # Colonne Email en String
    password = Column(String, nullable=False)  # Colonne Password en String
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Colonne Created At, avec valeur par défaut définie à l'heure actuelle
    
    @staticmethod
    def get_current_time(arg1, arg2, target):
        paris_tz = timezone('Europe/Paris')
        return datetime.now(paris_tz)  # Fonction pour générer une date avec le fuseau horaire de Paris
    
    # Fonction pour générer un token
    # @staticmethod
    # def generateToken(arg1, arg2, target):
    #     alphabet = string.ascii_letters + string.digits
    #     target.token = ''.join(secrets.choice(alphabet) for _ in range(128))

event.listen(User, 'before_insert', User.get_current_time) # Ajoute d'un event listener pour générer une date avant l'insertion d'un nouvel utilisateur

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserDelete(BaseModel):
    email: str
    password: str