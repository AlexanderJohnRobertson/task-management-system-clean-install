'''This is the main file for the application. This file contains the main code for the application.
 This file contains the code for the main pages of the application, such as the login page, the create account page,
 the user home page, the view tasks page, the view projects page, the add task page, the update task page, the delete
 task page, the add project page, the update project page, the delete project page, the change username page, the change
 password page, the delete account page, the account details page, the update account details page, and the test page.
 This file also contains the code for the global variables and the common passwords list. This file also contains the
 code for the database connection and the error handling for the database connection. This file also contains the code
 for the hashing of the passwords and the regular expressions for the password validation. This file also contains the
 code for the cookies and the flash messages. This file also contains the code for the main function that runs the
 application.'''

#importing the required libraries
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, request, make_response
import os
import sqlite3
from sqlite3 import Error, IntegrityError, OperationalError
import hashlib
import re
import smtplib
import random

app = Flask(__name__) #creating the Flask application
app.config['SECRET_KEY'] = 'hdyr35bjdgge65gcsl' #setting the secret key for the application
def global_var(Uname):
    global globalUsername
    globalUsername = Uname
    return globalUsername

def global_var2():
    """This function returns a list of common passwords."""
    global commonPasswords #declaring the global variable
    commonPasswords = ["Hello", "Password","Password123@", "123456", "123456789", "qwerty", "password",
                       "1234567", "12345678", "12345", "iloveyou", "111111", "123123", "abc123", "qwerty123",
                       "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "lovely", "7777777", "welcome",
                       "888888", "princess", "dragon", "password1", "123qwe", "666666", "1qaz2wsx", "121212",
                       "123654", "superman", "qazwsx", "1234qwer", "asdf", "zxcvbnm", "qwe123", "123qweasd",
                       "admin123", "1234567890", "123456a", "123456q", "123456789a", "123456789q", "123456789z",
                       "123456789x", "123456789c", "123456789v", "123456789b", "123456789n", "123456789m",
                    "123456", "123456789", "12345", "12345678", "111111", "123123", "1234567890", "234567","qwerty123"
                    "000000", "1q2w3e", "aa12345678", "abc123", "password1", " 	1234", "qwertyuiop", "123321", "password123"]
    return commonPasswords

def sendEmail(emailAddress, unencryptedPassword):
    '''This function sends an email to the user with their new password.'''
    server = smtplib.SMTP('smtp-mail.outlook.com', 587) #setting up the email server
    server.starttls() #starting the email server
    server.login("taskmanagementsystem@hotmail.com", "Python.303") #logging into the email server
    message = """\
Subject: Task Management System

Your password has been reset.  Your new password is: """ + unencryptedPassword
    server.sendmail("taskmanagementsystem@hotmail.com", emailAddress, message)
    server.quit() #quitting the email server

