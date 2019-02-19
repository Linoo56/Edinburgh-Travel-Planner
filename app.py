import configparser
import bcrypt
from flask import Flask, request, flash, render_template, g, abort, redirect, session, url_for
app = Flask(__name__)
config = configparser.ConfigParser()
config.read('etc/defaults.cfg')


def init(app):
    config = configparser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)

        app.config['SECRET_KEY'] = config.get("config", "secret_key")
        app.config['GMAIL_PSW'] = config.get("config", "gmail_psw")
    except:
        return render_template('error.html')


@app.route('/')
def root():
    return render_template('home.html')



@app.route('/')
def root():
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    init(app)
    app.run(host="0.0.0.0", debug=True)
