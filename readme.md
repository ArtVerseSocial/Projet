# Welcome on ArtVerse

## Table of contents

<p align="center">
    <a href="#description">Description</a><br />
    <a href="#installation">Installation</a><br />
    <a href="#route-disponible">Route Disponible</a>
</p>

## Introduction

## Description

C'est une rest API (coté serveur), inspiré de pinterest, pour le concours trophée NSI, le but étant de répondre au besoin de partager son art, dessin et avoir des retours utilisateurs, pouvoir liker, commenter etc...
Et tout cela open source où chacun est libre de faire le client pour cette API, c'est en quelque sorte aussi un défi pour les débutants qui souhaite s'entrainer sur les api et les clients qui y font des requêtes !

## Schema
[Schema](docs/schema.png)

## Installation

Clone `git clone https://github.com/ArtVerseSocial/ArtVerseAPI.git`

Go to the project directory : `$ cd SportInsight`

### Windows:
Install Python 3.7 or higher : [Python](https://www.python.org/downloads/)

Install Git : [Git](https://git-scm.com/downloads)

Install Virtualenv : `$ pip install virtualenv`

Create a virtual environment : `$ virtualenv -p python3.11 .venv `

Activate the virtual environment : `$ .\.venv\Scripts\activate`

### Linux:

If you not find package python3.11: `sudo add-apt-repository ppa:deadsnakes/ppa` Then `sudo apt update`

Install python3.11 and other dependencies: `apt install -y python3.11-venv python3.11-dev libpq-dev gcc`

Install Virtualenv : `$ pip install virtualenv`

Create a virtual environment : `$ virtualenv -p python3.11 .venv `

On Linux you need to install python3.11 before create the virtual env

Activate the virtual environment: `$ source .venv/bin/activate`

==============================

Install Dependencies : `$ (.venv) > pip install -r requirements.txt`

Start Application : `$ (.venv) > python3 main.py`

## Route disponible

#### Swagger Docs:

/auth/login?email="(email)"&password="(password)"

/auth/refresh

/auth/new

/art/post

/art/delete

/art/edit

```
Plus d'informations concernant la documention : <ip_de_l_api>/docs

Lorsque celle-ci est démarré
```
