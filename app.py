from flask import Flask, flash, redirect, render_template, request, session, jsonify , url_for 
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
import sqlite3
from helpers import check_email, login_required, check_date

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# AI Usage: ChatGPT was used as a learning aid to understand how to work with SQLite using Python’s sqlite3 module without using the CS50 library.
# Configure SQLite3 to access database
conn = sqlite3.connect("app.db", isolation_level=None, check_same_thread=False)
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
def tasks():
    """Display ongoing tasks"""

    # Store user's data
    user_id = session.get("user_id")
    tasks = cur.execute("SELECT * FROM tasks WHERE user_id = ? AND is_done == 0 ORDER BY due_date", (user_id,)).fetchall()

    return render_template("tasks.html", tasks=tasks, active_page='tasks')

# AI usage: ChatGPT helped me understand how to implement this route logic
@app.post("/toggle")
def toggle_task():
    """Mark task as completed"""

    # Get task id from form
    task_id = request.form["task_id"]

    # Mark task as done
    done = 1
    today = date.today()

    # Update task status and completion date
    cur.execute("UPDATE tasks SET is_done = ?, completed_at = ? WHERE id = ?", (done, today, task_id))

    # Redirect back to tasks page
    return redirect("/")

# AI usage: ChatGPT helped me understand how to fetch task details safely
@app.route("/task/<int:task_id>")
@login_required
def task(task_id):
    """Get task details"""

    # Get task title and description
    row = cur.execute("SELECT title, description FROM tasks WHERE id = ? AND user_id = ?",(task_id, session["user_id"])).fetchone()

    # Return 404 if task does not exist
    if not row:
        return jsonify({"error": "not found"}), 404

    # Return task data as JSON
    return jsonify({"title": row["title"], "description": row["description"]})

@app.route("/completed", methods=["GET", "POST"])
@login_required
def completed():
    """Display completed tasks"""

    # Store user's data
    user_id = session.get("user_id")
    tasks = cur.execute("SELECT * FROM tasks WHERE user_id = ? AND is_done == 1 ORDER BY completed_at DESC", (user_id,)).fetchall()

    return render_template("completed.html", tasks=tasks, active_page='completed')

@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    """Create new task"""

    # Store user's data
    user_id = session.get("user_id")

    if request.method == "GET":
        return render_template("new.html", active_page='new')
    else:
        # Store user's input and current date
        title = request.form.get("title")
        description = request.form.get("description")
        due = request.form.get("due")
        today = date.today()

        # Check if title input is not blank
        if not title:
            flash("Invalid title", "danger")
            return redirect("/new")
        # Check if due date input is not blank or not valid
        elif not due or not check_date(due) or due < str(today):
            flash("Invalid due date", "danger")
            return redirect("/new")
        else:
            # Insert new task into the database
            cur.execute("INSERT INTO tasks (user_id, title, description, due_date) VALUES (?, ?, ?,?)", (user_id, title, description, due))
            return redirect("/")

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
            elif not check_date(birth):
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
