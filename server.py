from flask import Flask, request, redirect, render_template
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'friend_db')
# an example of running a query


@app.route('/')
def index():
    query = "SELECT CONCAT(friends.first_name,' ', friends.last_name) AS name, friends.age, DATE_FORMAT(friends.created_at,'%M %D %Y') AS since FROM friendship JOIN users ON friendship.users_id = users.id JOIN users AS friends ON friendship.friend_id = friends.id WHERE users.id = 1;"
    friends = mysql.query_db(query)
    return render_template('index.html',friends = friends)

@app.route('/add_friend', methods=['POST'])
def process():
    name = request.form['name']
    age = request.form['age']
    query = "SELECT * FROM users WHERE CONCAT(users.first_name, ' ', users.last_name) = '{}' AND users.age = {};".format(name,age)
    temp = mysql.query_db(query)
    if(temp[0]):
        query = "INSERT INTO friendship(friendship.users_id, friendship.friend_id, friendship.created_at, friendship.updated_at) VALUE(:user_id , :friend_id, NOW() , NOW())"
        data = {
            "user_id": 1,
            "friend_id": temp[0]["id"]
        }
        mysql.query_db(query,data)
    return redirect('/')    

app.run(debug=True)