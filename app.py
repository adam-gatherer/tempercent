from flask import Flask
from main import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    out_str = main_function()
    return f"<h1>{out_str}</h1>"
    
    
@app.route("/api")
def return_json():
    return "you tried"