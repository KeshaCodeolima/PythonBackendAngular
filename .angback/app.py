from flask import Flask,request
from flask_cors import CORS
import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

SELECT_INFO2=""" SELECT * FROM angularone WHERE email= %s AND password= %s"""

UPDATE_INFO = """ UPDATE angularone SET password= %s WHERE email= %s """

DELETE_INFO = """ DELETE FROM angularone WHERE email= %s"""

SECRET_KEY ="erhifhdh@49938djk"

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
    password=data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_INFO2,(email,password,))
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

@app.post("/forgetemail")
def forget():
    data = request.get_json()
    email = data["email"]
    with connection.cursor()as cursor:
        cursor.execute(SELECT_INFO,(email,))
        user_email = cursor.fetchone()

        if user_email:
            try:
                sender_email = "kulasekarakeshan41@gmail.com"
                receiver_email = email
                password = "vyyr wswn uknj ahvp"


                reset_link = f"http://localhost:4200/froget"

                subject = "Password Reset Link."
                body = f"""
                Hi, 

                We received a request to reset your password. If this was you, click the link below to reset it:
                        {reset_link}
                This Email link expire in 2 minutes.
                If this wasn't you, please ignore this email.
                """

                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject

                message.attach(MIMEText(body, "plain"))

                with smtplib.SMTP("smtp.gmail.com",587)as server:
                    server.starttls()
                    server.login(sender_email, password)
                    text = message.as_string()
                    server.sendmail(sender_email,receiver_email,text)
                    return{"message" : "Email Send Successful"},201
            except Exception as e:
                return{"message" : "Email send fail because of : "+ str(e)} 
        else:
            return{"message" : "Email not found."}

        
if __name__ == "__main__":
    app.run(debug=True)