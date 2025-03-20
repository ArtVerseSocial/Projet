
"""
Info: Permet de gérer les "j'aimes"
"""

from fastapi import Request, status, Response, HTTPException, Depends, Query
from models.PostModel import Post, PostLike, CommentLike, Comment
from models.UserModel import User
from sqlalchemy.orm import Session
from config.ConfigDatabase import SessionLocal

def addLikeToPost(request: Request, post_id: int, db: Session = Depends(SessionLocal)):
    user = request.state.auth['user']
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    
    if db.query(PostLike).filter(PostLike.user_uuid == user['uuid'], PostLike.post_id == post_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - You already liked this post')
    
    new_like = PostLike(
        user_uuid=user['uuid'],
        post_id=post_id
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    return new_like

def removeLikeFromPost(request: Request, post_id: int, db: Session = Depends(SessionLocal)):
    user = request.state.auth['user']
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    
    like = db.query(PostLike).filter(PostLike.user_uuid == user['uuid'], PostLike.post_id == post_id).first()
    
    if not like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - You have not liked this post')
    
    db.delete(like)
    db.commit()
    
    return {"status": "Like removed"}

def switchLikeToPost(request: Request, post_id: int, db: Session = Depends(SessionLocal)):
    user = request.state.auth['user']
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    
    like = db.query(PostLike).filter(PostLike.user_uuid == user['uuid'], PostLike.post_id == post_id).first()
    
    if like:
        db.delete(like)
        db.commit()
        return {"status": "Like removed"}
    
    new_like = PostLike(
        user_uuid=user['uuid'],
        post_id=post_id
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    return { "status": "Like added" }

def getPostLikes(post_id: int = Query(...), db: Session = Depends(SessionLocal)):
    likes = db.query(PostLike).filter(PostLike.post_id == post_id).all()
    return likes

def addLikeToComment(request: Request, comment_id: int, db: Session = Depends(SessionLocal)):
    user = request.state.auth['user']
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')
    
    if db.query(CommentLike).filter(CommentLike.user_uuid == user['uuid'], CommentLike.comment_id == comment_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - You already liked this comment')
    
    new_like = CommentLike(
        user_uuid=user['uuid'],
        comment_id=comment_id
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    return new_like

def removeLikeFromComment(request: Request, comment_id: int, db: Session = Depends(SessionLocal)):
    user = request.state.auth['user']
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')
    
    like = db.query(CommentLike).filter(CommentLike.user_uuid == user['uuid'], CommentLike.comment_id == comment_id).first()
    
    if not like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - You have not liked this comment')
    
    db.delete(like)
    db.commit()
    
    return {"status": "Like removed"}

def switchLikeToComment(request: Request, comment_id: int, db: Session = Depends(SessionLocal)):
    user = request.state.auth['user']
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')
    
    like = db.query(CommentLike).filter(CommentLike.user_uuid == user['uuid'], CommentLike.comment_id == comment_id).first()
    
    if like:
        db.delete(like)
        db.commit()
        return {"status": "Like removed"}
    
    new_like = CommentLike(
        user_uuid=user['uuid'],
        comment_id=comment_id
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    return new_like

__all__ = ["addLikeToPost", "removeLikeFromPost", "getPostLikes", "addLikeToComment", "removeLikeFromComment", "switchLikeToPost", "switchLikeToComment"]