def setupEmail(emailAddress, unencryptedPassword):
    '''This function sends an email to the root user with their new password.'''
    server = smtplib.SMTP('smtp-mail.outlook.com', 587) #setting up the email server
    server.starttls() #starting the email server
    server.login("taskmanagementsystem@hotmail.com", "Python.303") #logging into the email server
    message = """\
Subject: Task Management System

Welcome to the Task Management System (first time setup).  Your password is: """ + unencryptedPassword
    server.sendmail("taskmanagementsystem@hotmail.com", emailAddress, message)
    server.quit() #quitting the email server


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Main (Landing) page of the application. This is the first page that the user sees when they visit the website.'''
    rootUser = "Root"  # root user
    database = r"database.db" #database file
    conn = None
    conn = sqlite3.connect(database) #connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (rootUser,)) #querying the database
    root = cur.fetchall()
    cur.close()
    if not root:
        return redirect(url_for('setup')) #if the root user does not exist redirect to the setup page
    else:
        cookie = request.cookies.get('userID')
        sessionCookie = request.cookies.get('sessionID')#getting the cookie
        if cookie != "" or sessionCookie != "0": #if the cookie is not empty
            database = r"database.db" #database file
            conn = None
            conn = sqlite3.connect(database)
            cur = conn.cursor()
            sessionCookie = "0"
            cur.execute('UPDATE users SET sessionID = ? WHERE username = ?', (sessionCookie, cookie,)) #querying the database
            conn.commit()
            cur.close()
            resp = make_response(render_template('logoutcookie.html'))
            resp.set_cookie('userID', "") #setting the cookie to an empty string
            resp.set_cookie('sessionID', "0") #setting the session ID cookie to 0
            return resp
        else:
            return render_template('index.html') #rendering the index.html page

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''This function allows the user to login to the application.'''
    if request.method == 'POST':
        username = request.form['username'] # get form details
        password = request.form['password']
        if not username: #validate the form details
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                for i in range(10): #password hashing encryption
                        password = hashlib.sha3_512(password.encode('utf-8'))
                        password = password.hexdigest()
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database) #connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)) #querying the database
                user = cur.fetchall()
                cur.close()
                User = user[0]
                Uname = User[0]
                Pword = User[1]
                blocked = User[7]
                failedLoginAttempts = User[8]
                if Uname == username and Pword == password: #if the username and password are correct
                    if blocked == "Yes": #if the user is blocked flash an error message
                        flash('You have been blocked.  Please contact the administrator.')
                    elif failedLoginAttempts >= 3: #if the user has had 3 failed login attempts flash an error message
                        blocked = "Yes"
                        database = r"database.db" #database file
                        conn = None
                        conn = sqlite3.connect(database)
                        cur = conn.cursor()
                        cur.execute('UPDATE users SET blocked = ? WHERE username = ?', (blocked, username,))
                        conn.commit()
                        cur.close()
                    else:
                        sessionID = random.randint(1000000000, 9999999999) #generate a random session ID
                        print(sessionID)
                        global_var(Uname)
                        database = r"database.db" #database file
                        conn = None
                        conn = sqlite3.connect(database) #connecting to the database
                        cur = conn.cursor()
                        cur.execute('UPDATE users SET failedLoginAttempt = ? WHERE username = ?', (0, username, )) #reset the failed login attempts to 0 if the user logs in successfully
                        cur.execute('UPDATE users SET sessionID = ? WHERE username = ?', (sessionID, username,)) #update the session ID in the database
                        conn.commit()
                        cur.close()
                        user = Uname
                        resp = make_response(render_template('readcookie.html'))
                        resp.set_cookie('userID', user) #setting the cookie connected to the username
                        resp.set_cookie('sessionID', str(sessionID)) #setting the cookie connected to the session ID
                        return resp
                else: #if the username and password are incorrect flash an error message
                    database = r"database.db"  # database file
                    conn = None
                    conn = sqlite3.connect(database)  # connecting to the database
                    cur = conn.cursor()
                    cur.execute('SELECT failedLoginattempt FROM users WHERE username = ?',
                                (username,))  # querying the database
                    failedLoginAttempts = cur.fetchall()
                    failedLoginAttempts = failedLoginAttempts[0][0]
                    failedLoginAttempts = failedLoginAttempts + 1 #increment the failed login attempts if password is incorrect
                    print(failedLoginAttempts)
                    cur.execute('UPDATE users SET failedLoginAttempt = ? WHERE username = ?',
                                (failedLoginAttempts, username,)) # updating the failed login attempts in the database
                    conn.commit()
                    cur.close()
                    if failedLoginAttempts >= 3: #block the user if there are 3 failed login attempts
                        blocked = "Yes"
                        database = r"database.db"
                        conn = None
                        conn = sqlite3.connect(database)
                        cur = conn.cursor()
                        cur.execute('UPDATE users SET blocked = ? WHERE username = ?', (blocked, username,))
                        conn.commit()
                        cur.close()
                        flash(
                            'You have been blocked because you entered the wrong password too many times. Please contact the administrator.')
                    flash('Username or Password is incorrect!')
            except IndexError: #if there is an error caused by incorrect login details flash an error message
                try:
                    database = r"database.db"  # database file
                    conn = None
                    conn = sqlite3.connect(database)  # connecting to the database
                    cur = conn.cursor()
                    cur.execute('SELECT failedLoginattempt FROM users WHERE username = ?',(username,))  # querying the database
                    failedLoginAttempts = cur.fetchall()
                    failedLoginAttempts = failedLoginAttempts[0][0]
                    failedLoginAttempts = failedLoginAttempts + 1 #increment the failed login attempts if password is incorrect
                    cur.execute('UPDATE users SET failedLoginAttempt = ? WHERE username = ?',(failedLoginAttempts, username,)) #updating the failed login attempts in the database
                    conn.commit()
                    cur.close()
                    if failedLoginAttempts >= 3: #block the user if there are 3 failed login attempts
                        blocked = "Yes"
                        database = r"database.db"
                        conn = None
                        conn = sqlite3.connect(database)
                        cur = conn.cursor()
                        cur.execute('UPDATE users SET blocked = ? WHERE username = ?', (blocked, username,))
                        conn.commit()
                        cur.close()
                        flash('You have been blocked because you entered the wrong password too many times. Please contact the administrator.')
                    flash('Username or Password is incorrect!')
                except IndexError:
                    flash('Username does not exist!')
    return render_template('login.html') #render the login.html page

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    '''This function allows the user to create an account.'''
    if request.method == 'POST': #get form details
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        accountType = "Standard" #set the account type to standard
        blocked = "No" #set the blocked status to no
        failedLoginAttempts = 0 #set the failed login attempts to 0
        checkLowercase = re.search(r'[a-z]', password) #use regular expressions to validate the password
        checkUppercase = re.search(r'[A-Z]', password)
        checkNumber = re.search(r'[0-9]', password)
        checkSpecialChar = re.search(r'[^A-Za-z0-9]', password)
        if not firstname: #validate the form details
            flash('First Name is required!')
        elif not lastname:
            flash('Last Name is required!')
        elif not username:
            flash('Username is required!')
        elif not email:
            flash('Email Address is required!')
        elif not phonenumber:
            flash('Phone Number is required!')
        elif not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        elif not confirmPassword:
            flash('Confirm Password is required!')
        elif not checkLowercase: #validate the password
            flash('Password must contain at least one lowercase letter!')
        elif not checkUppercase:
            flash('Password must contain at least one uppercase letter!')
        elif not checkNumber:
            flash('Password must contain at least one number!')
        elif not checkSpecialChar:
            flash('Password must contain at least one special character!')
        elif len(password) < 10: # minimum password length is 10 characters
            flash('Password must be at least 10 characters long!')
        elif password == username:
            flash('Password cannot be the same as the username!')
        elif password == firstname:
            flash('Password cannot be the same as the first name!')
        elif password == lastname:
            flash('Password cannot be the same as the last name!')
        elif password == email:
            flash('Password cannot be the same as the email!')
        elif password == phonenumber:
            flash('Password cannot be the same as the phone number!')
        elif password in global_var2(): #if the password is in the common passwords list flash an error message
            flash('Password is too common!')
        else:
            try:
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database) #connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,)) #querying the database
                user = cur.fetchall()
                cur.close()
                if user: #if the username already exists flash an error message
                    flash('Username already exists!')
                else:
                    if password != confirmPassword: #if the password and confirm password do not match flash an error message
                        flash('Passwords do not match!')
                    else:
                        for i in range(10): #password hashing encryption
                            password = hashlib.sha3_512(password.encode('utf-8'))
                            password = password.hexdigest()
                        sessionID = random.randint(1000000000, 9999999999) #generate a random session ID
                        cur = conn.cursor()
                        cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (username, password, firstname, lastname, email, phonenumber, accountType, blocked, failedLoginAttempts, sessionID)) #inserting the user details into the database
                        conn.commit()
                        cur.close()
                        resp = make_response(render_template('readcookie.html')) #setting the cookie connected to the username
                        resp.set_cookie('userID', username)
                        resp.set_cookie('sessionID', str(sessionID))
                        return resp
            except IndexError: #if there is an error caused by incorrect login details flash an error message
                flash('Username or Password is incorrect!')
    return render_template('createaccount.html') #render the createaccount.html page

