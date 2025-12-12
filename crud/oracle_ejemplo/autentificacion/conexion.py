import oracledb
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

with oracledb.connect(
     user=username, 
     password=password, 
     dsn=dsn
     ) as connection:
    with connection.cursor() as cursor:
        sql = "select sysdate from dual"
        for row in cursor.execute(sql):
            for column in row:
                print(column)

""" CREDENCIALES
ORACLE_USER="C##ANGELO_ZAMORA"
ORACLE_DSN="10.50.1.0/xe"
ORACLE_PASSWORD="Inacap#2025" 
"""