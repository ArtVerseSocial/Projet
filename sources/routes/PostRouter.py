"""
Info : Fait un group avec le prefix "/post" pour les routes de post

Imaginé par Mathis et Léandre, fait par Léandre
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from sqlalchemy.orm import Session
from config.ConfigDatabase import SessionLocal
from models.PostModel import Post, PostCreate, PostUpdate, PostLike, CommentCreate, Comment, CommentUpdate
from middlewares.PostMiddleware import createPost, updatePost, deletePost, getPost
from middlewares.AuthMiddleware import authenticateToken
from middlewares.LikeMiddleware import switchLikeToPost
from middlewares.CommentMiddleware import createComment
import base64

PostRouter = APIRouter() # Création d'une classe de router pour créer un groupe de routes

@PostRouter.get("/get") # Création d'une route GET pour récupérer tous les articles
def getArt(post_id: int = None, db: Session = Depends(SessionLocal)):
    posts = getPost(post_id, db) # Récupération des articles
    return posts # Retourne la liste des posts

@PostRouter.post("/create") # Création d'une route POST/create pour créer un nouveau post
async def postArt(request: Request,post: PostCreate, db: Session = Depends(SessionLocal)): # Définition de la fonction de la route
    if not post.title or not post.img or not post.description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - Missing parameters')
    
    try: # Vérification que l'image est bien en base64
        base64.b64decode(post.img, validate=True)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - img must be base64 encoded')
    
    new_post = createPost(request, post, db) # Création de l'article dans la base de données
    return new_post

@PostRouter.put("/update") # Création d'une route Post/update pour modifier un post
async def updateArt(request: Request, post: PostUpdate = Body(...), db: Session = Depends(SessionLocal)):
    # Vérification des paramètres
    if not post.id: # Vérification des paramètres
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - Missing parameters')
    
    return await updatePost(request, post, db)

@PostRouter.delete("/delete") # Création d'une route Post/delete pour supprimer un post
async def deleteArt(request: Request, postId: int, db: Session = Depends(SessionLocal)):
    if not postId: # Vérification des paramètres
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - Missing parameters')
    
    post = db.query(Post).filter(Post.id == postId).first()
    
    if not post: # Vérification que le post existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found - Post not found')
    
    return await deletePost(request, postId, db)

@PostRouter.post("/{post_id}/like") # Création d'une route Post/{post_id}/like pour liker un post
def like_post(request: Request, post_id: int, db: Session = Depends(SessionLocal)):
    if not post_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - Missing parameters')
    
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found - Post not found')
    
    return switchLikeToPost(request, post_id, db)

@PostRouter.get("/{post_id}/comment/getAll") # Création d'une route Post/{post_id}/comment/getAll pour récupérer tout les commentaires du post
def getAll(request: Request, post_id: int,db: Session=Depends(SessionLocal)):
    if not post_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - Missing parameters')

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found - Post not found')
    
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@PostRouter.post("/{post_id}/comment") # Création d'une route Post/{post_id}/comment pour commenter un post
def comment_post(request: Request, post_id: int, comment: CommentCreate, db: Session = Depends(SessionLocal)):
    if not post_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - Missing parameters')
        
    if not comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - Missing comment')
    
    existing_comment = db.query(Comment).filter(Comment.post_id == post_id, Comment.user_uuid == request.state.auth["user"]["uuid"]).first()
    
    if existing_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request - User has already commented on this post')
    comment.post_id = post_id
    return createComment(request, comment, db)

@PostRouter.put("/{post_id}/comment/update") # Création d'une route Post/{post_id}/comment/update pour modifier son commentaire du post
def updateComment(request: Request, post_id: int, comment: CommentUpdate, db: Session = Depends(SessionLocal)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found - Post not found')

    user_uuid = request.state.auth["user"]["uuid"]
    commentDB = db.query(Comment).filter(Comment.post_id == post_id, Comment.user_uuid == user_uuid).first()
    
    if commentDB is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found - Comment not found')
    
    commentDB.content = comment.content
    
    db.commit()
    db.refresh(commentDB)
    return commentDB

@PostRouter.delete("/{post_id}/comment/delete") # Création d'une route Post/{post_id}/comment/delete pour supprimer son commentaire du post
def deleteComment(request: Request, post_id: int, db: Session = Depends(SessionLocal)):
    user_uuid = request.state.auth["user"]["uuid"]
    comment = db.query(Comment).filter(Comment.post_id == post_id,Comment.user_uuid == user_uuid).first()
    
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found - Comment not found')
    
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted successfully"}