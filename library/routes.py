import os
import secrets
import sqlite3
# import author
# import book
# import member
# import publisher
# import queries
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from library import app, author, book, member, publisher, queries

# con = sqlite3.connect("book.db")  
# print("Database opened successfully")  
# con.execute("create table Book (bookId INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, length INTEGER NOT NULL, availability BOOLEAN NOT NULL CHECK(availability IN (0, 1)))")  
# print("Table created successfully") 
# con.execute("create table Author (authorId INTEGER PRIMARY KEY AUTOINCREMENT, firstName TEXT NOT NULL, lastName TEXT NOT NULL)")  
# print("Table created successfully")
# con.execute("create table Publisher (publisherId INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address TEXT NOT NULL)")  
# print("Table created successfully")
# con.execute("create table Member (memberId INTEGER PRIMARY KEY AUTOINCREMENT, firstName TEXT NOT NULL, lastName TEXT NOT NULL, \
#     birthday DATE NOT NULL, phoneNumber VARCHAR(15) NOT NULL)")  
# print("Table created successfully")
# con.execute("create table WrittenBy (bookId INTEGER NOT NULL, authorId INTEGER NOT NULL, \
# CONSTRAINT fk_book_written FOREIGN KEY(bookId) REFERENCES Book(bookId) ON DELETE CASCADE, \
# CONSTRAINT fk_author_written FOREIGN KEY(authorId) REFERENCES Author(authorId) ON DELETE CASCADE)")  
# print("Table created successfully")
# con.execute("create table PublishedBy (bookId INTEGER NOT NULL, publisherId INTEGER NOT NULL, datePublished DATE NOT NULL,\
# CONSTRAINT fk_book FOREIGN KEY(bookId) REFERENCES Book(bookId) ON DELETE CASCADE, CONSTRAINT fk_publisher FOREIGN KEY(publisherId) \
# REFERENCES Publisher(publisherId) ON DELETE CASCADE)")  
# print("Table created successfully")
# con.execute("create table BorrowedBy (bookId INTEGER NOT NULL, memberId INTEGER NOT NULL, issueDate DATE NOT NULL,\
# CONSTRAINT fk_book_borrowed FOREIGN KEY(bookId) REFERENCES Book(bookId) ON DELETE CASCADE, \
# CONSTRAINT fk_member_borrowed FOREIGN KEY(memberId) REFERENCES Member(memberId) ON DELETE CASCADE)")  
# print("Table created successfully")

# 1. Check that you can add books with the same author/publisher
# 2. Complete the search functions
# 3. Add links in all the view pages to search them in different ways
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/add")  
def add():  
    return render_template("add.html")  

@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "Did not attempt"
    db = queries.queries
    db.connect()
    if request.method == "POST":  
        global bookAdded
        bookAdded = book.book(request.form["title"], request.form["length"], request.form["availability"])
        global authorAdded
        authorAdded = author.author(request.form['firstName'], request.form['lastName'])
        global publisherAdded
        publisherAdded = publisher.publisher(request.form['name'], request.form['address'])
        global datePublished
        datePublished = request.form['datePublished']
        if(db.checkBook(bookAdded) == False):
            try:  
                db.addBook(bookAdded)
                db.makeBookId(bookAdded)
            except:
                msg = "Could not add book"
        if(db.checkAuthor(authorAdded) == False):
            try:
                db.addAuthor(authorAdded)
                db.makeAuthorId(authorAdded)
            except:
                msg = "Author already exists"
        try:
            db.addWrittenBy(bookAdded, authorAdded)
        except:
            msg = "This book already exists: author"
        if(db.checkPublisher(publisherAdded) == False):
            try:
                db.addPublisher(publisherAdded)
                db.makePublisherId(publisherAdded)
            except:
                msg = "Publisher could not be added"
        if(db.alreadyPublished(bookAdded, publisherAdded) == False):
            try:
                db.addPublishedBy(bookAdded, publisherAdded, datePublished)
            except:
                msg = "This book already exists: publisher"
        msg = "Book Successfully Added"  
        return render_template("success.html",msg = msg)  

