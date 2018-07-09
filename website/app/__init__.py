#any directory in python that includes a __init__.py file is considered a package
#a package can be imported. When you import a package, the __init__.py executes and
#defines what symbols the packages exposes to the outside world
from flask import Flask#the application object will be an instance of class Flask

app = Flask(__name__)#__name__ is a Python defined var set as the name of this module



#this import is a workaround to circular imports
from app import routes
