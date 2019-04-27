from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
from user import User

app = Flask(__name__)
db = DBHelper()
ph = PasswordHelper()
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = '16ef17a2794f1d1c9b6f9738e88c72e7268bcfb5'


@login_manager.user_loader
def load_user(user_id):
  user_password = db.get_user(user_id)
  if user_password:
    return User(user_id)

@app.route('/login', methods=['POST'])
def login():
  email = request.form.get('email')
  password = request.form.get('password')
  stored_user = db.get_user(email) # Get the users email, salt, and hash and store it in stored_user variable, this return a dictionary
  if stored_user and ph.validate_password(password, stored_user['salt'], stored_user['hashed']): # Then whe check: if ther is a stored_user dictionary and this ph.validate_password funtion first create a hash and then check if it's maches the main users hash - return True or False
    user = User(email) # Whe created the user.
    login_user(user, remember=True) # Whe login the user.
    return redirect(url_for('account')) # Then redirect them to account page.
  return home() 

@app.route('/register', methods=['POST'])
def register():
  email = request.form.get('email')
  pw1 = request.form.get('password')
  pw2 = request.form.get('password2')
  if not pw1 == pw2:  # Checks if the two password inputs are the same if not then redirect to home page.
    return redirect(url_for('home'))
  if db.get_user(email): # Checks if there is a user with the same email if the is then redirect to home page.
    return redirect(url_for('home'))
  salt = ph.get_salt() # Make a salt - random simbols.
  hashed = ph.get_hash(pw1 + salt) # Make a hash with our password and salt.
  db.add_user(email, salt, hashed) # Add the email, salt, and hash to our database.
  return redirect(url_for('home')) # Then redirect to home page.

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('home'))

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/account')
@login_required
def account():
  return 'You are logged in'




if __name__ == '__main__':
  app.run(port=8000, debug=True)