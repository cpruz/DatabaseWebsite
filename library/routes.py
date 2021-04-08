import os
import secrets
import sqlite3
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from library import app, db


@app.route("/")
@app.route("/home")
def home():
    #posts = Post.query.all()
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/add")  
def add():  
    return render_template("add.html")  
