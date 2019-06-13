from flask import Flask
from flask_cors import CORS

app = Flask("terrible_blog")
app.secret_key = 'terribleblog'
CORS(app)