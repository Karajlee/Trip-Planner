from flask import Flask, redirect, render_template, request, session, url_for, send_file
import os
import mysql.connector
import re

app = Flask(__name__)

@app.route('/')
def index():
    # once the map html page is done we should make default the map page
    return render_template("login.html")

@app.route('/login')
def newUser():
    return render_template("login.html")

@app.route('/signup')
def newUser():
    return render_template("signup.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")


if __name__ == '__main__':
    app.run(debug=True) # this turns on the debugger for flask

