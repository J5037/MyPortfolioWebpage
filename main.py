from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('API_KEY')
Bootstrap5(app)


class ContactForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    subject = StringField('Subject', [DataRequired()])
    message = TextAreaField('Message', [DataRequired()])
    submit = SubmitField('Submit')


def send_webhook(name, email, subject, message):
    # webhook
    webhook = DiscordWebhook(
        url=os.environ.get('WEBHOOK'),)
    embed = DiscordEmbed(title="**Contact Info**", color='1a3e78')
    embed.set_author(name="Contact Form Response Received!",
                     icon_url="https://media.gettyimages.com/id/1253926432/vector/flashlight-warning-alarm-light-and-siren-light-flat-design-vector-design.jpg?s=612x612&w=0&k=20&c=yOj6Jpu7XDrPJCTfUIpQm-LWI9q9RWQB91s-N7CgQDQ=")
    embed.set_footer(text='Time Created')
    embed.add_embed_field(name="Name", value=f"{name}")
    embed.add_embed_field(name="Email", value=f"{email}", inline=True)
    embed.add_embed_field(name="Subject", value=f"{subject}", inline=False)
    embed.add_embed_field(name="Message", value=f"{message}", inline=False)
    embed.set_thumbnail(
        url="https://t4.ftcdn.net/jpg/05/25/22/63/360_F_525226337_x7lLRcnU08vDLkijRwgcbaIs8zCfDktC.jpg")
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()


@app.route('/', methods=['GET', 'POST'])
def home():
    year = datetime.datetime.now().year
    form = ContactForm()
    if form.validate_on_submit():
        if 'https://' in str(form.message.data):
            abort(400)
        else:
            send_webhook(form.name.data, form.email.data, form.subject.data, form.message.data)
            flash('Your message has been sent.')
            return redirect(url_for('home') + '#contact')
    return render_template('index.html', form=form, year=year)


if __name__ == '__main__':
    app.run(debug=False)