@app.route("/savememberdetails",methods = ["POST","GET"])  
def saveMemberDetails():  
    msg = "Did not attempt" 
    db = queries.queries
    db.connect()
    if request.method == "POST": 
        global memberAdded
        memberAdded = member.member(request.form["firstName"], request.form["lastName"], request.form["birthday"], request.form["phoneNumber"]) 
        if(db.checkMember(memberAdded) == False):
            try:  
                db.addMember(memberAdded)
                db.makeMemberId(memberAdded)
            except:   
                msg = "We can not add the member to the list" 
        msg = "Member successfully added" 
    return render_template("member_success.html",msg = msg)   

@app.route("/view")  
def view():  
    con = sqlite3.connect("book.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("SELECT Book.bookId, Book.title, Book.length, Book.availability, Author.firstName, Author.lastName, Publisher.name\
    FROM Author JOIN WrittenBy JOIN Book JOIN PublishedBy JOIN Publisher\
    ON Book.bookId = WrittenBy.bookId\
    AND WrittenBy.authorId = Author.authorId\
    AND Book.bookId = PublishedBy.bookId\
    AND PublishedBy.publisherId = Publisher.publisherId")  
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows) 

@app.route("/viewmember")  
def viewMember():  
    con = sqlite3.connect("book.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Member")  
    rows = cur.fetchall()  
    return render_template("view_members.html",rows = rows) 

@app.route("/viewauthor")  
def viewAuthor():  
    con = sqlite3.connect("book.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Author")  
    rows = cur.fetchall()  
    return render_template("view_authors.html",rows = rows)

@app.route("/viewpublisher")  
def viewPublisher():  
    con = sqlite3.connect("book.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Publisher")  
    rows = cur.fetchall() 
    return render_template("view_publishers.html",rows = rows)

@app.route("/delete")  
def delete():  
    return render_template("delete.html") 

@app.route("/deleterecord",methods = ["POST", "GET"])  
def deleterecord():
    db = queries.queries
    db.connect()
    if request.method == "POST":   
        bookId = request.form["bookId"]   
        try:  
            db.deleteBook(bookId)
            msg = "Book successfully deleted" 
        except:  
            msg = "Book can't be deleted" 
    return render_template("delete_record.html",msg = msg)

@app.route("/addmember")  
def add_member():  
    return render_template("add_member.html")

@app.route("/deletemember")  
def delete_member():  
    return render_template("delete_member.html")

@app.route("/checkin")  
def checkin():  
    return render_template("checkin.html")

@app.route("/checkinbook",methods = ["POST", "GET"])  
def checkinBook():  
    db = queries.queries
    db.connect()  
    bookId = request.form["bookId"]
    if(db.alreadyBorrowed(bookId) == True):
        try:
            db.removeBorrowedBy(bookId)
        except:
            msg = "This book is not checked out"
    try:
        db.checkinBook(bookId)
        msg = "Book successfully checkedin"
    except:
        msg = "Book could not be checked in"
    return render_template("checkin_book.html", msg = msg)

@app.route("/checkout")  
def checkout():  
    return render_template("checkout.html")

@app.route("/checkoutbook",methods = ["POST", "GET"])  
def checkoutBook():  
    db = queries.queries
    db.connect()  
    bookId = request.form["bookId"]
    memberId = request.form["memberId"]
    if(db.alreadyBorrowed(bookId) == False):
        try:
            db.addBorrowedBy(bookId, memberId)
        except:
            msg = "The book could not be borrowed"
    try:
        db.checkoutBook(bookId)
        msg = "Book successfully checkedout"
    except:
        msg = "Book could not be checked out"
    return render_template("checkout_book.html", msg = msg)

@app.route("/checkedoutlist")
def borrowedBooks():  
    con = sqlite3.connect("book.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("SELECT Book.bookId, Book.title, Book.length, Book.availability, Member.memberId, Member.firstName, Member.lastName\
    FROM Book JOIN BorrowedBy JOIN Member\
    ON Book.bookId = BorrowedBy.bookId\
    AND BorrowedBy.memberId = Member.memberId")  
    rows = cur.fetchall()  
    return render_template("borrowed_books.html", rows = rows)

@app.route("/searchbook")  
def search_book():  
    return render_template("search_book.html")

@app.route("/searchbookauthor")  
def search_book_author():  
    return render_template("search_book_author.html")

@app.route("/searchbookpublisher")  
def search_book_publisher():  
    return render_template("search_book_publisher.html")

@app.route("/searchbookgenre")  
def search_book_genre():  
    return render_template("search_book_genre.html")

