import os
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Get database URL from environment variable
DATABASE_URL = "postgresql://postgres:poop@localhost/bookdb"
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))
print('flask is starting')


"""
turns out this is ORM so not using it.
class Book(db.Model):
    __tablename__="books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    review = db.Column(db.String, nullable=False)

"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods =["POST"])
def login():
    username = request.form.get("usernamel")
    password = request.form.get("passwordl")
    existing_user = db.execute(text("SELECT * FROM users WHERE username = :username AND password = :password"), {"username": username, "password": password}).fetchone()
    if existing_user:
        session["username"] = username
        return render_template("search.html", username=session["username"])
    else:
        return render_template("index.html", message="username or password is incorrect.")
    
@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("usernamer")
    password = request.form.get("passwordr")
    existing_user = db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
    if existing_user:
        return render_template("index.html", message="username already exists.")
    else:
        db.execute(text("INSERT INTO users (username, password) VALUES (:username, :password)"), {"username": username, "password": password})
        db.commit()
        return render_template("index.html", message="account created, you can log in now.")

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search = request.form.get("query")
        search = f"%{search}%"
        result_exists = db.execute(text("SELECT * FROM books WHERE isbn LIKE :search OR title LIKE :search OR author LIKE :search OR CAST(year AS TEXT) LIKE :search"), {"search": search}).fetchall()
        if result_exists:
            return render_template("search.html", username=session["username"], results="results found", books=result_exists)
        else:
            return render_template("search.html", username=session["username"], results="no results found.")
    if request.method == "GET":
        return render_template("search.html", username=session["username"])

@app.route("/book/<int:book_id>", methods=["POST","GET"])
def bookpage(book_id):
    if request.method == "GET":
        book = db.execute(text("SELECT * FROM books WHERE id = :id"), {"id":book_id}).fetchone()
        reviews = db.execute(text("SELECT * FROM reviews WHERE book_id = :id"), {"id":book_id}).fetchall()
        return render_template("bookpage.html", book=book, username=session["username"], reviews=reviews)
    if request.method == "POST":
        review = request.form.get("review")
        username = session["username"]
        book = db.execute(text("SELECT * FROM books WHERE id = :id"), {"id":book_id}).fetchone()
        db.execute(text("INSERT INTO reviews (book_id, username, review) VALUES (:book_id, :username, :review)"), {"book_id":book_id, "username":username, "review":review})
        db.commit()
        reviews = db.execute(text("SELECT * FROM reviews WHERE book_id = :id"), {"id":book_id}).fetchall()
        return render_template("bookpage.html", book=book, username=session["username"], reviews=reviews)

if __name__ == "__main__":
    app.run(debug=True)