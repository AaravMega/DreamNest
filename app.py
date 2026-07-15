from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "dreamnest_secret_key_change_this_in_production"

DB_PATH = os.path.join(os.path.dirname(__file__), "dreamnest.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dream_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            house_type TEXT,
            plot_size TEXT,
            bedrooms INTEGER,
            budget_range TEXT,
            style TEXT,
            location TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def home():
    gallery_items = [
        {"title": "Modern Villa", "type": "Villa", "desc": "A spacious modern villa with clean lines and large windows."},
        {"title": "Classic Family Home", "type": "House", "desc": "A warm, traditional family home with a cozy layout."},
        {"title": "Minimalist Bungalow", "type": "Bungalow", "desc": "A simple, elegant single-story home design."},
        {"title": "Luxury Duplex", "type": "Duplex", "desc": "A premium two-floor home with a rooftop terrace."},
        {"title": "Eco-Friendly Cottage", "type": "Cottage", "desc": "A sustainable home built with eco-conscious materials."},
        {"title": "Contemporary Farmhouse", "type": "Farmhouse", "desc": "A blend of rustic charm and modern comfort."},
    ]
    return render_template("home.html", gallery_items=gallery_items)


@app.route("/gallery")
def gallery():
    gallery_items = [
        {"title": "Modern Villa", "type": "Villa"},
        {"title": "Classic Family Home", "type": "House"},
        {"title": "Minimalist Bungalow", "type": "Bungalow"},
        {"title": "Luxury Duplex", "type": "Duplex"},
        {"title": "Eco-Friendly Cottage", "type": "Cottage"},
        {"title": "Contemporary Farmhouse", "type": "Farmhouse"},
        {"title": "Urban Loft House", "type": "Loft"},
        {"title": "Traditional Courtyard Home", "type": "Traditional"},
    ]
    return render_template("gallery.html", gallery_items=gallery_items)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/faq")
def faq():
    faqs = [
        {"q": "What is DreamNest?", "a": "DreamNest is a platform that helps you plan, organize, and begin the journey of building your dream home, all in one place."},
        {"q": "Is DreamNest free to use?", "a": "Yes, creating an account and building your dream home plan on DreamNest is completely free."},
        {"q": "Can I estimate my construction budget?", "a": "Yes, our Budget Planning tool gives you an approximate cost estimate based on your inputs."},
        {"q": "Does DreamNest help with home loans?", "a": "DreamNest provides general home loan planning guidance to help you understand your financing options."},
        {"q": "Can I save multiple home plans?", "a": "Yes, once logged in, you can create and save multiple dream home plans in your dashboard."},
    ]
    return render_template("faq.html", faqs=faqs)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        conn = get_db()
        conn.execute(
            "INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
            (name, email, subject, message)
        )
        conn.commit()
        conn.close()
        flash("Thank you for reaching out! We will get back to you soon.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("signup"))

        hashed_pw = generate_password_hash(password)
        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO users (full_name, email, password, phone) VALUES (?, ?, ?, ?)",
                (full_name, email, hashed_pw, phone)
            )
            conn.commit()
            conn.close()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("signup"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            flash(f"Welcome back, {user['full_name']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    plans = conn.execute(
        "SELECT * FROM dream_plans WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return render_template("dashboard.html", plans=plans)


@app.route("/profile")
@login_required
def profile():
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    conn.close()
    return render_template("profile.html", user=user)


@app.route("/plan-home", methods=["GET", "POST"])
@login_required
def plan_home():
    if request.method == "POST":
        house_type = request.form.get("house_type")
        plot_size = request.form.get("plot_size")
        bedrooms = request.form.get("bedrooms")
        budget_range = request.form.get("budget_range")
        style = request.form.get("style")
        location = request.form.get("location")
        notes = request.form.get("notes")

        conn = get_db()
        conn.execute(
            """INSERT INTO dream_plans
               (user_id, house_type, plot_size, bedrooms, budget_range, style, location, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (session["user_id"], house_type, plot_size, bedrooms, budget_range, style, location, notes)
        )
        conn.commit()
        conn.close()
        flash("Your dream home plan has been saved!", "success")
        return redirect(url_for("dashboard"))

    return render_template("plan_home.html")


@app.route("/budget-planning", methods=["GET", "POST"])
@login_required
def budget_planning():
    estimate = None
    if request.method == "POST":
        try:
            area = float(request.form.get("area", 0))
            cost_per_sqft = float(request.form.get("cost_per_sqft", 0))
            estimate = area * cost_per_sqft
        except ValueError:
            flash("Please enter valid numbers.", "danger")
    return render_template("budget_planning.html", estimate=estimate)


@app.route("/loan-planning", methods=["GET", "POST"])
@login_required
def loan_planning():
    result = None
    if request.method == "POST":
        try:
            loan_amount = float(request.form.get("loan_amount", 0))
            annual_rate = float(request.form.get("annual_rate", 0))
            tenure_years = float(request.form.get("tenure_years", 0))

            monthly_rate = (annual_rate / 12) / 100
            months = tenure_years * 12

            if monthly_rate > 0:
                emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** months) / \
                      ((1 + monthly_rate) ** months - 1)
            else:
                emi = loan_amount / months if months else 0

            result = {
                "emi": round(emi, 2),
                "total_payment": round(emi * months, 2),
                "total_interest": round((emi * months) - loan_amount, 2)
            }
        except (ValueError, ZeroDivisionError):
            flash("Please enter valid loan details.", "danger")

    return render_template("loan_planning.html", result=result)


@app.route("/services")
def services():
    return render_template("services.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