@app.route('/userhome/', methods=['GET', 'POST'])
def userhome():
    '''This function renders the userhome page.'''
    try:
        cookie = request.cookies.get('userID') #get the cookie
        sessionCookie = request.cookies.get('sessionID') #get the session ID cookie
        database = r"database.db" #database file
        conn = None
        conn = sqlite3.connect(database) #connecting to the database
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,)) #querying the database
        user = cur.fetchall()
        if not user: #deny access if the user does not exist
            return render_template('accessdenied.html')
        sessionID = user[0][9] #get the session ID from the database
        cur.close()
        if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
            return render_template('accessdenied.html')
        elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    name = request.cookies.get('userID') #get the cookie
    data = name
    return render_template('userhome.html', data=data) #render the userhome.html page

@app.route('/viewtasks')
def viewtasks():
    '''This function renders the viewtasks page.'''
    try:
        cookie = request.cookies.get('userID')  # get the cookie
        sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
        database = r"database.db"  # database file
        conn = None
        conn = sqlite3.connect(database)  # connecting to the database
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
        user = cur.fetchall()
        if not user: #deny access if the user does not exist
            return render_template('accessdenied.html')
        sessionID = user[0][9]
        cur.close()
        if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
            return render_template('accessdenied.html')
        elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    database = r"database.db" #database file
    conn = None
    try:
        conn = sqlite3.connect(database) #connecting to the database
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks") #selecting all the tasks from the database
    data = cur.fetchall()

    #return jsonify(data)
    return render_template('viewtasks.html', data1=data) #render the viewtasks.html page

@app.route('/viewprojects', methods=['GET', 'POST'])
def viewprojects():
    '''This function renders the viewprojects page.'''
    try:
        cookie = request.cookies.get('userID')  # get the cookie
        sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
        database = r"database.db"  # database file
        conn = None
        conn = sqlite3.connect(database)  # connecting to the database
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
        user = cur.fetchall()
        if not user:
            return render_template('accessdenied.html')
        sessionID = user[0][9]
        cur.close()
        if len(sessionID) < 10:
            return render_template('accessdenied.html')
        elif sessionID != sessionCookie:
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    database = r"database.db" #database file
    conn = None
    try:
        conn = sqlite3.connect(database) #connecting to the database
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects") #selecting all the projects from the database
    data = cur.fetchall()

    #return jsonify(data)
    return render_template('viewprojects.html', data1=data) #render the viewprojects.html page

'''@app.route('/readcookie', methods=['GET', 'POST'])
def readcookie():
    return redirect(url_for('userhome'))'''

@app.route('/addtask', methods=['POST', 'GET'])
def addtask():
    '''This function allows the user to add a task to the database.'''
    try:
        cookie = request.cookies.get('userID')  # get the cookie
        sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
        database = r"database.db"  # database file
        conn = None
        conn = sqlite3.connect(database)  # connecting to the database
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
        user = cur.fetchall()
        if not user:
            return render_template('accessdenied.html')
        sessionID = user[0][9]
        cur.close()
        if len(sessionID) < 10:
            return render_template('accessdenied.html')
        elif sessionID != sessionCookie:
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    if request.method == 'POST': #get form details
        taskid = request.form['taskid']
        title = request.form['title']
        duedate = request.form['duedate']
        priority = request.form['priority']
        status = request.form['status']
        projectid = request.form['projectid']
        description = request.form.get('description')
        if not taskid: #validate the form details
            flash('Task ID is required!')
        elif not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        elif not duedate:
            flash('Due Date is required!')
        elif not priority:
            flash('Priority is required!')
        elif not status:
            flash('Status is required!')
        elif not projectid:
            flash('Project ID is required!')
        elif priority != 'High' and priority != 'Medium' and priority != 'Low':
            flash('Priority must be High, Medium, or Low!')
        elif status != 'Planned' and status != 'In Progress' and status != 'Completed' and status != 'Overdue' and status != 'Cancelled' and status !='Not Started':
            flash('Status must be Not Started, Planned, In Progress, Completed, Overdue or Cancelled!')
        else:
            try:
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM tasks WHERE taskID = ?', (taskid,)) #querying the database to check if the task ID already exists
                task = cur.fetchall()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,)) #querying the database to check if the project ID exists
                project = cur.fetchall()
                cur.execute('SELECT * FROM users WHERE username = ?', (cookie,)) #querying the database to check if the user exists
                user = cur.fetchall()
                if task:
                    flash('Task ID already exists!')
                elif not project:
                    flash('Project ID does not exist!')
                elif not user:
                    return render_template('accessdenied.html')
                else:
                    cur.execute('INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?, ?)', (taskid, title, description, duedate, priority, status, projectid)) #inserting the task details into the database
                    conn.commit()
                    cur.close()
                    #flash ('Task added successfully!')
                    return redirect(url_for('viewtasks')) #redirect to the viewtasks page
            except IndexError:
                flash('Error adding task!') #if there is an error adding the task flash an error message
            except IntegrityError:
                flash('Task ID already exists!') #if the task ID already exists flash an error message
            except OperationalError:
                flash('Database locked.')  #if the database is locked flash an error message
                return redirect(url_for('addtask'))
    return render_template('addtask.html') #render the addtask.html page

