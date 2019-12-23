from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import User, all_places, get_places, visited, will_visit, get_users, will_visit_places, visited_places

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


@app.route("/search_places", methods=["GET", "POST"])
def search_places():
    places = get_places()
    usertype = request.form.get("usertype")
    place = request.form.get("place")
    users = ""
    if places and usertype:
        if usertype == "Odwiedza":
            users = will_visit(place)
        if usertype == "Odwiedzili":
            users = visited(place)

    if users != "":
        return render_template("search_places.html", places=places, users=users, usertype=usertype, place=place)
    else:
        return render_template("search_places.html", places=places)

@app.route("/search_users", methods=["GET", "POST"])
def search_users():
    users = get_users()
    type = request.form.get("type")
    user = request.form.get("user")
    places = ""
    if users and type:
        if type == "Odwiedzi":
            places = will_visit_places(user)
        if type == "Odwiedzil":
            places = visited_places(user)

    if places != "":
        return render_template("search_users.html", users=users, places=places, type=type, user=user)
    else:
        return render_template("search_users.html", users=users)

@app.route("/profile/<username>")
def yourplaces(username):
    user = User(username)
    visited = user.visited_by_me()
    will_visit = user.to_visit_by_me()

    return render_template("yourplaces.html", username=username, visited=visited, will_visit=will_visit)


@app.route("/logout")
def logout():
    session.pop("username")
    flash("Wylogowano.")
    return redirect(url_for("index"))