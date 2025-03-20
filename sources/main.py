"""
Fait par Léandre

Ce fichier permet de lancer l'API avec le serveur uvicorn.
"""
from fastapi import FastAPI
from config.ConfigManager import ConfigManager
from routes.AccountRouter import AccountRouter
from middlewares.AuthMiddleware import authenticateToken
from routes.PostRouter import PostRouter
from fastapi import Depends, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime
from contextlib import asynccontextmanager
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.cors import CORSMiddleware

startTime = datetime.now() # Récupération de l'heure actuelle

@asynccontextmanager # Fonction pour gérer le temps d'exécution de l'API
async def lifespan(app: FastAPI):
    execution_time = (datetime.now() - startTime).total_seconds() * 1000 # Calcul du temps d'exécution de l'API en millisecondes
    print(f"API started in {execution_time:.2f} ms") # Affichage du temps d'exécution de l'API en millisecondes
    yield

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False}, lifespan=lifespan) # Initialization d'une api FastAPI#app.include_router(AccountRouter, prefix="/account") # Création d'un groupe de route avec comme prefix "user" donc -> "http://localhost:7676/user/..."

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Création d'un schéma d'authentification
app.add_middleware(SessionMiddleware, secret_key=ConfigManager.APP()["SECRET_KEY"]) # Ajout du middleware de session
app.add_middleware(HTTPSRedirectMiddleware) # Ajout du middleware pour rediriger HTTP vers HTTPS
#
## Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],  # Permettre toutes les méthodes HTTP
    allow_headers=["*"],  # Permettre tous les headers
    allow_origins=["https://*"],  # Permettre uniquement les origines HTTPS A remplacer : (* -> domain.fr)
)

app.include_router(AccountRouter, prefix="/auth") # Création d'un groupe de route avec comme prefix "auth" donc -> "http://localhost:7676/auth/*"
app.include_router(PostRouter, prefix="/post", dependencies=[Depends(authenticateToken)]) # Création d'un groupe de route avec comme prefix "post" donc -> "http://localhost:7676/post/*", avec une dépendance pour vérifier le token et le compte en même temps

# code pour pouvoir lancer l'api avec le server uvicorn
if __name__ == "__main__":
    import uvicorn # Importation du serveur uvicorn
    uvicorn.run(app, host=ConfigManager.APP()["IP"], port=ConfigManager.APP()["PORT"], headers=[("Server", "API")]) # Utilisation des variables de l'applications puis le lancement de l'API