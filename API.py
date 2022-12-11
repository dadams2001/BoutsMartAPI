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
            qry = "select * from Merch"
            cursor.execute(qry)
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

def convert_data(data_list):
    keys = ['name', 'value']

    data_objs = [dict(zip(keys, sublst)) for sublst in data_list]
    return data_objs

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
            qry1="SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED FROM Sales GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10;"
            cursor.execute(qry1)
            result1 = cursor.fetchall()
            new_result1=convert_data(result1)
           
            # Bar Chart 2 (How much money each merch item made in night 1)
            qry2="SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-7' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10;"
            cursor.execute(qry2)
            result2 = cursor.fetchall()
            new_result2=convert_data(result2)
            
            # Bar Chart 3 (How much money each merch item made in night 2)
            qry3="SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-10' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10;"
            cursor.execute(qry3)
            result3 = cursor.fetchall()
            new_result3=convert_data(result3)
            
            # Bar Chart 4 (How much money each merch item made in night 3)
            qry4="SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-16' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10;"
            cursor.execute(qry4)
            result4 = cursor.fetchall()
            new_result4=convert_data(result4)

            # Pie Chart 1 (How much money each merch item made across every night)
            qry5="SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales)*100 as TOTAL_MONEY_RAISED FROM Sales GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;"
            cursor.execute(qry5)
            result5 = cursor.fetchall()
            new_result5=convert_data(result5)
            
            # Pie Chart 2 (How much money each merch item made in night 1)
            qry6="SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-7')*100 as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-7' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;"
            cursor.execute(qry6)
            result6 = cursor.fetchall()
            new_result6=convert_data(result6)
            
            # Pie Chart 3 (How much money each merch item made in night 2)
            qry7="SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-10')*100 as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-10' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;"
            cursor.execute(qry7)
            result7 = cursor.fetchall()
            new_result7=convert_data(result7)
            
            # Pie Chart 4 (How much money each merch item made in night 3)
            qry8="SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-16')*100 as TOTAL_MONEY_RAISED FROM Sales WHERE DATE_SOLD = '2022-11-16' GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;"
            cursor.execute(qry8)
            result8 = cursor.fetchall()
            new_result8=convert_data(result8)
            
            # Gender Bar Chart 1 (How much money each merch item made across every night)
            qry9="SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE) New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC;"
            cursor.execute(qry9)
            result9 = cursor.fetchall()
            new_result9=convert_data(result9)
            
            # Gender Bar Chart 2 (How much money each merch item made in night 1)
            qry10="SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-7') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC;"
            cursor.execute(qry10)
            result10 = cursor.fetchall()
            new_result10=convert_data(result10)
            
            # Gender Bar Chart 3 (How much money each merch item made in night 2)
            qry11="SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-10') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC;"
            cursor.execute(qry11)
            result11 = cursor.fetchall()
            new_result11=convert_data(result11)
            
            # Gender Bar Chart 4 (How much money each merch item made in night 3)
            qry12="SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-16') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC;"
            cursor.execute(qry12)
            result12 = cursor.fetchall()
            new_result12=convert_data(result12)
            
            # Gender Pie Chart 1 (How much money each merch item made across every night)
            qry13="SELECT New.ITEM_ID, ROUND(New.TOTAL_MONEY_RAISED, 2) FROM (SELECT ITEM_ID, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales)*100 as TOTAL_MONEY_RAISED FROM Sales GROUP BY ITEM_ID ORDER BY TOTAL_MONEY_RAISED DESC LIMIT 10) New;"
            cursor.execute(qry13)
            result13 = cursor.fetchall()
            new_result13=convert_data(result13)
            
            # Gender Pie Chart 2 (How much money each merch item made in night 1)
            qry14="SELECT Final.GENDER as GENDER, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-7')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-7') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC) Final;"
            cursor.execute(qry14)
            result14 = cursor.fetchall()
            new_result14=convert_data(result14)

            # Gender Pie Chart 3 (How much money each merch item made in night 2)
            qry15="SELECT Final.GENDER as GENDER, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-10')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-10') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC) Final;"
            cursor.execute(qry15)
            result15 = cursor.fetchall()
            new_result15=convert_data(result15)
            
            # Gender Pie Chart 4 (How much money each merch item made in night 3)
            qry16="SELECT Final.GENDER as GENDER, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.GENDER as GENDER, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-16')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-16') New GROUP BY New.GENDER ORDER BY TOTAL_MONEY_RAISED DESC) Final;"
            cursor.execute(qry16)
            result16 = cursor.fetchall()
            new_result16=convert_data(result16)
            
            # Category Bar Chart 1 (How much money each merch item made across every night)
            qry17="SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE) New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC;"
            cursor.execute(qry17)
            result17 = cursor.fetchall()
            new_result17=convert_data(result17)
            
            # Category Bar Chart 2 (How much money each merch item made in night 1)
            qry18="SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-7') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC;"
            cursor.execute(qry18)
            result18 = cursor.fetchall()
            new_result18=convert_data(result18)
            
            # Category Bar Chart 3 (How much money each merch item made in night 2)
            qry19="SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-10') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC;"
            cursor.execute(qry19)
            result19 = cursor.fetchall()
            new_result19=convert_data(result19)
            
            # Category Bar Chart 4 (How much money each merch item made in night 3)
            qry20="SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD) as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-16') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC;"
            cursor.execute(qry20)
            result20 = cursor.fetchall()
            new_result20=convert_data(result20)

            # Category Pie Chart 1 (How much money each merch item made across every night)
            qry21="SELECT Final.CATEGORY as CATEGORY, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales)*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE) New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC) Final;"
            cursor.execute(qry21)
            result21 = cursor.fetchall()
            new_result21=convert_data(result21)
            
            # Category Pie Chart 2 (How much money each merch item made in night 1)
            qry22="SELECT Final.CATEGORY as CATEGORY, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-7')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-7') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC) Final;"
            cursor.execute(qry22)
            result22 = cursor.fetchall()
            new_result22=convert_data(result22)
            
            # Category Pie Chart 3 (How much money each merch item made in night 2)
            qry23="SELECT Final.CATEGORY as CATEGORY, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-10')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-10') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC) Final;"
            cursor.execute(qry23)
            result23 = cursor.fetchall()
            new_result23=convert_data(result23)
            
            # Category Pie Chart 4 (How much money each merch item made in night 3)
            qry24 = "SELECT Final.CATEGORY as CATEGORY, ROUND(Final.TOTAL_MONEY_RAISED, 2) FROM (SELECT New.CATEGORY as CATEGORY, SUM(PRICE*QUANTITY_SOLD)/(select SUM(PRICE*QUANTITY_SOLD) FROM Sales WHERE DATE_SOLD = '2022-11-16')*100 as TOTAL_MONEY_RAISED from (select Sales.ITEM_ID, Sales.SIZE, Sales.PRICE, Sales.QUANTITY_SOLD, Sales.DATE_SOLD, Merch.CATEGORY, Merch.SUB_CATEGORY, Merch.GENDER from Sales, Merch WHERE Sales.ITEM_ID = Merch.ITEM_ID AND Sales.SIZE = Merch.SIZE AND Sales.DATE_SOLD = '2022-11-16') New GROUP BY New.CATEGORY ORDER BY TOTAL_MONEY_RAISED DESC) Final;"
            cursor.execute(qry24)
            result24 = cursor.fetchall()
            new_result24=convert_data(result24)

    response_body = {
        "status" : "success",
        "bar_chart_data1": new_result1,
        "bar_chart_data2": new_result2,
        "bar_chart_data3": new_result3,
        "bar_chart_data4": new_result4,
        "pie_chart_data5": new_result5,
        "pie_chart_data6": new_result6,
        "pie_chart_data7": new_result7,
        "pie_chart_data8": new_result8,
        "gender_bar_chart1": new_result9,
        "gender_bar_chart2": new_result10,
        "gender_bar_chart3": new_result11,
        "gender_bar_chart4": new_result12,
        "gender_pie_chart1": new_result13,
        "gender_pie_chart2": new_result14,
        "gender_pie_chart3": new_result15,
        "gender_pie_chart4": new_result16,
        "category_bar_chart1": new_result17,
        "category_bar_chart2": new_result18,
        "category_bar_chart3": new_result19,
        "category_bar_chart4": new_result20,
        "category_pie_chart1": new_result21,
        "category_pie_chart2": new_result22,
        "category_pie_chart3": new_result23,
        "category_pie_chart4": new_result24,
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
    
    

    return new_result1