@app.route('/updatetask', methods=['POST', 'GET'])
def updatetask():
    '''This function allows the user to update a task in the database.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user:#deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator": #if the user is not an administrator deny access
        return render_template('adminrequired.html')
    if request.method == 'POST': #get form details
        taskid = request.form['taskid']
        title = request.form['title']
        duedate = request.form['duedate']
        priority = request.form['priority']
        status = request.form['status']
        projectid = request.form['projectid']
        description = request.form.get('description')
        if not taskid: #validate the form details
            flash('Task ID is required!')
        elif not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        elif not duedate:
            flash('Due Date is required!')
        elif not priority:
            flash('Priority is required!')
        elif not status:
            flash('Status is required!')
        elif not projectid:
            flash('Project ID is required!')
        elif priority != 'High' and priority != 'Medium' and priority != 'Low':
            flash('Priority must be High, Medium, or Low!')
        elif status != 'Planned' and status != 'In Progress' and status != 'Completed' and status != 'Overdue' and status != 'Cancelled' and status !='Not Started':
            flash('Status must be Not Started, Planned, In Progress, Completed, Overdue or Cancelled!')
        else:
            try:
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database) #connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM tasks WHERE taskID = ?', (taskid,)) #querying the database to check if the task ID exists
                task = cur.fetchall()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,)) #querying the database to check if the project ID exists
                project = cur.fetchall()
                if not task:
                    flash('Task does not exist!')
                elif not project:
                    flash('Project ID does not exist!')
                else:
                    cur.execute('UPDATE tasks SET title = ?, description = ?, duedate = ?, priority = ?, status = ?, projectID = ? WHERE taskID = ?', (title, description, duedate, priority, status, projectid, taskid)) #updating the task details in the database
                    conn.commit()
                    cur.close()
                    #flash ('Task updated successfully!') #flash a success message
                    return redirect(url_for('viewtasks')) #redirect to the viewtasks page
            except IndexError:
                flash('Error updating task!')
            except IntegrityError:
                flash('Task ID already exists!') #if the task ID already exists flash an error message
    return render_template('updatetask.html') #render the updatetask.html page

@app.route('/deletetask', methods=['POST', 'GET'])
def deletetask():
    '''This function allows the user to delete a task from the database.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: #deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator": #if the user is not an administrator deny access
        return render_template('adminrequired.html')
    if request.method == 'POST': #get form details
        taskid = request.form['taskid']
        title = request.form['title']
        if not taskid: #validate the form details
            flash('Task ID is required!')
        elif not title:
            flash('Title is required!')
        else:
            try:
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database) #connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM tasks WHERE taskID = ?', (taskid,)) #querying the database to check if the task ID exists
                task = cur.fetchall()
                if not task:
                    flash('Task does not exist!')
                elif task[0][1] != title:
                    flash('Task ID and Title do not match!')
                else:
                    cur.execute('DELETE FROM tasks WHERE taskID = ?', (taskid,)) #deleting the task from the database
                    conn.commit()
                    cur.close()
                    #flash ('Task deleted successfully!')
                    return redirect(url_for('viewtasks')) #redirect to the viewtasks page
            except IndexError:
                flash('Error deleting task!')
            except IntegrityError:
                flash('Task ID already exists!')
    return render_template('deletetask.html')   #render the deletetask.html page

@app.route('/addproject', methods=['POST', 'GET'])
def addproject():
    '''This function allows the user to add a project to the database.'''
    try:
        cookie = request.cookies.get('userID')  # get the cookie
        sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
        database = r"database.db"  # database file
        conn = None
        conn = sqlite3.connect(database)  # connecting to the database
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
        user = cur.fetchall()
        if not user: #deny access if the user does not exist
            return render_template('accessdenied.html')
        sessionID = user[0][9]
        cur.close()
        if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
            return render_template('accessdenied.html')
        elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    if request.method == 'POST': #get form details
        projectid = request.form['projectid']
        title = request.form['title']
        description = request.form.get('description')
        assignedTasks = request.form.get('assignedTasks')
        if not projectid:   #validate the form details
            flash('Project ID is required!')
        elif not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        elif not assignedTasks:
            flash('List of assigned tasks is required!')
        else:
            try:
                database = r"database.db"  #database file
                conn = None
                conn = sqlite3.connect(database)    #connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,))   #querying the database to check if the project ID already exists
                project = cur.fetchall()
                if project:
                    flash('Project ID already exists!')
                else:
                    cur.execute('INSERT INTO projects VALUES(?, ?, ?, ?)', (projectid, title, description, assignedTasks)) #inserting the project details into the database
                    conn.commit()
                    cur.close()

                    return redirect(url_for('viewprojects'))
            except IndexError:
                flash('Error adding project!')
            except IntegrityError:
                flash('Project ID already exists!') #if the project ID already exists flash an error message
            except OperationalError:
                flash('Database locked.')
                return redirect(url_for('addproject'))
    return render_template('addproject.html')   #render the addproject.html page



@app.route('/updateproject', methods=['POST', 'GET'])
def updateproject():
    '''This function allows the user to update a project in the database.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user:    #deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator": #if the user is not an administrator deny access
        return render_template('adminrequired.html')
    if request.method == 'POST': #get form details
        projectid = request.form['projectid']
        title = request.form['title']
        description = request.form.get('description')
        assignedTasks = request.form['assignedTasks']
        if not projectid:  #validate the form details
            flash('Project ID is required!')
        elif not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        elif not assignedTasks:
            flash('List of assigned tasks is required!')
        else:
            try:
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,))  #querying the database to check if the project ID exists
                project = cur.fetchall()
                if not project:
                    flash('Project does not exist!')
                else:
                    cur.execute('UPDATE projects SET title = ?, description = ?, tasks = ? WHERE projectID = ?', (title, description, assignedTasks, projectid)) #updating the project details in the database
                    conn.commit()
                    cur.close()
                    #flash ('Project updated successfully!')
                    return redirect(url_for('viewprojects')) #redirect to the viewprojects page
            except IndexError:
                flash('Error updating project!')
            except IntegrityError:
                flash('Project ID already exists!') #if the project ID already exists flash an error message
    return render_template('updateproject.html')  #render the updateproject.html page

@app.route('/deleteproject', methods=['POST', 'GET'])
def deleteproject():
    '''This function allows the user to delete a project from the database.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: #deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator": #if the user is not an administrator deny access
        return render_template('adminrequired.html')
    if request.method == 'POST': #get form details
        projectid = request.form['projectid']
        title = request.form['title']
        if not projectid: #validate the form details
            flash('Project ID is required!')
        elif not title:
            flash('Title is required!')
        else:
            try:
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database) #connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,)) #querying the database to check if the project ID exists
                project = cur.fetchall()
                if not project:
                    flash('Project does not exist!')
                elif project[0][1] != title:
                    flash('Project ID and Title do not match!')
                else:
                    cur.execute('DELETE FROM projects WHERE projectID = ?', (projectid,)) #deleting the project from the database
                    conn.commit()
                    cur.close()
                    #flash ('Project deleted successfully!')
                    return redirect(url_for('viewprojects')) #redirect to the viewprojects page
            except IndexError:
                flash('Error deleting project!')
            except IntegrityError:
                flash('Project ID already exists!') #if the project ID already exists flash an error message
    return render_template('deleteproject.html') #render the deleteproject.html page

