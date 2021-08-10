from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        # code = shortened name for URL
        return render_template('your_url.html', code=request.form['code'])
    else:
        return 'This is not valid'
