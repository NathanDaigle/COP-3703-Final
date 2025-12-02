import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host = os.getenv("db_host"),
    user = os.getenv("db_user"),
    password = os.getenv("db_password"),
    database = os.getenv("db_name")
)

def executeSQL(command: str):
    mycursor = mydb.cursor()
    mycursor.execute(command)

    if command.startswith("INSERT") or command.startswith("UPDATE") == True:
        mydb.commit()
        
        return {
            "affected_rows": mycursor.rowcount,
            "last_insert_id": mycursor.lastrowid
        }
    else:
        return mycursor.fetchall()