@app.route('/changeusername', methods=['POST', 'GET'])
def changeUsername():
    '''This function allows the user to change their username.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: #deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    if request.method == 'POST': #get form details
        username = request.form['username']
        newUsername = request.form['newUsername']
        confirmNewUsername = request.form['confirmNewUsername']
        password = request.form['password']
        if not username: #validate the form details
            flash('Username is required!')
        elif not newUsername:
            flash('New Username is required!')
        elif not confirmNewUsername:
            flash('Confirm New Username is required!')
        elif not password:
            flash('Password is required!')
        elif newUsername != confirmNewUsername:
            flash('New Username and Confirm New Username do not match!')
        else:
            try:
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database)    #connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,)) #querying the database to check if the username exists
                user = cur.fetchall()
                encryptedPassword = user[0][1]
                for i in range(10): #password hashing encryption
                    password = hashlib.sha3_512(password.encode('utf-8'))
                    password = password.hexdigest()
                if not user: #if the username does not exist flash an error message
                    flash('User does not exist!')
                elif username != cookie:
                    flash('New Your username does not match your current username!')
                elif username == "Root" and cookie == "Root":
                    flash('Root username cannot be changed!')
                elif password != encryptedPassword:
                    flash('Password is incorrect!')
                else:
                    cur.execute('UPDATE users SET username = ? WHERE username = ?', (newUsername, cookie,)) #updating the username in the database
                    conn.commit()
                    cur.close()
                    resp = make_response(render_template('readcookie.html'))
                    resp.set_cookie('userID', newUsername)
                    flash('Username changed successfully!') #flash a success message
                    return resp
            except IndexError:
                flash('Error changing!')
            except IntegrityError:
                flash('User already exists!')
    return render_template('changeusername.html') #render the changeusername.html page

@app.route('/changepassword', methods=['POST', 'GET'])
def changePassword():
    '''This function allows the user to change their password.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: #deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    if request.method == 'POST': #get form details
        username = request.form['username']
        password = request.form['password']
        newPassword = request.form['newPassword']
        confirmPassword = request.form['confirmPassword']
        checkLowercase = re.search(r'[a-z]', newPassword) #validate the password using regular expressions
        checkUppercase = re.search(r'[A-Z]', newPassword)
        checkNumber = re.search(r'[0-9]', newPassword)
        checkSpecialChar = re.search(r'[^A-Za-z0-9]', newPassword)
        if not username: #validate the form details
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        elif not newPassword:
            flash('New Password is required!')
        elif not confirmPassword:
            flash('Confirm New Password is required!')
        elif newPassword != confirmPassword: #if the new password and confirm new password do not match flash an error message
            flash('New Password and Confirm New Password do not match!')
        elif not checkLowercase: #validate the password
            flash('Password must contain at least one lowercase letter!')
        elif not checkUppercase:
            flash('Password must contain at least one uppercase letter!')
        elif not checkNumber:
            flash('Password must contain at least one number!')
        elif not checkSpecialChar:
            flash('Password must contain at least one special character!')
        elif len(password) < 10: # minimum password length is 10 characters
            flash('Password must be at least 10 characters long!')
        elif password == username: #if the password is the same as the username flash an error message
            flash('Password cannot be the same as the username!')
        elif password in global_var2(): #if the password is in the common passwords list flash an error message
            flash('Password is too common!')
        else:
            try:
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,)) #querying the database to check if the username exists
                user = cur.fetchall()
                tupleUser = user[0] #get the user details
                encryptedPassword = tupleUser[1]
                username = tupleUser[0]
                firstname = tupleUser[2]
                lastname = tupleUser[3]
                email = tupleUser[4]
                phonenumber = tupleUser[5]
                for i in range(10): #password hashing encryption
                    password = hashlib.sha3_512(password.encode('utf-8'))
                    password = password.hexdigest()
                if not user: #if the username does not exist flash an error message
                    flash('User does not exist!')
                elif username != cookie: # paswwordvalidation
                    flash('New Your username does not match your current username!')
                elif password == username:
                    flash('Password cannot be the same as the username!')
                elif password == firstname:
                    flash('Password cannot be the same as the first name!')
                elif password == lastname:
                    flash('Password cannot be the same as the last name!')
                elif password == email:
                    flash('Password cannot be the same as the email!')
                elif password == phonenumber:
                    flash('Password cannot be the same as the phone number!')
                elif password != encryptedPassword:
                    flash('Password is incorrect!')
                else:
                    for i in range(10): #password hashing encryption
                        newPassword = hashlib.sha3_512(newPassword.encode('utf-8'))
                        newPassword = newPassword.hexdigest()
                    cur.execute('UPDATE users SET password = ? WHERE username = ?', (newPassword, cookie,)) #updating the password in the database
                    conn.commit()
                    cur.close()
                    flash('Password changed successfully!')
                    return redirect(url_for('userhome')) #redirect to the userhome page
            except IndexError:
                flash('Error changing!')
            except IntegrityError:
                flash('User already exists!')
    return render_template('changepassword.html') #render the changepassword.html page

