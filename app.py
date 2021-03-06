from flask import Flask, redirect, url_for, render_template, request, session, make_response
from wtforms import Form, TextAreaField, validators, StringField, SubmitField, PasswordField
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_wtf import CSRFProtect
import subprocess
from datetime import *
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

loginInfo = dict()

class registerForm(Form):
    uname = StringField(label='User Name', id='uname', validators=[validators.DataRequired()])
    pword = PasswordField(label='Password', id='pword', validators=[validators.DataRequired()])
    fa2 = StringField(label='2 Factor Number', id='2fa', validators=[validators.DataRequired(), validators.Length(min=10,max=11)])
    submit = SubmitField('Submit')

class spellForm(Form):
    textbox = TextAreaField('textbox', [validators.DataRequired()], id='inputtext')

class workCheckForm(Form):
    textbox = TextAreaField('textbox', [validators.DataRequired(message="User To Check"),validators.Length(max=20000)], id='inputtext')

class userCheckForm(Form):
    textbox = TextAreaField('textbox', [validators.DataRequired(message="User to Check"),validators.Length(max=20)], id='inputtext')    

class User(UserMixin):
    def __init__(self, username):
        self.id = username


app = Flask(__name__)
app.secret_key = 'secret'
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect()
csrf.init_app(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spell.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class userTable(db.Model,UserMixin):
    user_id = db.Column(db.Integer(),unique=True,nullable=False,primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    password = db.Column(db.String(20),nullable=False)
    multiFactor = db.Column(db.String(11),nullable=False)
    registered_on = db.Column('registered_on', db.DateTime)
    accessRole = db.Column(db.String(50))
    def get_id(self):
        return self.user_id
    def get_active(self):
        return True
class loginHistory(db.Model):
    login_id = db.Column(db.Integer(),unique=True,nullable=False,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer(),db.ForeignKey("user_table.user_id"),unique=False)
    username = db.Column(db.String(20), unique=False,nullable=False)
    logStatus = db.Column(db.String(20))
    loggedIn = db.Column(db.DateTime)
    loggedOut = db.Column(db.DateTime)
class spellCheckHistory(db.Model):
    queryID= db.Column(db.Integer(),unique=True,nullable=False,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20), unique=False,nullable=False)
    queryText = db.Column(db.String(1000), unique=False,nullable=False)
    queryResults = db.Column(db.String(1000), unique=False,nullable=False)

db.drop_all()
db.create_all()
Admin = userTable(username='admin',password= bcrypt.generate_password_hash('Administrator@1').decode('utf-8'),multiFactor='12345678901',accessRole='admin')
db.session.add(Admin)
db.session.commit()

@login_manager.user_loader
def user_loader(user_id):
    return userTable.query.get(user_id)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home', methods=['POST','GET'])
def home():
    if session.get('logged_in') and request.method == 'GET':
        error='Logged In' 
        response = make_response(render_template('home.html', error=error))
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

    if session.get('logged_in') and request.method == 'POST' and request.form['submit_button'] =='Log Out':
        userLoginToAdd = loginHistory(logStatus='LoggedOut', username=current_user.username,loggedOut=datetime.now())
        db.session.add(userLoginToAdd)
        db.session.commit()
        error='Logged Out'
        session.pop('logged_in', None)
        logout_user()
        response = make_response(render_template('home.html', error=error))
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
    
    else:
        error='Not Logged In'
        response = make_response(render_template('home.html', error=error))
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

@app.route('/register', methods=['GET','POST'])
def register():
    form = registerForm()
    data = registerForm(request.form)
    if request.method == 'POST' and data.validate():
        uname = data.uname.data
        pword = data.pword.data
        fa2 = data.fa2.data
        hashPass = bcrypt.generate_password_hash(pword).decode('utf-8')

        if userTable.query.filter_by(username=('%s' % uname)).first() == None:
            User = userTable(username=uname, password=hashPass,multiFactor=fa2,registered_on=datetime.now(),accessRole='user')
            db.session.add(User)
            db.session.commit()
            error="success"
            return render_template('register.html', form=form, error=error)
        else:
            dbUserCheck = userTable.query.filter_by(username=('%s' % uname)).first()
            if uname == dbUserCheck.username:
                print('User Already Exists')
                error='failure'
                return render_template('register.html', form=form, error=error)
    else:
        error=''
        return render_template('register.html', form=form, error=error)

@app.route('/login', methods=['POST','GET'])
def login():
    form = registerForm()
    data = registerForm(request.form)
    if request.method == 'POST' and data.validate() and not session.get('logged_in'): 
        uname = (data.uname.data)
        pword = (data.pword.data)
        fa2 = (data.fa2.data)
        if  userTable.query.filter_by(username=('%s' % uname)).first() == None:
            error='Incorrect'
            return render_template('login.html', form=form,error=error)
        else :
            dbUserCheck = userTable.query.filter_by(username=('%s' % uname)).first()
            if uname == dbUserCheck.username and bcrypt.check_password_hash(dbUserCheck.password,pword) and fa2 == dbUserCheck.multiFactor:
                session['logged_in'] = True
                login_user(dbUserCheck)
                userLoginToAdd = loginHistory(logStatus='LoggedIn', username=username,loggedIn=datetime.now())
                db.session.add(userLoginToAdd)
                db.session.commit()
                error="Successful Authentication"   
                return render_template('login.html', form=form,error=error)
            if pword != dbUserCheck.password:
                error='Incorrect'
                return render_template('login.html', form=form,error=error)
            if fa2 != dbUserCheck.multiFactor:
                error='Two-factor'
                return render_template('login.html', form=form,error=error) 
    if request.method == 'POST' and form.validate() and session.get('logged_in'): 
        error='Already Logged In'
        return render_template('login.html', form=form,error=error)  
    else:
        error=''
        return render_template('login.html', form=form,error=error) 

@app.route('/spell_check', methods=['POST', 'GET'])
def spell_check():
    form = spellForm()
    data = spellForm(request.form)
    misspelled = []
    if session.get('logged_in') and request.method == 'GET':
        error = ''
        response = make_response(render_template('spell_check.html', form=form, error=error))
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
    if session.get('logged_in') and request.method == 'POST' and request.form['submit_button'] == 'Check Spelling':
        data = (data.textbox.data)
        inputText = open('words.txt','w')
        inputText.write(data)
        inputText.close()
        spellCheck = subprocess.Popen(['./a.out', 'words.txt', 'wordlist.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        misspelledWords = spellCheck.stdout.read().strip()
        spellCheck.terminate()
        spellHistory = spellCheckHistory(username=current_user.username,queryText=data,queryResults=misspelledWords.decode('utf-8'))
        db.session.add(spellHistory)
        db.session.commit()
        for line in misspelledWords.decode('utf-8').split('\n'):
            misspelled.append(line.strip())
        response = make_response(render_template('result.html', misspelled=misspelled, data=data))
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
    if not session.get('logged_in'):
        error='Must Log In'
        response = make_response(render_template('spell_check.html', form=form,error=error))
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
    else:
        error='spellCheck else statement'
        response = make_response(render_template('spell_check.html', form=form, error=error))
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
    return app

@app.route('/history', methods=['GET','POST'])
def history():
    form = workCheckForm(request.form)
    if session.get('logged_in') and request.method =='POST':
        userQuery = form.textbox.data
        dbUserCheck = userTable.query.filter_by(username=('%s' % userQuery)).first()
        if current_user.accessRole=='admin':
            numqueries = spellCheckHistory.query.filter_by(username=('%s' % userQuery)).order_by(spellCheckHistory.queryID.desc()).first()
            numqueriesCount = numqueries.queryID
            allqueries =  spellCheckHistory.query.filter_by(username=('%s' % userQuery)).all()
            return render_template('history.html', numqueries=numqueriesCount,allqueries=allqueries,form=form)

    if session.get('logged_in') and request.method =='GET':
        try:
            numqueries = spellCheckHistory.query.filter_by(username=('%s' % current_user.username)).order_by(spellCheckHistory.queryID.desc()).first()
            numqueriesCount = numqueries.queryID
            allqueries =  spellCheckHistory.query.filter_by(username=('%s' % current_user.username)).all()
        except AttributeError:
            numqueriesCount = 0
            allqueries = ''
        return render_template('history.html', numqueries=numqueriesCount,allqueries=allqueries,form=form)
    else:
        return render_template('home.html')

@app.route("/history/<query>")
def queryPage(query):
    if request.method == 'GET':
        try:
            query = query.replace('query','')
            history = spellCheckHistory.query.filter_by(queryID=('%s' % query)).first()
            queryID = history.queryID
            uname = history.username
            text = history.queryText
            misspelled = history.queryResults
        except AttributeError:
            return render_template('home.html')
        return render_template('queryIDresults.html', queryID=queryID, uname=uname,text=text,misspelled=misspelled)

@app.route('/login_history', methods=['GET','POST'])
def login_history():
    form = userCheckForm(request.form)
    user = userTable.query.filter_by(username=('%s' % current_user.username)).first()

    if session.get('logged_in') and request.method =='GET' and user.accessRole=='admin':
        error = 'Authenticated User '
        return render_template('login_history.html', form=form, error=error)

    if session.get('logged_in') and request.method == 'POST' and request.form['submit_button'] == 'Check User Login History':
        search = (form.textbox.data)
        queryResults = loginHistory.query.filter_by(queryID=('%s' % search)).all()

        username = []
        loginTime = []
        logoutTime = []
        print(queryResults)

        for entry in queryResults:
            print(entry.logStatus)
            if entry.logStatus == 'LoggedIn':
                loginTime.append(entry.loggedIn)
            if entry.logStatus == 'LoggedOut':                    
                logoutTime.append(entry.loggedOut)

        if len(loginTime) > len(logoutTime):
            logoutTime.append("N/A")
        return render_template('login_history_results.html', login=loginTime, logout=logoutTime)
    else:
        error='Not Admin'
        return render_template('home.html', error=error)

if __name__ == '__main__':
    # app = Flask(__name__)
    # app = create_app()
    app.run(debug=True)