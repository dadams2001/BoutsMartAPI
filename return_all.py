from flask import Flask
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

@app.route("/return_all")
def return_all():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                user='msilvest',
                                password='pwpwpwpw',
                                database='msilvest')
    with connection:
        with connection.cursor() as cursor:
            # Read all records
            cursor.execute("select * from Merch")
            result = cursor.fetchall()


        


    response_body = {
        "flaskStatusMessage": "Success!",
        "flaskMessage": result
    }

    return response_body
