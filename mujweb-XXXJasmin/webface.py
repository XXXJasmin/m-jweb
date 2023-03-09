from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools
from distutils.log import error
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random

from sqlitewrap import SQLite


app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
app.secret_key = b"x6\x87j@\xd3\x88\x0e8\xe8pM\x13\r\xafa\x8b\xdbp\x8a\x1f\xd41\xb8"


slova = ("Super", "Perfekt", "Úža", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "uživatel" in session:
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

@app.route("/login/", methods=["GET"])
def login():
    jméno=request.args.get("jméno")
    heslo=request.args.get("heslo")
    print(jméno,heslo)
    return render_template('login.html')

@app.route("/login/", methods=["POST"])
def login_post():
    jmeno=request.form.get("jmeno")
    heslo=request.form.get("heslo")
    page = request.args.get('page')

    with SQLite('data.db') as cur:
        cur.execute('SELECT passwd FROM user WHERE login = ?', [jmeno])
        ans= cur.fetchall()
        print(ans)

    if ans and check_password_hash( ans[0][0], heslo):
        flash('Jsi přihlášen!', 'message')
        session["uživatel"] = jmeno
        if page:
            return redirect(page)
    else:
        flash('Nesprávné přihlašovací údaje', 'error')
    if page:
        return redirect(url_for("login", page=page))
    return redirect(url_for('login'))

@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session.pop("uživatel", None)
    flash('Byl jsi odhlášen!')
    return redirect(url_for('main'))

@app.route("/registrace/", methods=['GET'])
def registrace():
    return render_template("registrace.html")

@app.route("/registrace/", methods=['POST'])
def registrace_post():
    jmeno=request.form.get("jmeno")
    heslo=request.form.get("heslo")
    heslo2=request.form.get("heslo2")
    print(jmeno, heslo, heslo2)
    if not (jmeno and heslo and heslo2):
        flash('Je nutné vyplnit všechna políčka', 'error')
        return redirect(url_for("registrace"))

    if heslo != heslo2:
        flash('Obě hesla musí být stejná', 'error')
        return redirect(url_for("registrace"))
    heslo_hash =generate_password_hash(heslo)
    try:    
        with SQLite('data.db') as cur:
            cur.execute("INSERT INTO user (login,passwd) VALUES (?,?)", [jmeno,heslo_hash])
        flash('Právě jsi se zaregistroval.', 'message')
        flash('Jsi přihlášen....', 'message')
        session['uživatel'] = jmeno
        return redirect(url_for("index"))
    except sqlite3.IntegrityError:
        flash(f"Jméno {jmeno} již existuje. Vyberte jiné.", "error")

    return redirect(url_for("registrace"))


@app.route("/prispevky/", methods=["GET"])
def prispevky():
    if "uživatel" in session:
        with SQLite('data.db') as cur:
            res = cur.execute("SELECT text,user FROM prispevky")
            tabulka=res.fetchall()
        if not tabulka:
            tabulka=[]
        return render_template("prispevky.html", tabulka=tabulka)
    else:
        return redirect(url_for('login'))
    
@app.route("/prispevky/", methods=["POST"])
def prispevky_post():
    if "uživatel" in session:
        text=request.form.get("text")
        with SQLite('data.db') as cur:
            cur.execute("INSERT INTO prispevky (text,user) VALUES (?,?)", [text, session["uživatel"]])
        return redirect(url_for("prispevky"))
    else:
        return redirect(url_for('login'))