@app.route('/deleteaccount', methods=['POST', 'GET'])
def deleteAccount():
    '''This function allows the user to delete their account.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: #deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    if request.method == 'POST': #get form details
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        if not username: #validate the form details
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        elif not confirmPassword:
            flash('Confirm New Password is required!')
        elif password != confirmPassword:
            flash('Password and Confirm Password do not match!')
        else:
            try:
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database) #connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,)) #querying the database to check if the username exists
                user = cur.fetchall()
                encryptedPassword = user[0][1] #get the user details
                for i in range(10): #password hashing encryption
                    password = hashlib.sha3_512(password.encode('utf-8'))
                    password = password.hexdigest()
                if not user:
                    flash('User does not exist!')
                elif username != cookie:
                    flash('New Your username does not match your current username!')
                elif username == "Root" and cookie == "Root":
                    flash('Root username cannot be deleted!')
                elif password != encryptedPassword:
                    flash('Password is incorrect!')
                else:
                    cur.execute('DELETE FROM users WHERE username = ?', (cookie,)) #deleting the user from the database
                    conn.commit()
                    cur.close()
                    flash('Account Deleted successfully!') #flash a success message
                    return redirect(url_for('index')) #redirect to the index page and log the user out after deleting the account
            except IndexError:
                flash('Error changing!')
            except IntegrityError:
                flash('User already exists!')
    return render_template('deleteaccount.html') #render the deleteaccount.html page

@app.route('/accountdetails')
def viewAccountDetails():
    '''This function allows the user to view their account details.'''
    try:
        cookie = request.cookies.get('userID')  # get the cookie
        sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
        database = r"database.db"  # database file
        conn = None
        conn = sqlite3.connect(database)  # connecting to the database
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
        user = cur.fetchall()
        if not user: #deny access if the user does not exist
            return render_template('accessdenied.html')
        sessionID = user[0][9]
        cur.close()
        if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
            return render_template('accessdenied.html')
        elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    database = r"database.db" #database file
    conn = None
    try:
        conn = sqlite3.connect(database) #connecting to the database
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (cookie,)) #selecting the user details from the database
    data = cur.fetchall()
    tupleData = data[0]
    tupleData = tupleData[0],tupleData[2],tupleData[3],tupleData[4],tupleData[5],tupleData[6] #get the user details
    data = []
    data.append(tupleData)

    #return jsonify(data)
    return render_template('accountdetails.html', data1=data) #render the accountdetails.html page

@app.route('/updateaccountdetails', methods=['POST', 'GET'])
def updateAccountDetails():
    '''This function allows the user to update their account details.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: #deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    if request.method == 'POST': #get form details
        username = request.form['username']
        password = request.form['password']
        firstName = request.form['updateFirstName']
        lastName = request.form['updateLastName']
        email = request.form['updateEmail']
        phoneNumber = request.form['updatePhoneNumber']
        if not username: #validate the form details
            flash('Username is required!')
        elif not firstName:
            flash('First Name is required!')
        elif not lastName:
            flash('Last Name is required!')
        elif not email:
            flash('Email is required!')
        elif not phoneNumber:
            flash('Phone Number is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                for i in range(10): #password hashing encryption
                    password = hashlib.sha3_512(password.encode('utf-8'))
                    password = password.hexdigest()
                database = r"database.db" #database file
                conn = None
                conn = sqlite3.connect(database)    #connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (cookie,)) #querying the database to check if the username exists
                user = cur.fetchall()
                tupleUser = user[0]
                if not user: #if the username does not exist flash an error message
                    flash('User does not exist!')
                elif username != cookie:
                    flash('New Your username does not match your current username!')
                elif password != tupleUser[1]:
                    flash('Password is incorrect!')
                else:
                    cur.execute('UPDATE users SET forename = ?, surname = ?, email = ?, phone = ? WHERE username = ?', (firstName, lastName, email, phoneNumber, cookie,)) #updating the user details in the database
                    conn.commit()
                    cur.close()
                    flash('Account details updated successfully!')
                    return redirect(url_for('userhome')) #redirect to the userhome page
            except IndexError:
                flash('Error changing!')
            except IntegrityError:
                flash('User already exists!') #if the user already exists flash an error message
    return render_template('updateaccountdetails.html') #render the updateaccountdetails.html page

@app.route('/viewusers' , methods=['GET', 'POST'])
def viewUsers():
    '''This function allows the user to view their account details.'''
    try:
        cookie = request.cookies.get('userID')  # get the cookie
        sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
        database = r"database.db"  # database file
        conn = None
        conn = sqlite3.connect(database)  # connecting to the database
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
        user = cur.fetchall()
        if not user: #deny access if the user does not exist
            return render_template('accessdenied.html')
        sessionID = user[0][9]
        cur.close()
        if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
            return render_template('accessdenied.html')
        elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
            return render_template('accessdenied.html')
        tupleUser = user[0]
        userType = tupleUser[6]
        if userType != "Administrator":  # if the user is not an administrator deny access
            return render_template('adminrequiredusers.html')
        # deny access if the user does not exist
    except IndexError:
        flash('Error')
    database = r"database.db" #database file
    conn = None
    try:
        conn = sqlite3.connect(database) #connecting to the database
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT username, forename, surname, email, phone, usertype, blocked, failedLoginAttempt FROM users") #selecting the user details from the database
    data = cur.fetchall()

    #return jsonify(data)
    return render_template('viewusers.html', data1=data) #render the accountdetails.html page

@app.route('/blockuser', methods=['POST', 'GET'])
def blockUser():
    '''This function allows the user to block a user.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: #deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: #deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: #deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator":  # if the user is not an administrator deny access
        return render_template('adminrequiredusers.html')
    if request.method == 'POST':  # get form details
        username = request.form['username']
        if not username:  # validate the form details
            flash('Username is required!')
        elif username == cookie:
            flash('You cannot block yourself!')
        elif username == "Root":
            flash('Root username cannot be blocked!')
        else:
            try:
                database = r"database.db"  # database file
                conn = None
                conn = sqlite3.connect(database)  # connecting to the database
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?',(username,))  # querying the database to check if the username exists
                user = cur.fetchall()
                tupleUser = user[0]
                userBlocked = tupleUser[7]
                if not user:
                    flash('User does not exist!')
                elif userBlocked == "Yes":
                    flash('User is already blocked!')
                else:
                    blocked = "Yes"
                    cur.execute('UPDATE users SET blocked = ? WHERE username = ?', (blocked, username)) #updating the user details in the database to block the user
                    conn.commit()
                    cur.close()
                    flash('User blocked successfully!')  # flash a success message
                    return redirect(url_for('viewUsers'))  # redirect to the view users page and log the user out after blocking the account
            except IndexError:
                flash('User does not exist!')
            except IntegrityError:
                flash('User already exists!')
    return render_template('blockuser.html') # render the blockuser.html page

@app.route('/unblockuser', methods=['POST', 'GET'])
def unblockUser():
    '''This function allows the user to unblock a user.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: # deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: # deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie:  # deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator":
        return render_template('adminrequiredusers.html')
    if request.method == 'POST':
        username = request.form['username']
        if not username:
            flash('Username is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,)) # querying the database to check if the username exists
                user = cur.fetchall()
                tupleUser = user[0]
                userBlocked = tupleUser[7]
                if not user:
                    flash('User does not exist!')
                elif userBlocked == "No":
                    flash('User is not blocked!')
                else:
                    blocked = "No"
                    failedLoginAttempts = 0
                    cur.execute('UPDATE users SET blocked = ?, failedLoginAttempt = ? WHERE username = ?', (blocked, failedLoginAttempts, username)) #updating the user details in the database to unblock the user
                    conn.commit()
                    cur.close()
                    flash('User unblocked successfully!')
                    return redirect(url_for('viewUsers')) # redirect to the view users page
            except IndexError:
                flash('User does not exist!')
            except IntegrityError:
                flash('User already exists!')
    return render_template('unblockuser.html') # render the unblockuser.html page

@app.route('/deleteuser', methods=['POST', 'GET'])
def deleteUser():
    '''This function allows the user to delete a user.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: # deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: # deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: # deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator": # if the user is not an administrator deny access
        return render_template('adminrequiredusers.html')
    if request.method == 'POST': # get form details
        username = request.form['username']
        if not username: # validate the form details
            flash('Username is required!')
        elif username == cookie:
            flash('You cannot delete yourself!')
        elif username == "Root":
            flash('Root username cannot be deleted!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,)) # querying the database to check if the username exists
                user = cur.fetchall()
                if not user:
                    flash('User does not exist!')
                else:
                    cur.execute('DELETE FROM users WHERE username = ?', (username,)) # deleting the user from the database
                    conn.commit()
                    cur.close()
                    flash('User deleted successfully!')
                    return redirect(url_for('viewUsers')) # redirect to the view users page
            except IndexError:
                flash('User does not exist!')
            except IntegrityError:
                flash('User already exists!')
    return render_template('deleteuser.html') # render the deleteuser.html page

@app.route('/changeaccounttype', methods=['POST', 'GET'])
def changeAccountType():
    '''This function allows the user to change the account type of a user.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: # deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: # deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: # deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator": # if the user is not an administrator deny access
        return render_template('adminrequiredusers.html')
    if request.method == 'POST': # get form details
        username = request.form['username']
        accountType = request.form['accountType']
        if not username: # validate the form details
            flash('Username is required!')
        elif not accountType:
            flash('Account Type is required!')
        elif username == cookie:
            flash('You cannot change your own account type!')
        elif username == "Root":
            flash('Root username account type cannot be changed!')
        elif accountType != "Administrator" and accountType != "Standard":
            flash('Account Type must be Administrator or Standard (Case Sensitive)!')
        else:
            try: # change the account type
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,)) # querying the database to check if the username exists
                user = cur.fetchall()
                if not user:
                    flash('User does not exist!')
                else:
                    cur.execute('UPDATE users SET usertype = ? WHERE username = ?', (accountType, username)) # updating the account type in the database
                    conn.commit()
                    cur.close()
                    flash('Account type changed successfully!')
                    return redirect(url_for('viewUsers')) # redirect to the view users page
            except IndexError:
                flash('User does not exist!')
            except IntegrityError:
                flash('User already exists!')
    return render_template('changeaccounttype.html') # render the changeaccounttype.html page

