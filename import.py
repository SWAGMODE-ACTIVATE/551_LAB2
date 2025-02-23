from sqlalchemy import create_engine, text
import os
import csv

#load database URL
DATABASE_URL = "postgresql://postgres:poop@localhost/bookdb"
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

#connect to PostgreSQL
engine = create_engine(DATABASE_URL)
conn = engine.connect()

#sql commands
create_user_talbe = text("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users
    (username, password)
    VALUES ('nick','poop');
""")

create_book_talbe = text("""
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    isbn TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
);
""")

delete_tables = text("""
DROP TABLE IF EXISTS books, users, reviews;
""")

create_review_table = text("""
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    review TEXT NOT NULL

);
""")

#optional deletion and re-initializatoin of tables
yesno = input("type 1 to delete all tables and re-initialize them ")
if yesno == "1":
    print("deleting them")
    with engine.begin() as conn: #calls the earlier functions, wil clear all users and reviews
        conn.execute(delete_tables)
        conn.execute(create_book_talbe)
        conn.execute(create_user_talbe)
        conn.execute(create_review_table)
    print("tables remade.")

file = open("books.csv", "r") #open books csv
reader=csv.reader(file)
next(reader)#skip header
with engine.begin() as conn: #loops thru whole csv, registers all the books, skips if isbn already exists to avoid unique errors
    for isbn, title, author, year in reader:
        year = int(year)  #converts year to an integer
        addbook = text("""
                       INSERT INTO books (isbn, title, author, year)
                       VALUES (:isbn, :title, :author, :year)
                       ON CONFLICT (isbn) DO NOTHING;
                       """)
        conn.execute(addbook, {"isbn": isbn, "title": title, "author": author, "year": year})#calls addbook function will all things from csv
    
#ending stuff
conn.close()
print('done')