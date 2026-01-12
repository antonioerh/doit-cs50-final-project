from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import sqlite3
from helpers import check_email, login_required, check_birth

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite3 to access database
conn = sqlite3.connect("striation.db", isolation_level=None, check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template('register.html', active_page='register')

    else:
        # Store user's input fields
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Store checks
        username_check = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        email_check = cur.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        # Check if any field is left blank
        if not username or not email or not password or not confirmation:
            flash("Fill out all input fields", "danger")
            return redirect("/register")
        # Check if email input is valid
        elif not check_email(email):
            flash("Invalid email", "danger")
            return redirect("/register")
        # Check if username or email is taken
        elif username_check or email_check:
            flash("Username or email already taken", "danger")
            return redirect("/register")
        # Check if password fields match
        elif password != confirmation:
            flash("Passwords don't match", "danger")
            return redirect("/register")
        # Check if password has the minimum length
        elif len(password) < 8:
            flash("Password must be at least 8 characters long", "danger")
            return redirect("/register")
        else:
            # Add user's data to database
            cur.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", 
            (username, email, generate_password_hash(password)))

            # Log user in
            user = cur.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
            session["user_id"] = user["id"]

            # Redirect to home page
            flash("Registration successful!", "success")
            return redirect("/")

        
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html", active_page='login')

    else:
        # Store user's input
        identifier = request.form.get("identifier")
        password = request.form.get("password")

        # Check if any field is blank
        if not identifier or not password:
            flash("Fill out all input fields", "danger")
            return redirect("/login")

        # Check if user typed email or username
        if check_email(identifier):
            user = cur.execute("SELECT * FROM users WHERE email = ?", (identifier,)).fetchone()
        else:
            user = cur.execute("SELECT * FROM users WHERE username = ?", (identifier,)).fetchone()

        # Check if user exists and password is correct
        if not user or not check_password_hash(user["hash"], password):
            flash("Invalid email/username or password", "danger")
            return redirect("/login")
        else:
            # Log user in
            session["user_id"] = user["id"]

            # Redirect to home page
            flash("Login successful!", "success")
            return redirect("/")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Display home page"""

    # Store user's data
    user_id = session.get("user_id")
    users = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    return render_template("index.html", users=users, active_page='home')

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Show profile page"""

    # Store user's data
    user_id = session.get("user_id")
    users = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if request.method == "GET":
        return render_template("profile.html", users=users, active_page='profile')
    else:
        # Store user's input
        email = request.form.get("email")
        username = request.form.get("username")
        birth = request.form.get("birth")
        password = request.form.get("password")
        new_password = request.form.get("new_password")

        # Check if user typed password
        if not password:
            flash("Password required to save changes", "danger")
            return redirect("/profile")

        # Change user's email
        if email != users["email"]:
            if not check_password_hash(users["hash"], password):
                flash("Invalid password", "danger")
                return redirect("/profile")
            elif not check_email(email):
                flash("Invalid email", "danger")
                return redirect("/profile")
            elif email != users["email"]:
                cur.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))

        # Change user's username
        if username != users["username"]:
            if not check_password_hash(users["hash"], password):
                flash("Invalid password", "danger")
                return redirect("/profile")
            elif len(username) < 1:
                flash("Invalid username", "danger")
                return redirect("/profile")
            else:
                cur.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))

        # Change user's birth
        if birth != users["birth"]:
            if not check_password_hash(users["hash"], password):
                flash("Invalid password", "danger")
                return redirect("/profile")
            elif not check_birth(birth):
                flash("Invalid birth", "danger")
                return redirect("/profile")
            elif birth != users["birth"]:
                cur.execute("UPDATE users SET birth = ? WHERE id = ?", (birth, user_id))

        # Change user's password
        if new_password:
            if not check_password_hash(users["hash"], password):
                flash("Invalid password", "danger")
                return redirect("/profile")
            elif len(new_password) < 8:
                flash("Invalid password", "danger")
                return redirect("/profile")
            else:
                cur.execute("UPDATE users SET hash = ? WHERE id = ?", (generate_password_hash(new_password), user_id))

        # Show a success message to the user
        flash("Changes saved successfully", "success")
        return redirect("/profile")


