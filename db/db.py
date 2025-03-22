import mysql.connector

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'lucin2022',
    'database':'db_emails'
}


def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn
