# from config import Config
from flask import Flask, redirect, url_for, render_template, flash, request, session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, PasswordField
import subprocess
import os


loginInfo = dict()

class registerForm(Form):
    uname = StringField(label='User Name', id='uname', validators=[validators.required()])
    pword = PasswordField(label='Password', id='pword', validators=[validators.required()])
    fa2 = StringField(label='2 Factor', id='2fa')
    submit = SubmitField('Submit')

class spellForm(Form):
    textbox = TextAreaField('textbox', [validators.DataRequired()], id='inputtext')
    submit = SubmitField('Submit')


app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)
app.secret_key = '1234567891234567893242341230498120348719035192038471902873491283510981834712039847124123940812903752903847129038471290835710289675413864310867135'
# csrf = CSRFProtect()
# csrf.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home', methods=['POST','GET'])
def home():
    if session.get('logged_in') and request.method =='POST' and request.form['submit_button'] =='Log Out':
        error='Logged Out'
        session.pop('logged_in', None)
        return render_template('home.html', error=error)
    # if session.get('logged_in'):
    #     error='Logged In'
    #     return render_template('home.html', error=error)
    else:
        error='Not Logged In'
        return render_template('home.html', error=error)


@app.route('/register', methods=['GET','POST'])
def register():
    form = registerForm()
    data = registerForm(request.form)
    if request.method == 'POST' and data.validate():
        uname = data.uname.data
        if uname in loginInfo.keys():
            error = 'Already Exists'
            return render_template('register.html', form=form, error=error)

        if uname not in loginInfo.keys():
            loginInfo[uname] = [[data.pword.data],[data.fa2.data]]
            error = "Registered"
            return render_template('home.html', error=error)
    else:
        error='Incomplete Form'
        return render_template('register.html', form=form, error=error)

@app.route('/login', methods=['POST','GET'])
def login():
    form = registerForm()
    data = registerForm(request.form)

    if request.method == 'POST' and data.validate() and not session.get('logged_in'): 
        uname = data.uname.data
        pword = data.pword.data
        fa2 = data.fa2.data
        if uname in loginInfo.keys() and pword in loginInfo[uname][0] and fa2 in loginInfo[uname][1]:
            session['logged_in'] = True
            error="Successful Authentication"
            return redirect(url_for('home'))

        if uname not in loginInfo.keys() or pword not in loginInfo[uname][0]:
            error='Incorrect'
            return render_template('login.html', form=form, error=error)
        if fa2 not in loginInfo[uname][1]:
            error='Two-Factor'
            return render_template('login.html', form=form, error=error)  
        else:
            error='Incorrect'
            return render_template('login.html', form=form, error=error)

    else:
        error = "Please fill out login"
        return render_template('login.html', form=form, error=error)


@app.route('/spell_check', methods=['POST', 'GET'])
def spell_check():
    form = spellForm()
    data = spellForm(request.form)
    misspelled = []

    if session.get('logged_in') and request.method == 'GET':
        error = ''
        return render_template('spell_check.html', form=form, error=error) 

    if session.get('logged_in') and request.method == 'POST' and request.form['submit_button'] == 'Check Spelling':
        data = (data.textbox.data)
        tempFile = open("temp.txt","w")
        tempFile.write(data)
        tempFile.close()
        testsub = subprocess.Popen(["./a.out", "temp.txt", "wordlist.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = testsub.stdout.read().strip()
        testsub.terminate()
        for line in output.decode('utf-8').split('\n'):
            misspelled.append(line.strip())
        return render_template('result.html', misspelled=misspelled, data=data)
        #except:
        #    return "errors"
        #return render_template('spell_check.html', form=form)

    if not session.get('logged_in'):
        error='Must Log In'
        return render_template('spell_check.html', form=form,error=error)

    else:
        error='spellCheck else statement'
        return render_template('spell_check.html', form=form, error=error)





if __name__ == '__main__':
    app.debug=True
    app.run()