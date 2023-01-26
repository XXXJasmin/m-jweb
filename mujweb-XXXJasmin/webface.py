from flask import Flask, render_template, request, redirect, url_for, session
import functools

# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
app.secret_key = b"x6\x87j@\xd3\x88\x0e8\xe8pM\x13\r\xafa\x8b\xdbp\x8a\x1f\xd41\xb8"


slova = ("Super", "Perfekt", "Úža", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def main():
    return render_template("base.html")


@app.route("/experimenty/")
def experimenty():
    return render_template("experimenty.html")


@app.route("/fotografie/")
def fotografie():
    return render_template("fotografie.html", slova=slova)


@app.route("/text/")
def text():
    return """

<h1>Text</h1>

<p>toto je text</p>

"""
