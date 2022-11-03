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
            Sale_Item_ID = 111003
            Sale_Size = 'L'
            Sale_Price = 30.00
            Quantity_Sold = 1

            # Get the Current Max Sale_ID
            query = "SELECT max(Sale_ID) FROM Sale_Trial"
            cursor.execute(query);
            Max_Sale_ID = cursor.fetchone()

            # Insert New Sale Into Sale Database
            sql_sale = f"INSERT INTO Sale_Trial (Sale_ID, Item_ID, Size, Price, Quantity_Sold) VALUES ('{Max_Sale_ID[0] + 1}', '{Sale_Item_ID}', '{Sale_Size}', '{Sale_Price}', '{Quantity_Sold}')"
            cursor.execute(sql_sale); 
       
            # Update Merch Quantity Into Merch Database
            sql_quantity = f"UPDATE Merch_Trial SET Quantity = Quantity - '{Quantity_Sold}' WHERE Item_ID = '{Sale_Item_ID}' AND Size = '{Sale_Size}'"
            cursor.execute(sql_quantity);

        connection.commit()

    response_body = {
        "flaskStatusMessage": "Success!",
        "flaskMessage": Max_Sale_ID
    }

    return response_body
