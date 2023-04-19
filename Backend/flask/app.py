from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from urllib.parse import urlparse
from crontab import CronTab
import subprocess
import requests
import json


output = subprocess.check_output(['pwd'])
output_str = output.decode('utf-8').split('\n')

output_u = subprocess.check_output(['whoami'])
output_user = output_u.decode('utf-8').split('\n')

#set the crontab and cmd to run 
cron = CronTab(user=output_user[0])

# Establish a connection to the database
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="akhil",
  password="akhil@05",
  database="amazon_tracker"
)

# Create a cursor object to execute the query
cursor = mydb.cursor()

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/register', methods=['PUT'])
def register():
    email = request.json['email']
    full_name = request.json['fullName']

    # Define the INSERT query
    query = "INSERT INTO user_info (email, full_name) VALUES (%s, %s)"

    # Define the values to insert into the table
    values = (email, full_name)

    # Execute the query with the values
    cursor.execute(query, values)

    # Commit the changes to the database
    mydb.commit()

    # Print a message to confirm the insert was successful
    print(cursor.rowcount, "record inserted.")
    return "<p>Content updated</p>"

@app.route('/login', methods=['PUT'])
def login():
    # for getting the full name for the user
    email = request.json['email']

    select_query = "SELECT full_name FROM user_info WHERE email = %s"

    # Execute the SELECT query with the email parameter
    cursor.execute(select_query, (email, ))

    # Get the current price from the first row of the query results
    full_name = cursor.fetchone()[0]
    return jsonify({'full_name': full_name})

@app.route('/track', methods=['PUT'])
def track():
    #var 
    link = request.json['link']
    toggleValue = int(request.json['toggleValue'])
    email = request.json['email']
    enableNotification = 0

    # Get the ASIN for the product
    url = link 
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    #var
    asin = path_segments[3]

    #one time API call outside the cron-job
    url_api = "https://amazon-product-price-data.p.rapidapi.com/product"

    querystring = {"asins":asin,"locale":"US"}

    headers = {
        "X-RapidAPI-Key": "9ed674538amshdcb9838f5a86f98p11ff43jsnbbfd1b11af6d",
        "X-RapidAPI-Host": "amazon-product-price-data.p.rapidapi.com"
    }

    response = requests.request("GET", url_api, headers=headers, params=querystring)

    print(response.content)

    decoded_response = response.content.decode('utf-8')

    # Parse the JSON string into a Python object (in this case, a list)
    response_list = json.loads(decoded_response)

    # Access the asin value of the first item in the list
    current_price = response_list[0]['current_price']
    image_url = response_list[0]['image_url']
    product_name = response_list[0]['product_name']

    # Print the asin value
    current_price = str(current_price)
    image_url = str(image_url)
    product_name = str(product_name)
    tog_val = str(toggleValue)

    cmd = 'python3 ' + output_str[0] + '/asin.py ' + asin + ' ' + email + ' ' + tog_val

    #insert all the values in the DB
    # Define the insert statement
    sql = "INSERT INTO email_tracker (email, ASIN, amazon_link, product_name, image_link, cron_command, curr_price, notification_status, type_of_notification) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # Define the values to insert
    values = (email, asin, link, product_name, image_url, cmd, current_price, enableNotification, toggleValue)

    # Execute the insert statement with the values
    cursor.execute(sql, values)

    # Commit the changes to the database
    mydb.commit()

    if toggleValue == 0:
        #create the cron-job
        job = cron.new(command=cmd)
        job.minute.every(1)
    elif toggleValue == 1:
        #create the cron-job
        job = cron.new(command=cmd)
        job.hour.every(12)

    # write the cron job to the cron tab
    cron.write()
    print('Cron job created')
    
    return jsonify({'email':email, 'productName':product_name,'asinServer': asin,
                    'imageUrl': image_url, 'currentPrice': current_price, 'productLink': link})


@app.route('/fetchCards', methods=['PUT'])
def fetchCards():
    email = request.json['email']
    # Execute a SELECT statement with a WHERE clause to retrieve the desired data
    cursor.execute("SELECT ASIN, amazon_link, product_name, image_link, curr_price FROM email_tracker WHERE email = %s", (email,))

    # Fetch all rows of the resultset
    resultset = cursor.fetchall()
    rows = []
    for row in resultset:
        rows.append({
            "email": email,
            "productName": row[2],
            "asinServer": row[0],
            "imageUrl": row[3],
            "currentPrice": str(row[4]),
            "productLink": row[1]
        })

    # Convert the list of dictionaries into a JSON object
    json_data = json.dumps(rows)

    # Print the JSON object
    print(json_data)
    return json_data


@app.route('/toggleNotification', methods=['PUT'])
def toggleNotification():
    pass

@app.route('/remove', methods=['PUT'])
def remove():
    asin = request.json['asin']

    # Get the command to remove.

    sqlCommand = "SELECT cron_command FROM email_tracker WHERE ASIN = %s"
    cursor.execute(sqlCommand, (asin,))

    cron_command = str(cursor.fetchone()[0])
    job_to_remove = cron.find_command(cron_command) 
    cron.remove(job_to_remove)

    cron.write()

    # Commit the changes to the database
    mydb.commit()

    sql = "DELETE FROM email_tracker WHERE ASIN = %s"
    cursor.execute(sql, (asin,))
    # Commit the changes to the database
    mydb.commit()

    return "<p>Content removed</p>"