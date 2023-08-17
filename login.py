from flask import Flask, redirect, render_template, request, session, url_for, send_file
import os
import mysql.connector
import re
import sqlite3 as sl


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = mysql.connector.connect(host="localhost", user="root", password="R6328597x")

# root end point
# routes to login unless client has already logged in
@app.route("/")
def home():
    """
    Checks whether the user is logged in and returns appropriately.

    :return: renders login.html if not logged in,
                redirects to client otherwise.
    """
    # TODO: your code goes here and replaces 'pass' below
    # check if the user has logged in direct to client page and if not direct them to the login page
    if not session.get("logged_in"):
        return render_template("login.html")
    else:
        return redirect(url_for("home"))


# login endpoint
# allows client to log in (checks creds)
@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Allows user to log in
    Calls db_check_creds to see if supplied username and password are correct

    :return: redirects to home if login correct,
                redirects back to login otherwise
    """
    email = request.form["log-user"]
    password = request.form["log-password"]
    if email and password:
        # make sure entered username and password are correct
        if db_check_creds(email, password):
            # update the session information
            session["username"] = email
            session["logged_in"] = True
            # take user to client page after successfully logging in
            return redirect(url_for("local_home"))
        else:
            return redirect(url_for("login"))
    elif not email and not password:
        error_message = "Username and password are required."
        return render_template("login.html", Uerror_message=error_message, Perror_message = error_message)
    elif not email:
        error_message = "Username and password are required."
        return render_template("login.html", Uerror_message=error_message, Perror_message = None)
    elif not password:
        error_message = "Username and password are required."
        return render_template("login.html", Perror_message=error_message, Uerror_message = None)
    
    

def db_check_creds(un, pw):
    print("in credential method")
    """
    Checks to see if supplied username and password are in the DB's credentials table.
    Called from login() view function.

    :param un: username to check
    :param pw: password to check
    :return: True if both username and password are correct, False otherwise.
    """
    mydb = mysql.connector.connect(host="localhost", user="root", password="R6328597x")
    mycursor = mydb.cursor()
    query = "SELECT password FROM trip.users WHERE email=%s"
    values = (un,)  # Note the comma to make it a tuple
    mycursor.execute(query, values)
    result = mycursor.fetchone()  # Use fetchone() to get the result
    mydb.close()
    
    if result and result[0] == pw:
        return True
    return False

    
@app.route("/local_home")
def local_home():
    return render_template("home.html")

@app.route("/profilePage")
def profilePage():
    return render_template("profile.html")

@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for("home"))

def validEmail(email):
    # regex for email
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    return re.match(pattern, email) is not None


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)