@app.route('/changeuserpassword' , methods=['GET', 'POST'])
def changeUserPassword():
    '''This function allows the user to change the password of a user.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: # deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: # deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: # deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator": # if the user is not an administrator deny access
        return render_template('adminrequiredusers.html')
    if request.method == 'POST': # get form details
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        checkLowercase = re.search(r'[a-z]', password) # validate the password using regular expressions
        checkUppercase = re.search(r'[A-Z]', password)
        checkNumber = re.search(r'[0-9]', password)
        checkSpecialChar = re.search(r'[^A-Za-z0-9]', password)
        if not username: # validate the form details
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        elif not confirmPassword:
            flash('Confirm New Password is required!')
        elif password != confirmPassword:
            flash('New Password and Confirm New Password do not match!')
        elif not checkLowercase:
            flash('Password must contain at least one lowercase letter!')
        elif not checkUppercase:
            flash('Password must contain at least one uppercase letter!')
        elif not checkNumber:
            flash('Password must contain at least one number!')
        elif not checkSpecialChar:
            flash('Password must contain at least one special character!')
        elif len(password) < 10:
            flash('Password must be at least 10 characters long!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,)) # querying the database to check if the username exists
                user = cur.fetchall()
                tupleUser = user[0]
                emailAddress = tupleUser[4]
                unencryptedPassword = password
                if not user:
                    flash('User does not exist!')
                else:
                    try:
                        for i in range(10): # password hashing encryption
                            password = hashlib.sha3_512(password.encode('utf-8'))
                            password = password.hexdigest()
                        sendEmail(emailAddress, unencryptedPassword) # send an email to the user with the password
                        cur.execute('UPDATE users SET password = ? WHERE username = ?', (password, username)) # updating the password in the database
                        conn.commit()
                        cur.close()
                        flash('Password changed successfully!')
                        return redirect(url_for('viewUsers')) # redirect to the view users page
                    except UnicodeEncodeError:
                        flash('Error sending email. Password contains unsupported characters. Emailing passwords only supports ASCII Characters.')
            except IndexError:
                flash('Error changing!')
            except IntegrityError:
                flash('User already exists!')
    return render_template('changeuserpassword.html')

@app.route('/setup', methods=['POST', 'GET'])
def setup():
    '''This function creates root user during setup.'''
    database = r"database.db"
    conn = None
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    root = "Root"
    cur.execute('SELECT * FROM users WHERE username = ?', (root,)) # querying the database to check if the username exists
    user = cur.fetchall()
    if user: # if the root user already exists redirect to the index page
        return redirect(url_for('index'))
    conn.close()
    if request.method == 'POST':  # get form details
        username = "Root"
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        accountType = "Administrator"  # set the account type to administrator
        blocked = "No"  # set the blocked status to no
        failedLoginAttempts = 0
        checkLowercase = re.search(r'[a-z]', password)  # use regular expressions to validate the password
        checkUppercase = re.search(r'[A-Z]', password)
        checkNumber = re.search(r'[0-9]', password)
        checkSpecialChar = re.search(r'[^A-Za-z0-9]', password)
        if not firstname:  # validate the form details
            flash('First Name is required!')
        elif not lastname:
            flash('Last Name is required!')
        elif not email:
            flash('Email Address is required!')
        elif not phonenumber:
            flash('Phone Number is required!')
        elif not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        elif not confirmPassword:
            flash('Confirm Password is required!')
        elif not checkLowercase:  # validate the password
            flash('Password must contain at least one lowercase letter!')
        elif not checkUppercase:
            flash('Password must contain at least one uppercase letter!')
        elif not checkNumber:
            flash('Password must contain at least one number!')
        elif not checkSpecialChar:
            flash('Password must contain at least one special character!')
        elif len(password) < 10:  # minimum password length is 10 characters
            flash('Password must be at least 10 characters long!')
        elif password == "Root":
            flash('Password cannot be the same as the username!')
        elif password == firstname:
            flash('Password cannot be the same as the first name!')
        elif password == lastname:
            flash('Password cannot be the same as the last name!')
        elif password == email:
            flash('Password cannot be the same as the email!')
        elif password == phonenumber:
            flash('Password cannot be the same as the phone number!')
        elif password in global_var2():  # if the password is in the common passwords list flash an error message
            flash('Password is too common!')
        else:
            try:
                database = r"database.db"  # database file
                conn = None
                conn = sqlite3.connect(database)  # connecting to the database
                cur = conn.cursor()
                # cur = mysql.connection.cursor()
                # cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))  # querying the database
                user = cur.fetchall()
                cur.close()
                if user:  # if the username already exists flash an error message
                    flash('Username already exists!')
                else:
                    if password != confirmPassword:  # if the password and confirm password do not match flash an error message
                        flash('Passwords do not match!')
                    else:
                        try:
                            unencryptedPassword = password
                            for i in range(10):  # password hashing encryption
                                password = hashlib.sha3_512(password.encode('utf-8'))
                                password = password.hexdigest()
                            sessionID = random.randint(1000000000, 9999999999)  # generate a random session ID
                            setupEmail(email, unencryptedPassword)  # send an email to the user with the password
                            cur = conn.cursor()
                            cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                            username, password, firstname, lastname, email, phonenumber, accountType, blocked,
                            failedLoginAttempts, sessionID))  # inserting the user details into the database
                            conn.commit()
                            cur.close()
                            resp = make_response(render_template('readcookie.html'))  # setting the cookie connected to the username
                            resp.set_cookie('userID', username)
                            resp.set_cookie('sessionID', str(sessionID))
                            return resp
                        except UnicodeEncodeError:
                            flash('Error sending email. Password contains unsupported characters. Emailing passwords only supports ASCII Characters.')
            except IndexError:  # if there is an error caused by incorrect login details flash an error message
                flash('Username or Password is incorrect!')
    return render_template('setup.html')

@app.route('/reset', methods=['POST', 'GET'])
def reset():
    '''This function resets the Task Management System.'''
    cookie = request.cookies.get('userID')  # get the cookie
    sessionCookie = request.cookies.get('sessionID')  # get the session ID cookie
    database = r"database.db"  # database file
    conn = None
    conn = sqlite3.connect(database)  # connecting to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
    user = cur.fetchall()
    if not user: # deny access if the user does not exist
        return render_template('accessdenied.html')
    sessionID = user[0][9]
    cur.close()
    if len(sessionID) < 10: # deny access if the session ID is less than 10 characters as the session ID is always 10 characters long
        return render_template('accessdenied.html')
    elif sessionID != sessionCookie: # deny access if the session ID in the database does not match the session ID cookie
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator": # if the user is not an administrator deny access
        return render_template('adminrequiredusers.html')
    if request.method == 'POST': # get form details
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        if not password:
            flash('Password is required!')
        elif not confirmPassword:
            flash('Confirm Password is required!')
        elif password != confirmPassword:
            flash('Passwords do not match!')
        else:
            for i in range(10): # password hashing encryption
                password = hashlib.sha3_512(password.encode('utf-8'))
                password = password.hexdigest()
            if password != tupleUser[1]:
                flash('Password is incorrect!')
            else:
                try:
                    database = r"database.db"
                    conn = None
                    conn = sqlite3.connect(database)
                    cur = conn.cursor()
                    cur.execute('DELETE FROM users')  # deleting all the users from the database
                    cur.execute('DELETE FROM projects')  # deleting all the projects from the database
                    cur.execute('DELETE FROM tasks')  # deleting all the tasks from the database
                    conn.commit()
                    cur.close()
                    flash('Task Management System Reset Successfully!')
                    return redirect(url_for('index'))
                except IndexError:
                    flash('Error resetting database!')
    return render_template('reset.html')

@app.route('/testpage' , methods=['GET', 'POST'])
def testpage():
    '''This is a test page for testing purposes.'''
    return render_template('testpage.html')

@app.route('/testpage2')
def testpage2():
    '''This is a test page for testing purposes.'''
    for i in range(10):
        print("Hello World..")
    return render_template('testpage2.html')

@app.route('/test3')
def testpage3():
    '''This is a test page for testing purposes.'''
    return render_template('test3.html')


if __name__ == '__main__':
    '''This is the main function that runs the application.'''
    port = int(os.environ.get('PORT', 5000)) #port number
    app.run(debug=True, host='0.0.0.0', port=port) #run the application


