from flask import Flask, render_template, request, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
load_dotenv()
app = Flask(__name__)
app.secret_key = "fun_contact_secret_key"
def get_db():
    database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:ZLDZTkpziaLUXaCfzEEpMTLErbMQIWfO@zephyr.proxy.rlwy.net:21128/railway?sslmode=require"
    )
    conn = psycopg2.connect(
        database_url,
        cursor_factory=RealDictCursor
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    return conn
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/signin")
    search = request.args.get("search", "")
    user_id = session["user_id"]
    conn = get_db()
    cur = conn.cursor()
    if search:
        cur.execute("""
            SELECT id,name,phone
            FROM contacts
            WHERE user_id=%s
            AND name ILIKE %s
            ORDER BY id DESC
        """, (user_id, "%" + search + "%"))
    else:
        cur.execute("""
            SELECT id,name,phone
            FROM contacts
            WHERE user_id=%s
            ORDER BY id DESC
        """, (user_id,))
    contacts = cur.fetchall()
    conn.close()
    return render_template(
        "D1.html",
        contacts=contacts,
        search=search)
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect("/signin")

    message = ""

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        user_id = session["user_id"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO contacts(name, phone, user_id)
            VALUES(%s, %s, %s)
        """, (name, phone, user_id))

        conn.commit()
        conn.close()

        message = "Contact added successfully."

    return render_template(
        "ADD.html",
        message=message
    )


@app.route("/update")
def update():
    if "user_id" not in session:
        return redirect("/signin")

    search = request.args.get("search", "")
    user_id = session["user_id"]

    conn = get_db()
    cur = conn.cursor()

    if search:
        cur.execute("""
            SELECT id,name,phone
            FROM contacts
            WHERE user_id=%s
            AND name ILIKE %s
            ORDER BY id DESC
        """, (user_id, "%" + search + "%"))
    else:
        cur.execute("""
            SELECT id,name,phone
            FROM contacts
            WHERE user_id=%s
            ORDER BY id DESC
        """, (user_id,))

    contacts = cur.fetchall()

    conn.close()

    return render_template(
        "UPDP.html",
        contacts=contacts,
        search=search,
        contact=None
    )


@app.route("/update/<int:id>")
def update_selected(id):
    if "user_id" not in session:
        return redirect("/signin")

    user_id = session["user_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id,name,phone
        FROM contacts
        WHERE id=%s
        AND user_id=%s
    """, (id, user_id))

    contact = cur.fetchone()

    cur.execute("""
        SELECT id,name,phone
        FROM contacts
        WHERE user_id=%s
        ORDER BY id DESC
    """, (user_id,))

    contacts = cur.fetchall()

    conn.close()

    return render_template(
        "UPDP.html",
        contacts=contacts,
        contact=contact,
        search=""
    )
@app.route("/save_update", methods=["POST"])
def save_update():
    if "user_id" not in session:
        return redirect("/signin")

    contact_id = request.form["id"]
    name = request.form["name"]
    phone = request.form["phone"]
    user_id = session["user_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE contacts
        SET name=%s,
            phone=%s
        WHERE id=%s
        AND user_id=%s
    """, (name, phone, contact_id, user_id))

    conn.commit()
    conn.close()

    return redirect("/update")


@app.route("/delete")
def delete():
    if "user_id" not in session:
        return redirect("/signin")

    search = request.args.get("search", "")
    user_id = session["user_id"]

    conn = get_db()
    cur = conn.cursor()

    if search:
        cur.execute("""
            SELECT id,name,phone
            FROM contacts
            WHERE user_id=%s
            AND name ILIKE %s
            ORDER BY id DESC
        """, (user_id, "%" + search + "%"))
    else:
        cur.execute("""
            SELECT id,name,phone
            FROM contacts
            WHERE user_id=%s
            ORDER BY id DESC
        """, (user_id,))

    contacts = cur.fetchall()

    conn.close()

    return render_template(
        "DELP.html",
        contacts=contacts,
        search=search
    )


@app.route("/delete/<int:id>", methods=["POST"])
def delete_contact(id):
    if "user_id" not in session:
        return redirect("/signin")

    user_id = session["user_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM contacts
        WHERE id=%s
        AND user_id=%s
    """, (id, user_id))

    conn.commit()
    conn.close()

    return redirect("/delete")
@app.route("/developer")
def developer():
    if "user_id" not in session:
        return redirect("/signin")
    return render_template("DEVI.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO users(username,email,password)
                VALUES(%s,%s,%s)
            """, (username, email, password_hash))

            conn.commit()
            conn.close()

            return redirect("/signin")

        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()

            message = "Username or email already exists."

    return render_template(
        "SIGNUP.html",
        message=message
    )


@app.route("/signin", methods=["GET", "POST"])
def signin():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id,username,email,password
            FROM users
            WHERE username=%s
        """, (username,))

        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")
        else:
            message = "Invalid username or password."

    return render_template(
        "SIGNIN.html",
        message=message
    )
@app.route("/account")
def account():
    if "user_id" not in session:
        return redirect("/signin")

    user_id = session["user_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id,username,email
        FROM users
        WHERE id=%s
    """, (user_id,))

    user = cur.fetchone()

    conn.close()

    return render_template(
        "ACCOUNT.html",
        user=user,
        message=""
    )


@app.route("/update_account", methods=["POST"])
def update_account():
    if "user_id" not in session:
        return redirect("/signin")

    user_id = session["user_id"]
    username = request.form["username"]
    email = request.form["email"]

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE users
            SET username=%s,
                email=%s
            WHERE id=%s
        """, (username, email, user_id))

        conn.commit()

        session["username"] = username

        conn.close()

        return redirect("/account")

    except psycopg2.IntegrityError:

        conn.rollback()
        conn.close()

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id,username,email
            FROM users
            WHERE id=%s
        """, (user_id,))

        user = cur.fetchone()

        conn.close()

        return render_template(
            "ACCOUNT.html",
            user=user,
            message="Username or email already exists."
        )
@app.route("/change_password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        return redirect("/signin")

    user_id = session["user_id"]
    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    if new_password != confirm_password:

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id,username,email
            FROM users
            WHERE id=%s
        """, (user_id,))

        user = cur.fetchone()

        conn.close()

        return render_template(
            "ACCOUNT.html",
            user=user,
            message="New passwords do not match."
        )

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id,username,email,password
        FROM users
        WHERE id=%s
    """, (user_id,))

    user = cur.fetchone()

    if not user or not check_password_hash(user["password"], current_password):

        conn.close()

        return render_template(
            "ACCOUNT.html",
            user=user,
            message="Current password is incorrect."
        )

    new_password_hash = generate_password_hash(new_password)

    cur.execute("""
        UPDATE users
        SET password=%s
        WHERE id=%s
    """, (new_password_hash, user_id))

    conn.commit()
    conn.close()

    return redirect("/account")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/signin")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(
        host="0.0.0.0",
        port=port
    )