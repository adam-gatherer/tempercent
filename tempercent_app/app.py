from flask import Flask, redirect, url_for, request, render_template
from ukpostcodeutils import validation
from main import main_function
app = Flask(__name__)


@app.route('/success/<post_code>')
def success(post_code):
    try:
        temp_dict = main_function(post_code)
    except:
        return render_template(
            'result.html',
            message=f'"{post_code}" does not look like a valid UK postcode 🤔'
        )
    if temp_dict["today_pct"] > 100:
        today_pct = temp_dict["today_pct"] - 100
        above_below = "above"
    elif temp_dict["today_pct"] < 100:
        today_pct = 100 - temp_dict["today_pct"]
        above_below = "below"
    else:
        return render_template(
            'result.html',
            message="Today's temperature is bang on the average over the past five years."
        )
    return render_template(
        'result.html',
        message=f'Today is {today_pct}% {above_below} the average over the past five years.'
    )


@app.route('/postcode',methods = ['POST', 'GET'])
def index_page():
    if request.method == 'POST':
        postcode = request.form['postcode']
        postcode = (postcode.replace(" ","")).upper()
        if not validation.is_valid_postcode(postcode):
            return render_template(
                'result.html',
                message=f'"{postcode}" does not look like a valid UK postcode.'
            )
    else:
        postcode = request.args.get('postcode')
    return redirect(url_for('success', post_code = postcode))


@app.route("/")
def main_page():
    return render_template('index.html')
    
    
@app.route("/api")
def api_page():
    return "Under construction lol"


if __name__ == '__main__':
    app.run(debug = False, host='0.0.0.0', port=5000)