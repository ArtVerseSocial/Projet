"""
Permet de gérer la connexion à la base de donnée
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.ConfigManager import ConfigManager
from models.UserModel import User as UserModel
from models.PostModel import Post as PostModel
import os

Config = ConfigManager.DATABASE() # Récupération des variables de la base de donnée

# Class pour pouvoir regrouper toute la configuration de la bdd (à ne pas toucher)
class ConfigDatabase:
    def __init__(self, url):
        try:
            self.engine = create_engine(url, echo=True) # Connexion à la base de donnée
            print("Success")
            UserModel.metadata.create_all(bind=self.engine) # Si table non créé, alors la créer
            PostModel.metadata.create_all(bind=self.engine) # Si table non créé, alors la créer
            self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine) # Création d'une session pour pouvoir manipuler la base de donnée
        except Exception as e:
            print(e)

    def get_session(self):
        return self.Session() # Mettre la session en public

# Utilisation de la classe ConfigDatabase pour créer la base de données et la session
config_db = ConfigDatabase(f'{Config["PROTOCOL"]}://{Config["USER"]}:{Config["PASSWORD"]}@{Config["HOST"]}:{Config["PORT"]}/{Config["NAME"]}')

if Config["PROTOCOL"] == "sqlite":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "../DATA")
    os.makedirs(DATA_DIR, exist_ok=True) 
    config_db = ConfigDatabase(f"sqlite:///{os.path.join(DATA_DIR, 'database.sqlite')}")

SessionLocal = config_db.get_session # Initialization des variables externes

#"""
#Permet de gérer la connexion à la base de donnée
#"""
#import os
#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
#from config.ConfigManager import ConfigManager
#from models.UserModel import User as UserModel
#from models.PostModel import Post as PostModel
#
## Définir le chemin vers le dossier DATA
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#DATA_DIR = os.path.join(BASE_DIR, "../DATA")
#os.makedirs(DATA_DIR, exist_ok=True)
#
## Utiliser SQLite avec un fichier dans le dossier DATA
#DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'database.sqlite')}"
#
## Configuration SQLAlchemy
#engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
## Class pour pouvoir regrouper toute la configuration de la bdd (à ne pas toucher)
#class ConfigDatabase:
#    def __init__(self, url):
#        try:
#            self.engine = create_engine(url, echo=True) # Connexion à la base de donnée
#            print("Success")
#            UserModel.metadata.create_all(bind=self.engine) # Si table non créé, alors la créer
#            PostModel.metadata.create_all(bind=self.engine) # Si table non créé, alors la créer
#            self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine) # Création d'une session pour pouvoir manipuler la base de donnée
#        except Exception as e:
#            print(e)
#
#    def get_session(self):
#        return self.Session() # Mettre la session en public
#
## Utilisation de la classe ConfigDatabase pour créer la base de données et la session
#config_db = ConfigDatabase(DATABASE_URL)
#
#SessionLocal = config_db.get_session # Initialization des variables externes