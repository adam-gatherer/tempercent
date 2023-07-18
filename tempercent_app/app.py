from flask import Flask, redirect, url_for, request, render_template
from main import main_function
app = Flask(__name__)


@app.route('/success/<post_code>')
def success(post_code):
    # return f'<h1>{main_function(post_code)}</h1>'
    temp_dict = main_function(post_code)
    if temp_dict["today_pct"] > 100:
        above_below = "above"
    elif temp_dict["today_pct"] < 100:
        above_below = "below"
    else:
        return render_template(
            'result.html',
            today_pct=temp_dict["today_pct"],
            above_below="in line with"
        )
    return render_template(
        'result.html',
        today_pct=temp_dict["today_pct"],
        above_below=above_below
    )


@app.route('/postcode',methods = ['POST', 'GET'])
def index_page():
    if request.method == 'POST':
        try:
            postcode = request.form['postcode']
            return redirect(url_for('success', post_code = postcode))
        except:
            return f'<h1>BAD POSTCODE</h1>'
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
    app.run(debug = False, host='0.0.0.0', port=5000)