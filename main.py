from flask import Flask, render_template, request, url_for, redirect, flash
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import smtplib
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class ContactForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    subject = StringField('Subject', [DataRequired()])
    message = TextAreaField('Message', [DataRequired()])
    submit = SubmitField('Submit')


def send_email(name, email, subject, message):
    msg = f'Subject: (Contact form submission): {subject}\n\nName: {name}\n\nEmail: {email}\n\nMessage: {message}'
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        # connection.set_debuglevel(10)
        connection.login(user='houseofel310@gmail.com', password='yokqmdsswrtfwjlu')
        connection.sendmail(from_addr='houseofel310@gmail.com', to_addrs='jleos310@gmail.com',
                            msg=msg)
        connection.close()
        print('Email sent!')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        send_email(form.name.data, form.email.data, form.subject.data, form.message.data)
        flash('Your message has been sent.')
        return redirect(url_for('home') + '#contact')
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
