from config import Config
from flask import Flask, render_template, flash, request
import subprocess
import os


loginInfo = dict()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('register', methods=['GET','POST'])
def register():
	


if __name__ == '__main__':
    app.run()