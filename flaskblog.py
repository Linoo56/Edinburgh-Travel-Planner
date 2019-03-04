from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import pymysql #<-- this is the connector between flask and mysql

app = Flask(__name__)

# Config MySQL
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='test',
                             db='myflaskapp',
                             cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

class RegisterForm(Form): #Set min/max length of fields
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.hash(str(form.password.data))

        # Create Cursor
        cur = connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username,
        password))

        # Commit to DB
        connection.commit()
        #Close Connection
        connection.close()
        flash('You are now registered and can log in', 'success')

        cur.close()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
