from flask import Flask, redirect, url_for, render_template, request, session
from wtforms import Form, TextAreaField, validators, StringField, SubmitField, PasswordField
from flask_wtf import CSRFProtect
import subprocess

loginInfo = dict()

class registerForm(Form):
    uname = StringField(label='User Name', id='uname', validators=[validators.DataRequired()])
    pword = PasswordField(label='Password', id='pword', validators=[validators.DataRequired()])
    fa2 = StringField(label='2 Factor Number', id='2fa', validators=[validators.DataRequired(), validators.Length(min=10,max=10)])
    submit = SubmitField('Submit')

class spellForm(Form):
    textbox = TextAreaField('textbox', [validators.DataRequired()], id='inputtext')
    submit = SubmitField('Submit')

def create_app(config=None):
    app = Flask(__name__)
    csrf = CSRFProtect()
    app.secret_key = 'secret'
    csrf.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('home'))

    @app.route('/home', methods=['POST','GET'])
    def home():
        if session.get('logged_in') and request.method == 'GET':
            error='Logged In' 
            return render_template('home.html', error=error)
        if session.get('logged_in') and request.method == 'POST' and request.form['submit_button'] =='Log Out':
            error='Logged Out'
            session.pop('logged_in', None)
            return render_template('home.html', error=error)
        
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
                error = 'failure'
                return render_template('register.html', form=form, error=error)

            if uname not in loginInfo.keys():
                loginInfo[uname] = [[data.pword.data],[data.fa2.data]]
                error = 'success'
                return render_template('register.html', form=form, error=error)
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
                error='Success'
                return render_template('login.html', form=form, error=error)
            if uname not in loginInfo.keys() or pword not in loginInfo[uname][0]:
                error='Incorrect'
                return render_template('login.html', form=form, error=error)
            if fa2 not in loginInfo[uname][1]:
                error='Two-factor'
                return render_template('login.html', form=form, error=error)  
            else:
                error='Incorrect'
                return render_template('login.html', form=form, error=error)
        else:
            error = 'Please fill out login'
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
            inputText = open('words.txt','w')
            inputText.write(data)
            inputText.close()
            testsub = subprocess.Popen(['./a.out', 'words.txt', 'wordlist.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = testsub.stdout.read().strip()
            testsub.terminate()
            for line in output.decode('utf-8').split('\n'):
                misspelled.append(line.strip())
            return render_template('result.html', misspelled=misspelled, data=data)

        if not session.get('logged_in'):
            error='Must Log In'
            return render_template('spell_check.html', form=form,error=error)

        else:
            error='spellCheck else statement'
            return render_template('spell_check.html', form=form, error=error)
    return app

if __name__ == '__main__':
    app = create_app()
    app.debug=True
    app.run()