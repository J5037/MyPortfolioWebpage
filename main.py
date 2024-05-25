from flask import Flask, render_template, request, url_for, redirect, flash, abort
from flask_bootstrap import Bootstrap5
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired
import smtplib
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


@app.route('/')
def home():
    mode = request.args.get('darkModeSwitch')
    print(mode)
    return render_template('index.html', mode=mode)


if __name__ == '__main__':
    app.run(debug=True)
