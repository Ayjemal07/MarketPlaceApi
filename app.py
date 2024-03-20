from flask import render_template,jsonify
import time
from flask import Flask
from flask import request
from flask import session
from flask import redirect
import json
import requests
import mysql.connector
# from flask_mysqldb import MySQL

app = Flask(__name__)

# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'bargainbin'


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="bargainbin"
)


@app.route('/get_users')
def get_users():
    all_users = []
    try:
        # Create MySQL cursor
        with app.app_context():
            # Get a cursor from the MySQL connection
            #  cur = mysql.connection.cursor()
            # Execute the query to fetch users
            cur = mydb.cursor()
            cur.execute("SELECT * FROM users")
            # Fetch all users
            users = cur.fetchall()
            for each in users:
                all_users.append(
                    {
                        'name': each[0],
                        'pass': each[1]
                    }
                )
            # Close the cursor
            
            cur.close()
            # Return the users as JSON response
            print(all_users)

            return jsonify(all_users)
    except Exception as e:
        # Print any exception that occurs
        print("An error occurred:", str(e))
        return jsonify({"error": "An error occurred while fetching users."})




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST','GET'])
def login():
    all_users = []
    with app.app_context():
        # Get a cursor from the MySQL connection
        #  cur = mysql.connection.cursor()
        # Execute the query to fetch users
        cur = mydb.cursor()
        cur.execute("SELECT * FROM users")
        # Fetch all users
        users = cur.fetchall()
        print(users)
        for each in users:
            all_users.append(
                {
                    'name': each[0],
                    'pass': each[1]
                }
            )
        # Close the cursor
        
        cur.close()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(username,password)
        for user in all_users:
            if username == user['name'] and password == user['pass']:
                # Login successful
                print("successful login")
                return render_template('login.html', is_logged_in=True)
        
    
    print("not success login")
    return render_template('login.html', is_logged_in=False)










base_url = 'http://127.0.0.1:5000'

# Send a GET request to the '/get_users' endpoint
# response = requests.get(f'{base_url}/get_users')

# Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Print the JSON response containing users
#     print(response.json())
# else:
#     print('Error:', response.status_code)


if __name__ == '__main__':
    app.run(debug=True)

# print("Hello: {}".format(dir(get_users())))
