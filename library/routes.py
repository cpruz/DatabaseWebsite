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
# CONSTRAINT fk_book_written FOREIGN KEY(bookId) REFERENCES Book(bookId), CONSTRAINT fk_author_written FOREIGN KEY(authorId) REFERENCES Author(authorId))")  
# print("Table created successfully")
# con.execute("create table PublishedBy (bookId INTEGER NOT NULL, publisherId INTEGER NOT NULL, datePublished DATE NOT NULL,\
# CONSTRAINT fk_book FOREIGN KEY(bookId) REFERENCES Book(bookId), CONSTRAINT fk_publisher FOREIGN KEY(publisherId) REFERENCES Publisher(publisherId))")  
# print("Table created successfully")
# con.execute("create table BorrowedBy (bookId INTEGER NOT NULL, memberId INTEGER NOT NULL, issueDate DATE NOT NULL,\
# CONSTRAINT fk_book_borrowed FOREIGN KEY(bookId) REFERENCES Book(bookId), CONSTRAINT fk_member_borrowed FOREIGN KEY(memberId) REFERENCES Member(memberId))")  
# print("Table created successfully")

# 1. Test what you already have for adding a book
# 2. Set up the new format with add member
# 3. Complete the Author and Publisher listing pages
# 3. Reinstall all of the tables with the correct attributes so you can finish the queries
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
    global db 
    db = queries.queries
    db.connect() 
    msg = "Did not attempt"
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
                    db.addWrittenBy(bookAdded, authorAdded)
                except:
                    msg = "Data not valid for author"
        if(db.checkPublisher(publisherAdded) == False):
            try:
                db.addPublisher(publisherAdded)
                db.makePublisherId(publisherAdded)
                db.addPublishedBy(bookAdded, publisherAdded, datePublished)
            except:
                msg = "Publisher could not be added"
        msg = "Book Successfully Added"  
        return render_template("success.html",msg = msg)  

@app.route("/savememberdetails",methods = ["POST","GET"])  
def saveMemberDetails():  
    msg = "Did not attempt" 
    if request.method == "POST":  
        try:  
            firstName = request.form["firstName"]  
            lastName = request.form["lastName"]  
            birthday = request.form["birthday"]  
            phoneNumber = request.form["phoneNumber"]
            with sqlite3.connect("book.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Member (firstName, lastName, birthday, phoneNumber) values (?,?,?,?)",(firstName,lastName,birthday,phoneNumber))  
                con.commit()  
                msg = "Member Successfully Added" 
        except:  
            con.rollback()  
            msg = "We can not add the member to the list" 
        finally:  
            return render_template("member_success.html",msg = msg)  
            con.close() 

@app.route("/view")  
def view():  
    con = sqlite3.connect("book.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Book")  
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

@app.route("/delete")  
def delete():  
    return render_template("delete.html") 

@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    bookId = request.form["bookId"]  
    with sqlite3.connect("book.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Book where bookId = ?",bookId)  
            msg = "record successfully deleted" 
        except:  
            msg = "can't be deleted" 
        finally:  
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

@app.route("/viewauthors")  
def view_authors():  
    return render_template("view_authors.html")

@app.route("/viewpublishers")  
def view_publishers():  
    return render_template("view_publishers.html")
