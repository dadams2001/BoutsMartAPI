from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS
import pymysql
import os
import datetime

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
                Date_Sold = datetime.date.today()

                # Get the Current Max Sale_ID
                query = "SELECT max(SALE_ID) FROM Sales"
                cursor.execute(query)
                Max_Sale_ID = cursor.fetchone()

                # Insert New Sale Into Sale Database
                sql_sale = f"INSERT INTO Sales (SALE_ID, ITEM_ID, SIZE, PRICE, QUANTITY_SOLD, DATE_SOLD) VALUES ('{Max_Sale_ID[0] + 1}', '{Sale_Item_ID}', '{Sale_Size}', '{Sale_Price}', '{Quantity_Sold}', '{Date_Sold}')" 
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

@app.route("/add_item", methods=['GET','POST'])
def AddItem():
    
    if (request.method=="POST"):
        vars=request.get_json()

        # Connect to the database 
        connection = pymysql.connect(host='localhost',
                                user='msilvest',
                                password='pwpwpwpw',
                                database='msilvest')
        
        with connection.cursor() as cursor:
            New_Item_ID = vars["prod_id"]
            New_Item_Size = vars["size"]
            New_Item_Cat = vars["category"]
            New_Item_Price = vars["price"]
            New_Item_Sub_Cat = vars["sub_cat"]
            New_Item_Disc = vars["disc"]
            New_Item_Color = vars["color"]
            New_Item_Gender = vars["gender"]
            New_Item_Quantity = vars["quantity"]
            New_Item_Box = vars["box"]
            New_Item_Shelf = vars["shelf"]
            New_Item_Location = vars["location"]

            # get the current max item number
            query = "SELECT max(ITEM_ID) FROM Merch_Test"
            cursor.execute(query)
            Max_Item_ID = cursor.fetchone()

            # Insert New Item Into Sale Database
            sql_add_item = f"INSERT INTO Merch_Test (ITEM_ID, SIZE, CATEGORY, PRICE, SUB_CATEGORY, DISCONTINUED, COLOR, GENDER, QUANTITY, BOX, SHELF, LOCATION) VALUES ('{Max_Item_ID[0] + 1}', '{New_Item_Size}', '{New_Item_Cat}', '{New_Item_Price}', '{New_Item_Sub_Cat}', '{New_Item_Disc}', '{New_Item_Color}',  '{New_Item_Gender}',  '{New_Item_Quantity}',  '{New_Item_Box}',  '{New_Item_Shelf}',  '{New_Item_Location}')" 
            cursor.execute(sql_add_item)
        
        response = "we did it chief"
        connection.commit()
    
    elif (request.method=="GET"):
        response="we got it"

   
    response_body = {
        "flaskStatusMessage": "Success!",
        "flaskMessage": response
    }

    return response_body 


@app.route("/analytics")
def return_data():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                user='msilvest',
                                password='pwpwpwpw',
                                database='msilvest')
    with connection:
        with connection.cursor() as cursor:
            # Bar Chart 1 (How much money each merch item made across every night)
            cursor.execute("SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED FROM Sales GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10;")
            result1 = cursor.fetchall()
            
            # Bar Chart 2 (How much money each merch item made in night 1)
            cursor.execute("SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-7' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10;")
            result2 = cursor.fetchall()
            
            # Bar Chart 3 (How much money each merch item made in night 2)
            cursor.execute("SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-10' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10;")
            result3 = cursor.fetchall()
            
            # Bar Chart 4 (How much money each merch item made in night 3)
            cursor.execute("SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-16' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10;")
            result4 = cursor.fetchall()

    response_body = {
        "status" : "success",
        "bar chart data1": result1,
        "bar chart data2": result2,
        "bar chart data3": result3,
        "bar chart data4": result4,
    }

    return response_body
