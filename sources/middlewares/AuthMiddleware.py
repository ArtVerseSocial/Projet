"""
Info: Permet de gérer le système d'authentification
"""
import jwt
from config.ConfigManager import ConfigManager
from models.UserModel import User
from datetime import datetime, timedelta
from fastapi import Response, status, Request, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from config.ConfigDatabase import SessionLocal

Auth = ConfigManager.AUTH()

def tokenPayload(user):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - User not found')
    return {
        "uuid": str(user.uuid),
        "username": user.username,
        "email": user.email,
    }

expiredAccessToken = timedelta(hours=1)
expiredRefreshToken = timedelta(days=7)

def generateAccessToken(user):
    
    return jwt.encode(user, Auth["ACCESS_TOKEN"], algorithm='HS256')

def generateRefreshToken(user):
    return jwt.encode(user, Auth["REFRESH_TOKEN"], algorithm='HS256')

def formatJWT(token):
    parts = token.split('.')

    if len(parts) == 3:
        return True
    return False

def authenticateToken(request: Request, accessToken: str = Header(), db: Session = Depends(SessionLocal)):
    if not accessToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - Invalid Bearer token')

    try:
        if not formatJWT(accessToken):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - Invalid Format Bearer token')

        user = jwt.decode(accessToken, Auth["ACCESS_TOKEN"], algorithms=['HS256'])
        # Vérifie si l'utilisateur existe
        userDB = db.query(User).filter(User.uuid == user['uuid']).first()
        if not userDB:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - User not found')
        request.state.auth = request.state.auth if hasattr(request.state, 'auth') else {}
        request.state.auth['user'] = user

        if request.state.auth['user']['username'] == 'root' == userDB.username: # Vérifie si l'utilisateur est root
            request.state.auth['isRoot'] = True
        return True
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - Invalid Bearer token')
    except Exception as e:
        print('Erreur lors de la vérification du token :', e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - Invalid Bearer token')

async def refreshToken(token):
    if not formatJWT(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - Invalid Format Bearer token')

    try:
        user = jwt.decode(token, Auth["REFRESH_TOKEN"], algorithms=['HS256'])
        refreshedToken = generateRefreshToken(user)
        accessToken = generateAccessToken(user)
        return [accessToken, refreshedToken]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - Invalid Bearer token')

async def getUserWithToken(token):
    if not formatJWT(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - Invalid Format Bearer token')
    try:
        user = jwt.decode(token, Auth["ACCESS_TOKEN"], algorithms=['HS256'])
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - Invalid Bearer token')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized - Invalid Bearer token')

# Exporte des fonctions
__all__ = ['authenticateToken', 'generateAccessToken', 'generateRefreshToken', 'refreshToken']