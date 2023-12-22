from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app =  Flask(__name__)

# inlcude database
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "12345"
app.config['MYSQL_DB'] = "client_fees"

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
    return "<p> Hello World </p>"

@app.route("/client")
def get_client():
    conn = mysql.connection.cursor()
    query = "SELECT * FROM client_fees.clients;"
    conn.execute(query)
    data = conn.fetchall()
    conn.close()

    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)