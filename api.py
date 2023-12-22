from flask import Flask, make_response, jsonify, request
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

def data_fetchall(sql_query):
    conn = mysql.connection.cursor()
    conn.execute(sql_query)
    data = conn.fetchall()
    conn.close()

    return data

@app.route("/client", methods=["GET"])
def get_client():
    query = """SELECT * FROM client_fees.clients;"""
    data = data_fetchall(query)

    return make_response(jsonify(data), 200)

@app.route("/client/<int:id>", methods=["GET"])
def get_client_by_id(id):
    query = f"""SELECT * FROM client_fees.clients where client_id = {id};"""
    data = data_fetchall(query)

    return make_response(jsonify(data), 200)

@app.route("/client/<int:id>/projects", methods=["GET"])
def get_client_projets(id):
    query = f"""SELECT projects.project_name, CONCAT(YEAR(project_start_date), " - " ,YEAR(project_end_date)) as project_year FROM clients 
                INNER JOIN projects on clients.client_id = projects.client_id WHERE clients.client_id = {id};"""
    data = data_fetchall(query)

    return make_response(jsonify({"client_id": id, "count": len(data), "projects": data}), 200)

@app.route("/client", methods=["POST"])
def add_client():
    conn = mysql.connection.cursor()
    info = request.get_json()
    client_name = info['client_name']
    work_date = info['work_date']
    avg_datebillings = info['avg_datebillings']
    projectcount_kpi = info['projectcount_kpi']

    query = f"""INSERT INTO `client_fees`.`clients` (`client_name`, `work_date`, `avg_datebillings`, `projectcount_kpi`) 
                VALUES ('{client_name}','{work_date}','{avg_datebillings}','{projectcount_kpi}')"""
    conn.execute(query)

    mysql.connection.commit()
    rows_added = conn.rowcount
    print(f"Rows ADDED : {rows_added}")
    conn.close()

    return make_response(jsonify({"message": "Added Successfully", "row_added": rows_added}), 201)

@app.route("/client/<int:id>", methods=["PUT"])
def update_client(id):
    conn = mysql.connection.cursor()
    info = request.get_json()
    client_name = info['client_name']
    work_date = info['work_date']
    avg_datebillings = info['avg_datebillings']
    projectcount_kpi = info['projectcount_kpi']

    query = f"""UPDATE `client_fees`.`clients` SET `client_name` = '{client_name}', `work_date` = '{work_date}', 
                `avg_datebillings`= '{avg_datebillings}', `projectcount_kpi`= '{projectcount_kpi}'
                WHERE client_id = {id}"""
    conn.execute(query)

    mysql.connection.commit()
    rows_update = conn.rowcount
    print(f"Rows UPDATE : {rows_update}")
    conn.close()

    return make_response(jsonify({"message": "Updated Successfully", "row_updated": rows_update}), 200)

@app.route("/client/<int:id>", methods=["DELETE"])
def delete_client(id):
    conn = mysql.connection.cursor()
    query = f"""DELETE FROM `client_fees`.`clients` WHERE (`client_id` = '{id}');"""
    conn.execute(query)
    mysql.connection.commit()
    rows_delete = conn.rowcount
    conn.close()

    return make_response(jsonify({"message": "Updated Successfully", "row_deleted": rows_delete}), 200)

if __name__ == "__main__":
    app.run(debug=True)