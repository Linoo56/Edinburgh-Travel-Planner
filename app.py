import gc
import cur as cur
from flask import Flask, g, render_template, request, flash, redirect, session, url_for
import sqlite3
from passlib.handlers.sha2_crypt import sha256_crypt
from wtforms import StringField, PasswordField, Form, validators

app = Flask(__name__)
db_location = 'plan.db'
app.secret_key = 'R\xa0<\x9b\xce/\xd2\x96oJ\xb9\xdb\xb1\xaf\x8f\x07A1\x9cB\xf6\x01\xf2\x16'


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db, cur


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


class RegistrationForm(Form):
    title = StringField('title')
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
    try:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            title = form.title.data
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))
            real_name = form.name.data

            db, cur = get_db()

            x = cur.execute(
                'SELECT * FROM user WHERE username = ?', [username])
            print(x)

            if x is not None and x.fetchall():
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                cur.execute("INSERT INTO user (title, username, email, password, real_name) VALUES(?,?,?,?,?)", [
                    title, username, email, password, real_name])
                db.commit()

                flash("Thanks for registering!")

                cur.close()
                db.close()
                gc.collect()  # collect garbage

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('home'))

        return render_template('register.html', form=form)

    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
