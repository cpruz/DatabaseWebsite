import os
import secrets
import sqlite3
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from library import app, db

# con = sqlite3.connect("book.db")  
# print("Database opened successfully")  
# con.execute("create table Books (bookId INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, length INTEGER NOT NULL, availability BOOLEAN NOT NULL CHECK(availability IN (0, 1)))")  
# print("Table created successfully") 

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
    if request.method == "POST":  
        try:  
            title = request.form["title"]  
            length = request.form["length"]  
            availability = request.form["availability"]  
            with sqlite3.connect("book.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Books (title, length, availability) values (?,?,?)",(title,length,availability))  
                con.commit()  
                msg = "Book successfully Added" 
        except:  
            con.rollback()  
            msg = "We can not add the book to the list" 
        finally:  
            return render_template("success.html",msg = msg)  
            con.close() 

@app.route("/view")  
def view():  
    con = sqlite3.connect("book.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Books")  
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows) 

@app.route("/delete")  
def delete():  
    return render_template("delete.html") 

@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    bookId = request.form["bookId"]  
    with sqlite3.connect("book.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Books where bookId = ?",bookId)  
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

@app.route("/viewmembers")  
def view_members():  
    return render_template("view_members.html")