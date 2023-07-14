from flask import Flask, redirect, url_for, request, render_template
from .main import main_function
app = Flask(__name__)


@app.route('/success/<post_code>')
def success(post_code):
    return f'<h1>{main_function(post_code)}</h1>'


@app.route('/postcode',methods = ['POST', 'GET'])
def index_page():
    if request.method == 'POST':
        postcode = request.form['postcode']
        return redirect(url_for('success', post_code = postcode))
    else:
        postcode = request.args.get('postcode')
        return redirect(url_for('success', post_code = postcode))


@app.route("/")
def main_page():
    #out_str = main_function("EH51SG")
    #return f"<h1>{out_str}</h1>"
    return render_template('index.html')
    
    
@app.route("/api")
def api_page():
    return "Under construction lol"


if __name__ == '__main__':
    app.run(debug = True)