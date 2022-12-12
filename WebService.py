from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
import mysql.connector

app = Flask(__name__)
api = Api(app)

class Submit(Resource):

    def post(self):
        customer_id=request.json.get('CustomerID')
        first_name=request.json.get('FirstName')
        last_name=request.json.get('LastName')
        phone=request.json.get('Phone')
        street=request.json.get('Street')
        city=request.json.get('City')
        state=request.json.get('State')
        zip=request.json.get('Zip')
        sql=f'INSERT INTO customers VALUES ({customer_id}, {first_name}, {last_name}, {phone}, {street}, {city}, {state}, {zip})'
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='customers'
        )
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(sql)
        self.mydb.commit()
        self.mydb.close()


api.add_resource(Submit, '/submit')
app.run()