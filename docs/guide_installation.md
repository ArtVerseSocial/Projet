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
