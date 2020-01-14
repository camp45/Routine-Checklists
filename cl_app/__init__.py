from flask import Flask

app = Flask(__name__)

from cl_app import routes

