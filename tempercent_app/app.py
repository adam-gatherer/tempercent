from flask import Flask
from .main import main_function
    
app = Flask(__name__)

@app.route("/")
def main_page():
    out_str = main_function("EH51SG")
    return f"<h1>{out_str}</h1>"
    
    
@app.route("/api")
def api_page():
    return "Under construction lol"


#@app.route("/api", postcode=str)
#def api_post(postcode):
#    return postcode