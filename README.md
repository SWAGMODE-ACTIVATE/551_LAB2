# 551_LAB1
the book search website works using three databases - reviews, users, and books, all being created and filled using the flask applicatoin as wel las import.py. It contains a login/logout page, a serach page, and a template page for every book.

Files-
/static/pagestyle.css - this is the css stylesheet for all of the template pages

/templates/bookpage.html - this is the tmeplate page that shows for every book. it contains title, author, date, etc data, the form for submitting a review, and the reviews for the book all passed in via flask

/templates/index.html - this is the inoitial page you see. it is a simple login/logout and register form. the two forms create users in the user database and allow entry to the search functoin if the user enters in a valid username and password

/templates/search.html - the search bar that queries the books database for anything containing (LIKE) the query. The results are listed using flask below the bar.

the templates for the search page as well as the book page have logout and return buttons at the top of the page.

.gitattributes - idk what this is but it looks important

application.py - this is the main flask applicatoin that makes the whole thing work. it has 6 functions that handle searches, logins, user registries/logins, reviews and others. handles sessions and user login too.

import.py - creates all of the three databases and imports the contents of books.csv into the books database, also allows for resseting of those databases if needed.

books.csv - initial contents of books database to be imported.

readme.md- this file

requirements.txt - all packages needed to run both .py programs

ENGO 551 - Adv. Topics on Geospatial Technologies Nick Kennedy 30145355
