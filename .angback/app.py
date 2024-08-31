from flask import Flask,request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost"
)

CREATE_TABLE =""" CREATE TABLE IF NOT EXISTS angularone (
               id SERIAL PRIMARY KEY,
               name VARCHAR(200) NOT NULL,
               email VARCHAR(100) NOT NULL UNIQUE,
               phonenumber VARCHAR(11) NOT NULL,
               password VARCHAR(255) NOT NULL); """

INSERT_INFO = """INSERT INTO angularone (name,email,phonenumber,password) 
                 VALUES (%s,%s,%s,%s)"""

SELECT_INFO = """ SELECT * FROM angularone WHERE email= %s """

UPDATE_INFO = """ UPDATE angularone SET password= %s WHERE email= %s """

DELETE_INFO = """ DELETE FROM angularone WHERE email= %s"""

@app.post("/register")
def register():
    data = request.get_json()
    name=data["name"]
    email=data["email"]
    phonenumber=data["phonenumber"]
    password=data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE)
            cursor.execute(INSERT_INFO, (name,email,phonenumber,password,))
    return {"message":"register Successful."},201

@app.post("/login")
def login():
    data = request.get_json()
    email=data["email"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_INFO,(email,))
            user_email = cursor.fetchone()

            if user_email:
                return{"message":"Email is there"},201
            else:
                return{"message": "Email is not there"},404
            
@app.post ("/update")
def update():
    data =request.get_json()
    email=data["email"]
    new_password=data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_INFO,(email,))
            user_email =cursor.fetchone()

            if user_email:
                cursor.execute(UPDATE_INFO,(new_password,email))
                connection.commit()
                return {"message":"Password change successful"},201
            else:
                return{"message":"Email is Not Found"},404

@app.post("/delete")
def delete():
    data = request.get_json()
    email = data["email"]
    with connection.cursor()as cursor:
        cursor.execute(SELECT_INFO,(email,))
        user_email = cursor.fetchone()

        if user_email:
            cursor.execute(DELETE_INFO,(email,))
            connection.commit()
            return{"message":"User Delete Successful"},201
        else:
            return{"message":"User Not Fount"},404
        
if __name__ == "__main__":
    app.run(debug=True)