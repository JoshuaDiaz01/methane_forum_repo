from flask import Flask, session

app = Flask(__name__)
app.secret_key = "SHHHHHHHH."
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
