from flask import Flask, make_response, jsonify, request, render_template, session
from flask_mysqldb import MySQL
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# inlcude database
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "12345"
app.config['MYSQL_DB'] = "client_fees"

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

app.config['SECRET_KEY'] = '86f342b22484426eb61f220f10f17e48'

mysql = MySQL(app)

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is Missing!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            kwargs['token_payload'] = payload

        except jwt.ExpiredSignatureError:
            return jsonify({'Alert!': 'Token has expired!'})
        except jwt.InvalidTokenError as e:
            return jsonify({'Alert!': f'Invalid Token: {str(e)}'})
        except jwt.PyJWTError as e:
            return jsonify({'Alert!': f'JWT Error: {str(e)}'})
        return func(*args, **kwargs)
    
    return decorated


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('base.html')
    else:
        return 'Logged in currently'

@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '12345678':
        session['logged_in'] = True
        token = jwt.encode({
                'user': request.form['username'],
                'expiration': str(datetime.utcnow() + timedelta(seconds=120))
            }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed!'})

def data_fetchall(sql_query):
    conn = mysql.connection.cursor()
    conn.execute(sql_query)
    data = conn.fetchall()
    conn.close()

    return data

# Get Endpoints ==========================================================================================================
@app.route("/client", methods=["GET"])
@token_required
def get_client(token_payload):
    query = """SELECT * FROM client_fees.clients;"""
    data = data_fetchall(query)

    return make_response(jsonify(data), 200)

@app.route("/client/<int:id>", methods=["GET"])
@token_required
def get_client_by_id(token_payload, id):
    format_type = request.args.get("format", "json")
    query = f"""SELECT * FROM client_fees.clients WHERE client_id = {id};"""
    data = data_fetchall(query)

    if format_type.lower() == "xml":
        response = make_response(jsonify(data), 200)
        response.headers["Content-Type"] = "application/xml"
        return response
    else:
        return make_response(jsonify(data), 200)
    

@app.route("/client/<int:id>/projects", methods=["GET"])
@token_required
def get_client_projets(token_payload, id):
    query = f"""SELECT projects.project_name, CONCAT(YEAR(project_start_date), " - " ,YEAR(project_end_date)) as project_year FROM clients 
                INNER JOIN projects on clients.client_id = projects.client_id WHERE clients.client_id = {id};"""
    data = data_fetchall(query)

    return make_response(jsonify({"client_id": id, "count": len(data), "projects": data}), 200)

# http://127.0.0.1:5000/client/search?criteria=pasamonte
@app.route("/client/search", methods=["GET"])
@token_required
def search_clients(token_payload):
    criteria = request.args.get("criteria")
    query = f"""SELECT * FROM client_fees.clients WHERE client_name LIKE '%{criteria}%';"""
    data = data_fetchall(query)

    return make_response(jsonify(data), 200)

# Post Endpoint ==========================================================================================================
@app.route("/client", methods=["POST"]) 
@token_required
def add_client(token_payload):
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

# Put Endpoint ==========================================================================================================
@app.route("/client/<int:id>", methods=["PUT"])
@token_required
def update_client(token_payload, id):
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

# Delete Endpoint ==========================================================================================================
@app.route("/client/<int:id>", methods=["DELETE"])
@token_required
def delete_client(token_payload, id):
    conn = mysql.connection.cursor()
    query = f"""DELETE FROM `client_fees`.`clients` WHERE (`client_id` = '{id}');"""
    conn.execute(query)
    mysql.connection.commit()
    rows_delete = conn.rowcount
    conn.close()

    return make_response(jsonify({"message": "Deleted Successfully", "row_deleted": rows_delete}), 200)

if __name__ == "__main__":
    app.run(debug=True)