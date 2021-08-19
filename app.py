from flask import Flask, render_template, request
from flask import redirect, url_for, flash, abort
from flask import session, jsonify  # for implementing sessions & cookies
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'to_be_hidden_if_put_to_production'


@app.route('/')  # homepage
def home():
    return render_template('index.html', codes=session.keys())


@app.route('/your-url', methods=['GET', 'POST'])  # submitted form page
def your_url():
    if request.method == 'POST':
        urls = {}

        # Open JSON file, if it already exists
        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls = json.load(url_file)

        # If trying to override existing code --> direct to home
        if request.form['code'] in urls.keys():
            flash("""That shortname has already been taken.
                     Please select another name.""")
            return redirect(url_for('home'))

        # Check if URL or FILE upload by user
        if 'url' in request.form.keys():
            # ========== URL ==========
            # key='code' : value={'url':'https://url'}
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            # ========== FILE ==========
            f = request.files['input_file']
            full_name = request.form['code'] + secure_filename(f.filename)

            # save file to 'user_files' directory
            f.save(os.getcwd() + '/static/user_files/' + full_name)
            # key='code' : value={'file':'filename'}
            urls[request.form['code']] = {'file': full_name}

        # open/create JSON file & save user's input
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)  # save url to JSON
            session[request.form['code']] = True  # save to cookies

        # code = shortened name for URL
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')  # Redirect to URL or FILE
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                # If URL
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                # Else FILE
                else:
                    return redirect(url_for('static', filename='user_files/'
                                            + urls[code]['file']))

    # If route not found --> return 404 PAGE
    return abort(404)


@app.errorhandler(404)  # route to our custom 404 PAGE
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
