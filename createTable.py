import sqlite3
import smtplib

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE users(username varchar(40) primary key not null, password varchar(40) not null, forename varchar(40) not null, surname varchar(40) not null, email varchar(50) not null, phone varchar(20) not null, userType varchar(20) not null)')
#conn.execute('CREATE TABLE products(productID varchar(20) primary key, productName varchar(20) not null, quantity int(5) not null, price decimal(5,2) not null,prodImage text(50) not null)')
print('Users Table created successfully')
conn.execute('CREATE TABLE tasks(taskID integer(20) primary key not null, title varchar(40) not null, description text(400) not null, dueDate date not null, priority varchar(10) not null, status varchar(20) not null, projectID integer(20))')
print('Tasks Table created successfully')
conn.execute('CREATE TABLE projects(projectID integer(20) primary key not null, title varchar(40) not null, descriptiom text(400) not null, tasks text(400))')
print('Projects Table created successfully')
conn.close()

server = smtplib.SMTP('smtp-mail.outlook.com', 587)

server.starttls()

server.login("robertsona97@hotmail.co.uk", "Chinese.101")

server.sendmail("robertsona97@hotmail.co.uk", "s275931@uos.ac.uk", "Hello, this is a test email")

print("Email sent")

#Python.303