@app.route("/exercises", methods=["GET", "POST"])
@login_required
def exercises():
    # Store all equipments and muscles
    equipments = cur.execute("SELECT * FROM equipments").fetchall()
    muscles = cur.execute("SELECT * FROM muscles").fetchall()

    # Store user's sort input
    equipment_id = request.args.get("equipment") or None
    muscle_id = request.args.get("muscle") or None

    # Base query with where conditions
    query = """
        SELECT
        exercises.id,
        exercises.name AS exercise_name,
        muscles.name AS muscle_name,
        equipments.name AS equipment_name
        FROM exercises
        JOIN muscles ON exercises.muscle_id = muscles.id
        JOIN equipments ON exercises.equipment_id = equipments.id
        WHERE 1=1
    """

    # Query parameters
    params = []

    if equipment_id:
        query += " AND equipments.id = ?"
        params.append(equipment_id)

    if muscle_id:
        query += " AND muscles.id = ?"
        params.append(muscle_id)

    # Order exercises alphabetically
    query += " ORDER BY exercises.name"

    # Run query and fetch filtered exercises
    exercises = cur.execute(query, params).fetchall()

    return render_template("exercises.html", exercises=exercises, equipments=equipments, muscles=muscles, active_page="exercises")

@app.route("/routines", methods=["GET", "POST"])
@login_required
def routines():

    # Store user's id
    user_id = session.get("user_id")

    routines = cur.execute("SELECT * FROM routines WHERE user_id = ?", (user_id,)).fetchall()

    return render_template("routines.html", routines=routines)

@app.route("/routines_create", methods=["GET", "POST"])
@login_required
def routines_create():

    # Store user's id
    user_id = session.get("user_id")

    if request.method == "GET":
        exercises = db.execute("SELECT id, name FROM exercises ORDER BY name")
        return render_template("routine_create.html", exercises=exercises, active_page="routines")

    name = (request.form.get("name") or "").strip()
    notes = (request.form.get("notes") or "").strip()

    exercise_ids = request.form.getlist("exercise_ids[]")
    sets_list = request.form.getlist("sets[]")
    reps_list = request.form.getlist("reps[]")
    rest_list = request.form.getlist("rest_seconds[]")

    if not name:
        return apology("Routine name is required", 400)

    if len(exercise_ids) == 0:
        return apology("Add at least one exercise", 400)

    # garante alinhamento
    if not (len(exercise_ids) == len(sets_list) == len(reps_list) == len(rest_list)):
        return apology("Invalid routine items", 400)

    # cria rotina
    db.execute(
        "INSERT INTO routines (user_id, name, notes) VALUES (?, ?, ?)",
        session["user_id"], name, notes
    )
    routine_id = db.execute("SELECT last_insert_rowid() AS id")[0]["id"]

    def to_int_or_none(x, min_v=None, max_v=None):
        x = (x or "").strip()
        if x == "":
            return None
        try:
            v = int(x)
        except ValueError:
            return None
        if min_v is not None and v < min_v:
            return None
        if max_v is not None and v > max_v:
            return None
        return v

    position = 1
    for ex_id, s, r, rest in zip(exercise_ids, sets_list, reps_list, rest_list):
        try:
            ex_id_int = int(ex_id)
        except ValueError:
            return apology("Invalid exercise id", 400)

        sets_v = to_int_or_none(s, 1, 99)
        reps_v = to_int_or_none(r, 1, 999)
        rest_v = to_int_or_none(rest, 0, 3600)

        db.execute(
            """
            INSERT INTO routine_exercises (routine_id, exercise_id, position, sets, reps, rest_seconds)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            routine_id, ex_id_int, position, sets_v, reps_v, rest_v
        )
        position += 1

    return redirect(url_for("routines"))




    



    

