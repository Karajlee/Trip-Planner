from flask import Flask, redirect, render_template, request, session, url_for, send_file
import os
import mysql.connector
import re


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def home():
    # sign up page
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup():
    # get parameter values
    email = request.form.get('sign-user')
    first = request.form.get('first-name')
    last = request.form.get('last-name')
    password = request.form.get('sign-password')
    confirm = request.form.get('confirm-password')
    
    # blank input or invalid email
    if not first or not last or not email or not password or not confirm or password != confirm or not validEmail(email):
        return redirect(url_for("home"))
    query = "SELECT * FROM trip.users WHERE email = %s"
    value = (email,)
    try:
        # check if existing user -> refresh page
        mydb = mysql.connector.connect(host="localhost", user="root", password="csci201")
        mycursor = mydb.cursor()
        mycursor.execute(query, value)
        result = mycursor.fetchall() 
        if len(result) != 0:
            return redirect(url_for("home"))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    try:
        # insert new user, go to trip page
        mydb = mysql.connector.connect(host="localhost", user="root", password="csci201")
        mycursor = mydb.cursor()
        query = "INSERT INTO trip.users (email, firstName, lastName, password) VALUES (%s, %s, %s, %s)"
        values = (email, first, last, password,)
        mycursor.execute(query,values)
        mydb.commit()
        mydb.close()
        return redirect(url_for("local_home"))
    except mysql.connector.Error as e:
        return 'Error inserting data: ' + str(e)    
    # return redirect(url_for("local_home"))


@app.route("/local_home")
def local_home():
    return render_template("home.html")

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
