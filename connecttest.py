import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="R6328597x")

mycursor = mydb.cursor()

mycursor.execute("select * from hw4.users")

# result = mycursor.fetchall() # or user fetchone()

for i in mycursor:
    print(i)