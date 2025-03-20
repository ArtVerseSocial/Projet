"""
Info: permet de gérer les commentaires
"""
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from models.PostModel import Comment, CommentCreate, CommentUpdate
from config.ConfigDatabase import SessionLocal

def getAllCommentsOfPost(post_id: int, db: Session = Depends(SessionLocal)): # Fonction pour récupérer tous les commentaires d'un post
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

def createComment(request: Request, comment: CommentCreate, db: Session = Depends(SessionLocal)): 
    new_comment = Comment(
        post_id=comment.post_id,
        content=comment.content,
        user_uuid=request.state.auth["user"]["uuid"]  # Assuming you have a user_id field in your Comment model
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def updateComment(request: Request, post_id: int, comment: CommentUpdate, db: Session = Depends(SessionLocal)): # Fonction pour mettre à jour un commentaire
    user_uuid = request.state.auth["user"]["uuid"]
    commentDB = db.query(Comment).filter(Comment.post_id == post_id, Comment.user_uuid == user_uuid).first()
    
    if commentDB is None:
        return None  # Comment not found or user not authorized
    
    commentDB.content = comment.content
    
    db.commit()
    db.refresh(commentDB)
    return commentDB

def deleteComment(request: Request, comment_id: int, db: Session = Depends(SessionLocal)): # Fonction pour supprimer un commentaire
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        return None # Comment non trouvé
    
    db.delete(comment)
    db.commit()
    return comment

__all__ = ['getAllCommentsOfPost', 'createComment', 'updateComment', 'deleteComment'] # Exporte toutes les fonctions de ce fichier