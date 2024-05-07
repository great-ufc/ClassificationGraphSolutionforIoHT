import mysql.connector
from mysql.connector import Error
import pandas as pd
from utils import cesarDecriptor

connection = None
connection_db = None
db_name = None

#Connection configurations
host_name = 'localhost' 
user_name = 'root'
pw = cesarDecriptor('itgcv2C',2) #my pc

#create connection
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

###Funcions for Database
#Create Database
def create_database(connection, DatabaseName):
    cursor = connection.cursor()
    try:
        sql  = "CREATE DATABASE "+ DatabaseName
        cursor.execute(sql)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

#Drop Database
def drop_database(connection, DatabaseName):
    cursor = connection.cursor()
    try:
        cursor.execute("DROP DATABASE "+ DatabaseName)
        print("Database dropped successfully")
    except Error as err:
        print(f"Error: '{err}'")

#Create DB Connection
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def initServerConnection():
    return create_server_connection(host_name, user_name, pw)

def initDBConnection():
    return create_db_connection(host_name, user_name, pw, db_name)
    




