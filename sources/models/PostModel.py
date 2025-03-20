"""
Fait par Marin
Création du model pour toutes les tables différentes tel que User, Post, Comment, Likes, dans la base de donnée   
"""
from sqlalchemy import Column, Integer, String, DateTime, event, BOOLEAN, ForeignKey, UniqueConstraint, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from pydantic import BaseModel
from models.UserModel import User
from pytz import timezone

Base = declarative_base()

@staticmethod
def get_current_time(arg1, arg2, target):
    paris_tz = timezone('Europe/Paris')
    return datetime.now(paris_tz)  # Fonction pour générer une date avec le fuseau horaire de Paris

class PostLike(Base): # Création de la table Likes pour les posts
    # Nom de la table dans la base de données
    __tablename__ = 'post_like'

    # Définition des colonnes de la table
    id = Column(Integer, primary_key=True, unique=True, nullable=False)  # Colonne ID, clé primaire, générée automatiquement
    user_uuid = Column(UUID, ForeignKey(User.uuid), nullable=False)  # Colonne user_id, clé étrangère référant à la table user
    post_id = Column(Integer, ForeignKey("post.id"), nullable=True)  # Colonne Likespost en Integer, clé étrangère référant à la table post

    __tableargs__ = (UniqueConstraint('user_uuid', 'post_id', name='unique_user_post'),)  # Contrainte d'unicité pour éviter les doublons 

class CommentLike(Base): # Création de la table Likes pour les posts
    # Nom de la table dans la base de données
    __tablename__ = 'comment_like'

    # Définition des colonnes de la table
    id = Column(Integer, primary_key=True, unique=True, nullable=False)  # Colonne ID, clé primaire, générée automatiquement
    user_uuid = Column(UUID, ForeignKey(User.uuid), nullable=False)  # Colonne user_id, clé étrangère référant à la table user
    comment_id = Column(Integer, ForeignKey("comment.id"), nullable=True)  # Colonne Likespost en Integer, clé étrangère référant à la table post
    
    __tableargs__ = (UniqueConstraint('user_uuid', 'comment_id', name='unique_user_comment'),)  # Contrainte d'unicité pour éviter les doublons

class Comment(Base):
    # Nom de la table dans la base de données
    __tablename__ = 'comment'

    # Définition des colonnes de la table
    id = Column(Integer, primary_key=True, unique=True, nullable=False)  # Colonne ID, clé primaire, générée automatiquement
    user_uuid = Column(UUID, ForeignKey(User.uuid), nullable=False)  # Colonne user_id, clé étrangère référant à la table user
    content = Column(String, nullable=False)  # Colonne contenu en String
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Colonne Created At, avec valeur par défaut définie à l'heure actuelle
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)  # Colonne post_id, clé étrangère référant à la table post
    
    like = relationship("CommentLike", backref="comment",cascade="all, delete-orphan")  # Relation avec la table CommentLike
    likes_count = column_property(
        select(func.count("comment_like.id")).filter("comment_like.comment_id" == id).scalar_subquery(),
        deferred=True,
    )
    
    __table_args__ = (UniqueConstraint('user_uuid', 'post_id', name='unique_user_content'),)  # Contrainte d'unicité pour éviter les doublons

class CommentCreate(BaseModel):
    content: str;
    post_id: int = None;

class CommentUpdate(BaseModel):
    content: str;

event.listen(Comment, 'before_insert', get_current_time) # Ajoute d'un event listener pour générer une date avant l'insertion d'un nouveau commentaire

# Définition de la classe Post, représentant une table dans la base de données
class Post(Base):
    # Nom de la table dans la base de données
    __tablename__ = 'post'

    # Définition des colonnes de la table
    id = Column(Integer, primary_key=True, unique=True, nullable=False)  # Colonne UUID, clé primaire, générée automatiquement
    title = Column(String, nullable=False)  # Colonne Title en String
    user_uuid = Column(UUID, ForeignKey(User.uuid), nullable=False)  # Colonne user_uuid, clé étrangère référant à la table user
    img = Column(String, nullable=False)  # Colonne Image en String (doit être en base64)
    description = Column(String, nullable=False)  # Colonne Description en String
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Colonne Created At, avec valeur par défaut définie à l'heure actuelle
    likes_count = column_property(
        select(func.count(PostLike.id)).filter(PostLike.post_id == id).scalar_subquery(),
        deferred=False,
    )
    comments_count = column_property(
        select(func.count(Comment.id)).filter(Comment.post_id == id).scalar_subquery(),
        deferred=False,
    )
    likes = relationship("PostLike", backref="post", cascade="all, delete-orphan")  # Relation avec la table PostLike (Likes)
    comments = relationship("Comment", backref="post", cascade="all, delete-orphan")  # Relation avec la table Comment (Commentaires)

class PostCreate(BaseModel): # Création d'une classe de modèle pour la création d'un post
    title: str
    img: str
    description: str

class PostUpdate(BaseModel): # Création d'une classe de modèle pour la mise à jour d'un post
    id: int
    title: str = None
    img: str = None
    description: str = None

event.listen(Post, 'before_insert', get_current_time) # Ajoute d'un event listener pour générer une date avant la création d'un nouveau post