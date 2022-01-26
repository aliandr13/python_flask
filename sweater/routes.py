from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from sweater import app, db
from sweater.models import Message, User


@app.route("/", methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route("/main", methods=['GET'])
@login_required
def main():
    return render_template('main.html', messages=Message.query.all())


@app.route("/add_message", methods=['POST'])
@login_required
def add_message():
    text = request.form.get('text')
    tag = request.form.get('tag')
    db.session.add(Message(text=text, tags=tag))
    db.session.commit()

    return redirect(url_for('main'))


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main'))
        else:
            flash('Invalid password')
    else:
        flash('Please fill login and password')

    return render_template('login.html')


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == "POST":
        if not (login or password2 or password2):
            flash('Fill in all fields')
        elif password != password2:
            flash('Passwords do not match')
        else:
            password_hash = generate_password_hash(password)
            new_user = User(login=login, password=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.after_request
def after_request(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response
