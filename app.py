import flask
from flask import Flask, redirect, url_for
from flask_login import current_user, login_user, logout_user, LoginManager, UserMixin, login_required


app = Flask(__name__)
app.secret_key = b"1234"
login_manager = LoginManager()
login_manager.init_app(app)

users = {"foo@bar": {"password": "secret"}}


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    user.exists = True
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return
    user = User()
    user.id = email
    user.exists = True

    user.is_authenticated = request.form["password"] == users[email]["password"]
    return user


@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = flask.request.form['email']
    user = User()
    user.id = email
    user.exists = email in users
    if user.exists and flask.request.form['password'] == users[email]['password']:
        login_user(user)
        return redirect(url_for('secret'))

    return redirect(url_for("login"))


@app.route("/secret")
@login_required
def secret():
    return "Logged in as " + current_user.id


@app.route("/logout")
def logout():
    logout_user()
    return "logged out"


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True, port=8888)
