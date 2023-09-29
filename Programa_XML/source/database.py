import mysql.connector

def connect_db(host,user,password,database):

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database = database
    )
    return connection