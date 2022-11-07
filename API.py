from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)

picFolder = os.path.join('static', 'merchPics')
app.config['UPLOAD FOLDER'] = picFolder

@app.route("/")
def hello_world():

    hello = "hello from Flask!"

    response_body = {
        "statusMessage": "Success!",
        "flaskMessage": hello
    }

    return response_body

@app.route("/pics/<pic_id>")
def pics(pic_id):

    pic1 = os.path.join(app.config['UPLOAD FOLDER'], f'{pic_id}.png')
    pic1 = os.path.join("..", pic1)
    return render_template("pics.html", user_image=pic1)

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
        "status" : "success",
        "data": result
    }

    return response_body

@app.route("/insert_sale",methods=['GET','POST'])
def insert_sale():

    if (request.method=="POST"):
        vars=request.get_json()

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='msilvest',
                                    password='pwpwpwpw',
                                    database='msilvest')
        with connection:
            with connection.cursor() as cursor:
                
                Sale_Item_ID = vars["prod_id"]
                Sale_Size = vars["size"]
                Sale_Price = vars["price"]
                Quantity_Sold = vars["quantity"]

                # Get the Current Max Sale_ID
                query = "SELECT max(SALE_ID) FROM Sales"
                cursor.execute(query)
                Max_Sale_ID = cursor.fetchone()

                # Insert New Sale Into Sale Database
                sql_sale = f"INSERT INTO Sales (SALE_ID, ITEM_ID, SIZE, PRICE, QUANTITY_SOLD) VALUES ('{Max_Sale_ID[0] + 1}', '{Sale_Item_ID}', '{Sale_Size}', '{Sale_Price}', '{Quantity_Sold}')"
                cursor.execute(sql_sale)
        
                # Update Merch Quantity Into Merch Database
                sql_quantity = f"UPDATE Merch SET QUANTITY = QUANTITY - '{Quantity_Sold}' WHERE ITEM_ID = '{Sale_Item_ID}' AND SIZE = '{Sale_Size}'"
                cursor.execute(sql_quantity)

            response = "we did it chief"
            connection.commit()

    elif (request.method=="GET"):
        response="we got it"

   
    response_body = {
        "flaskStatusMessage": "Success!",
        "flaskMessage": response
    }

    return response_body
