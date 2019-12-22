from flask import Flask, request, session, redirect, url_for, render_template, flash
from models import User, all_places

app = Flask(__name__)


@app.route("/")
def index():
    places = all_places()
    return render_template("index.html", places= places)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User(username)
        if not user.register(password):
            flash("Uzytkownik o podanej nazwie posiada juz konto.")
        else:
            flash("Rejestracja przebiegla pomyslnie.")
        return redirect(url_for("login"))


    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User(username)
        if not user.verify_password(password):
            flash("Podano nieprawidlowe dane")
        else:
            flash("Logowanie zakonczone sukcesem")
            session["username"] = user.username
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/add_place", methods=["POST"])
def add_place():

    placename = request.form["placename"]
    days = request.form["days"]
    if request.form.get("visited"):
        visited = True
    else:
        visited = False

    if request.form.get("tovisit"):
        tovisit = True
    else:
        tovisit = False

    action = visited or tovisit
    user = User(session["username"])
    if not placename or not days or not action:
        flash("Uzupelnij wszystkie pola")
    else:
        user.add_place(placename, days, visited, tovisit)
        flash("Pomyslnie dodano")

    return redirect(url_for("index"))


@app.route("/like_post/<post_id>")
def like_post(post_id):
    return "TODO"


@app.route("/profile/<username>")
def profile(username):
    return "TODO"


@app.route("/logout")
def logout():
    return "TODO"