"""
Info: Permet de gérer les posts
"""
from models.PostModel import Post, PostCreate, PostUpdate
from sqlalchemy.orm import Session
from config.ConfigDatabase import SessionLocal
from fastapi import Depends, HTTPException, status, Request, Body

def getPost(post_id: int = None, db: Session = Depends(SessionLocal)):
    if post_id:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
        
        return post
    else:
        posts = db.query(Post).order_by(Post.created_at.desc()).all()
        return posts

def createPost(request: Request,post: PostCreate = Body(...), db: Session = Depends(SessionLocal)):
    new_post = Post( # Création d'un nouvel objet Post avec les paramètres reçus
        title=post.title,
        img=post.img,
        description=post.description,
        user_uuid=request.state.auth['user']['uuid']
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

def updatePost(request: Request, post: PostUpdate, db: Session = Depends(SessionLocal)):
    postDB = db.query(Post).filter(Post.id == post.id).first()
    if not postDB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    
    if str(request.state.auth['user']['uuid']) != str(postDB.user_uuid): # Vérification que l'utilisateur est bien l'auteur du post
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - You are not the author of this post')
    
    for key, value in vars(post).items():
        if key != "id" and value is not None:
            setattr(postDB, key, value)
    
    db.commit()
    db.refresh(postDB)
    
    return postDB

async def deletePost(request: Request, postId: int, db: Session = Depends(SessionLocal)):
    post = db.query(Post).filter(Post.id == postId).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    
    if str(request.state.auth['user']['uuid']) != str(post.user_uuid):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - You are not the author of this post')
    
    db.delete(post)
    db.commit()
    
    return {"status": "Post deleted"}

__all__ = ["getAllPost", "createPost", "updatePost", "deletePost"]