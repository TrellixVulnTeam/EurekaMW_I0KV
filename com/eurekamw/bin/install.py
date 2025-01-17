"""
    Prerequisites :
        1. Install mysql server. Use following command to install:
            sudo apt-get install mysql-server
        2. Install mysql-connector library in python

    Note:- Please create 'eureka' user before running this file. Use following commands to create the user and grant all the privileges to it.
            1. CREATE USER 'eureka' IDENTIFIED BY 'eurek@';
            2. CREATE DATABASE eureka;
            3. GRANT ALL PRIVILEGES ON eureka.* TO eureka;

    Use following command to check whether user is created or not
        select USER FROM mysql.user;

"""

import mysql.connector

from com.eurekamw.utils import DBUtils as dbu, UserUtils as uutils
from com.eurekamw.model import UserFile as uf

dbQueries = 'SHOW DATABASES'

sqlQueries = ('CREATE TABLE users (username VARCHAR(255), name VARCHAR(255), password VARCHAR(255), PRIMARY KEY(username))',
              'CREATE TABLE list (username VARCHAR(255), listname VARCHAR(255), description TEXT, wordlist TEXT, PRIMARY KEY(username, listname))',
              'CREATE TABLE words (word VARCHAR(255), category VARCHAR(255), stems TEXT, shortdef TEXT, xdef TEXT, PRIMARY KEY(word))')


def create_schema():
    try:
        # Get the db connection
        connection = dbu.get_connection()
        if connection is None:
            print("Unable to get mysql db object")
            return

        cursor = connection.cursor()

        # Create schemas
        for query in sqlQueries:
            print("Executing: %1s" % (query))
            cursor.execute(query)

        # Insert admin data
        print("Adding admin user")
        admin_user = uf.User('administrator', 'Admin', 'password')
        uutils.add_user(admin_user)

    except mysql.connector.Error as error:
        print('Failed to get record from database: {}'.format(error))
        return False

    finally:
        # Closing database connection
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print('MySQL connection is closed')


def __init__():
    create_schema()


__init__()
