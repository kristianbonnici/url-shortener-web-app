from flask import Flask

app = Flask(__name__)
app.secret_key = 'to_be_hidden_if_put_to_production'
