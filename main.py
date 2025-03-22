from flask import Flask, request, jsonify
from tools.algo import predict
import mysql.connector
from db.db import get_db_connection

import logging
from flask_cors import CORS 

app = Flask(__name__)


CORS(app, origins=['http://localhost:5173']) # Activer CORS pour toute l'application
app.config['MYSQL_CONNECTION'] = get_db_connection() # Maintient la connexion en mémoire

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




@app.route("/sendEmail", methods=["POST"])
def send_email():
    if request.method == "POST":
        data = request.get_json()
        to = data.get("to")
        subject = data.get("subject")
        message = data.get("message")

        pred = predict(subject + " " + message)
        try:
             conn = get_db_connection()
             cursor = conn.cursor()
             cursor.execute('INSERT INTO emails(from_email,subject,message,is_spam) VALUES(%s,%s,%s,%s)',(to,subject,message,pred.tolist()[0]))
             conn.commit()
             cursor.close()
             conn.close()
             return jsonify({
                 'message':'message envoyer avec succsé'
             })
             
        except mysql.connector.Error as err:
            return jsonify({
                "error": f"Erreur lors de l'insertion dans la base de données: {err}"
            }),500
       
    


@app.route('/getAllEmails',methods=['GET'])
def getEmails():
    if request.method == 'GET':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM emails')
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns,row)) for row in rows]

            cursor.close()
            conn.close()
            return jsonify({
                "data":result
            })
            
            
        except mysql.connector.Error as error: 
            return jsonify({
                "error":error
            })
        

@app.route('/SpamEmails',methods=['GET'])
def getSpamEmails():
        if request.method == 'GET': 
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM emails WHERE is_spam=1')
                rows = cursor.fetchall()

                columns = [desc[0] for desc in cursor.description]

                result = [dict(zip(columns,row)) for row in rows]
                return jsonify({
                    "data":result
                })
                
            except mysql.connector.Error as err :
                return jsonify({
                    "error":err
                })
        
@app.route('/hamEmails',methods=['GET'])
def getHamEmails():
    if request.method == 'GET': 
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM emails WHERE is_spam=0')
            rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns,row)) for row in rows]
            return jsonify({
                "data":result
            })
        except mysql.connector.Error as err: 
            return jsonify({
                "error":err
            })


if __name__ == "__main__":
    app.run(debug=True)
