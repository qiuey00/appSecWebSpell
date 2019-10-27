# from config import Config
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, PasswordField
import subprocess
import os


loginInfo = dict()

class registerForm(Form):
	uname = StringField(label='User Name', id='uname', validators=[validators.required()])
	pword = PasswordField(label='Password', id='pword', validators=[validators.required()])
	fa2 = StringField(label='2 Factor', id='2fa')
	submit = SubmitField('Submit')


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('register.html')

# @app.route('/register', methods=['GET','POST'])
# def register():
	

if __name__ == '__main__':
	app.run()