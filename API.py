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
            
            # Pie Chart 1 (How much money each merch item made across every night)
            cursor.execute("SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales)*100 as TOTAL_MONEY_RAISED FROM Sales GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;")
            result5 = cursor.fetchall()
            
            # Pie Chart 2 (How much money each merch item made in night 1)
            cursor.execute("SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-7')*100 as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-7' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;")
            result6 = cursor.fetchall()
            
            # Pie Chart 3 (How much money each merch item made in night 2)
            cursor.execute("SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-10')*100 as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-10' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;")
            result7 = cursor.fetchall()
            
            # Pie Chart 4 (How much money each merch item made in night 3)
            cursor.execute("SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-16')*100 as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-16' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;")
            result8 = cursor.fetchall()
            
            # Gender Bar Chart 1 (How much money each merch item made across every night)
            cursor.execute("SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE) New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC;")
            result9 = cursor.fetchall()
            
            # Gender Bar Chart 2 (How much money each merch item made in night 1)
            cursor.execute("SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-7') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC;")
            result10 = cursor.fetchall()
            
            # Gender Bar Chart 3 (How much money each merch item made in night 2)
            cursor.execute("SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-10') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC;")
            result11 = cursor.fetchall()
            
            # Gender Bar Chart 4 (How much money each merch item made in night 3)
            cursor.execute("SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-16') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC;")
            result12 = cursor.fetchall()
            
            # Gender Pie Chart 1 (How much money each merch item made across every night)
            cursor.execute("SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales)*100 as TOTAL_MONEY_RAISED FROM Sales GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;")
            result13 = cursor.fetchall()
            
            # Gender Pie Chart 2 (How much money each merch item made in night 1)
            cursor.execute("SELECT Final.GENDER as GENDER, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-7')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-7') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC) Final;")
            result14 = cursor.fetchall()

            # Gender Pie Chart 3 (How much money each merch item made in night 2)
            cursor.execute("SELECT Final.GENDER as GENDER, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-10')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-10') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC) Final;")
            result15 = cursor.fetchall()
            
            # Gender Pie Chart 4 (How much money each merch item made in night 3)
            cursor.execute("SELECT Final.GENDER as GENDER, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-16')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-16') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC) Final;")
            result16 = cursor.fetchall()
            
            # Category Bar Chart 1 (How much money each merch item made across every night)
            cursor.execute("SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE) New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC;")
            result17 = cursor.fetchall()
            
            # Category Bar Chart 2 (How much money each merch item made in night 1)
            cursor.execute("SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-7') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC;")
            result18 = cursor.fetchall()
            
            # Category Bar Chart 3 (How much money each merch item made in night 2)
            cursor.execute("SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-10') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC;")
            result19 = cursor.fetchall()
            
            # Category Bar Chart 4 (How much money each merch item made in night 3)
            cursor.execute("SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-16') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC;")
            result20 = cursor.fetchall()

            # Category Pie Chart 1 (How much money each merch item made across every night)
            cursor.execute("SELECT Final.CATEGORY as CATEGORY, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales)*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE) New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC) Final;")
            result21 = cursor.fetchall()
            
            # Category Pie Chart 2 (How much money each merch item made in night 1)
            cursor.execute("SELECT Final.CATEGORY as CATEGORY, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-7')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-7') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC) Final;")
            result22 = cursor.fetchall()
            
            # Category Pie Chart 3 (How much money each merch item made in night 2)
            cursor.execute("SELECT Final.CATEGORY as CATEGORY, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-10')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-10') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC) Final;")
            result23 = cursor.fetchall()
            
            # Category Pie Chart 4 (How much money each merch item made in night 3)
            cursor.execute("SELECT Final.CATEGORY as CATEGORY, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-16')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-16') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC) Final;")
            result24 = cursor.fetchall()

    response_body = {
        "status" : "success",
        "bar chart data1": result1,
        "bar chart data2": result2,
        "bar chart data3": result3,
        "bar chart data4": result4,
        "pie chart data5": result5,
        "pie chart data6": result6,
        "pie chart data7": result7,
        "pie chart data8": result8,
        "gender bar chart1": result9,
        "gender bar chart2": result10,
        "gender bar chart3": result11,
        "gender bar chart4": result12,
        "gender pie chart1": result13,
        "gender pie chart2": result14,
        "gender pie chart3": result15,
        "gender pie chart4": result16,
        "category bar chart1": result17,
        "category bar chart2": result18,
        "category bar chart3": result19,
        "category bar chart4": result20,
        "category pie chart1": result21,
        "category pie chart2": result22,
        "category pie chart3": result23,
        "category pie chart4": result24,
    }

    return response_body

@app.route("/newanalytics")
def return_new_data():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                user='msilvest',
                                password='pwpwpwpw',
                                database='msilvest')
    with connection:
        with connection.cursor() as cursor:
            # Bar Chart 1 (How much money each merch item made across every night)
            query1 = "SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED FROM Sales GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10;"
            result1 = cursor.execute(query1)
            result1 = cursor.fetchall()
            
    result_dict = {col1:(col2, col3) for (col1, col2, col3, col4, col5) in cursor.fetchall()}

    return result_dict
