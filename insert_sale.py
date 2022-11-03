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
            New_Sale_ID = 1
            Sale_Item_ID = 111001
            Sale_Size = 'S'
            Sale_Price = 30.00
            Quantity_Sold = 1

            # Insert new sale
            sql_sale = f"INSERT INTO Sale_Trial (Sale_ID, Item_ID, Size, Price, Quantity_Sold) VALUES ('{New_Sale_ID}', '{Sale_Item_ID}', '{Sale_Size}', '{Sale_Price}', '{Quantity_Sold}')"
            # cursor.execute("INSERT INTO Sale_Trial (Sale_ID, Item_ID, Size, Price, Quantity_Sold) VALUES (1, 111001, 'S', 30.00, 1)");
            cursor.execute(sql_sale); 
       
            # Update Merch Quantity
            sql_quantity = f"UPDATE Merch_Trial SET Quantity = Quantity - '{Quantity_Sold}' WHERE Item_ID = '{Sale_Item_ID}' AND Size = '{Sale_Size}'"
               
            cursor.execute(sql_quantity);

        connection.commit()

    response_body = {
        "flaskStatusMessage": "Success!",
        "flaskMessage": "we did it!"
    }

    return response_body
