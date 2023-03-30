#import statements
from dotenv import load_dotenv
import os
from subprocess import check_output
import pymysql
import json

cur = 0
connection = 0

def load_and_connect():
    global cur
    global connection
    # create environment variables
    load_dotenv()
    os.environ['HOST']='us-east.connect.psdb.cloud'
    os.environ['USERNAME']='n78y64ogqtzpe3dxbx8b'
    os.environ['PASSWORD']='pscale_pw_BoPSBFtKTmbOOC1efH9OwxISk9Yx7jcUCIEAv1F1Xe5'
    os.environ['DATABASE']='flext-db'
    
    connection = pymysql.connect(
        host= os.getenv("HOST"),
        user=os.getenv("USERNAME"),
        password= os.getenv("PASSWORD"),
        database= os.getenv("DATABASE"),
        ssl = {
        "ca": "static/cacert.pem"
      }
    )

    cur = connection.cursor()
    return cur


def fetch_records():
    global cur
    global connection
    sql_select_Query = "select * from bolic;"
    cur.execute(sql_select_Query)
    connection.commit()
    records = cur.fetchall()
    return json.dumps(records)
    

def exec_custom_query(query):
    global cur
    global connection
    cur = connection.cursor()
    cursor = connection.cursor()
    resp = cursor.execute(query)
    # get all records
    records = cursor.fetchall()
    return resp

def insert_phone_number(number='00000000000'):
    global cur
    insert_ph = 'INSERT INTO bolic(number) VALUES(%s);'
    args = (number, )
    resp = cur.execute(insert_ph, args)
    return resp 
    
    
def close_all():
    global connection
    global cur
    connection.close()
    cur.close()



    """
    New user:
Sign up or login, click sign up and ‘log in’ with google. Greet with ‘Hello {user}’ with google pic, welcome to flext!
Dashboard: past workout log table, friends list, username or email and load their google profile pic, and frequency. All fields are editable upon clicking ‘edit’.

L1: login, if user in table then user info is shown with their friends, frequency, email, username. Flask checks if current date and current user has an entry in db. If yes, render “You have already uploaded” template. If not: ‘Upload’ button is there, can upload picture and then shows confirmation of date, time and picture.
There is a ‘form’ button that will render the form, but this time it will UPDATE db instead of creating new.
If user not in table, render form.html and get user info.

    """

# ret = load_and_connect()
# print(ret)
# data = json.loads(fetch_records())
# print(type(data))
# print(data)