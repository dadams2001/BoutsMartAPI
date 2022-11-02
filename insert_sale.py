from flask import Flask
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

@app.route("/insert_sale")
def return_all():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                user='msilvest',
                                password='pwpwpwpw',
                                database='msilvest')
    with connection:
        with connection.cursor() as cursor:
            # Sale_ID = 1
            # Item_ID = 111001
            # Price = 30.00
            # Quantity_Sold = 1

            # Insert new record
            # sql = f"insert into 'Sale_Trial' ('Sale_ID', 'Item_ID', 'Size', 'Price', 'Quantity_Sold') VALUES ('{Sale_ID}', '{Item_ID}', '{Size}', '{Price}', '{Quantity_Sold}')"
            cursor.execute("INSERT INTO Sale_Trial (Sale_ID, Item_ID, Size, Price, Quantity_Sold) VALUES (1, 111001, 'S', 30.00, 1)");
            # cursor.execute(sql); 
        
        connection.commit()

    response_body = {
        "flaskStatusMessage": "Success!",
        "flaskMessage": "we did it!"
    }

    return response_body
