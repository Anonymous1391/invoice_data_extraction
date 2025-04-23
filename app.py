from flask import Flask , jsonify , render_template, request,send_from_directory
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from app.database import get_db # To access DB
import project_config
import datetime

app = Flask(__name__)

app.config ["JWT_SECRET_KEY"] = "secret-key"
jwt = JWTManager(app)

user_collection = get_db() # DB 

# making webpage
@app.route("/")
def home():
    return send_from_directory("templates", "login.html")

# API for webpage as variable
@app.route("/<page>")
def serve_page(page):
    return send_from_directory("templates", page)

#API for register
@app.route("/register", methods = ["POST"])
def register():
    user_data = request.form
    name = user_data.get("name"," ")
    username = user_data.get("username", " ")
    password = user_data.get("password"," ")
    email_id = user_data.get("email_id"," ")
    mobile_number = user_data.get("mobile_number"," ")
    dob = user_data.get("dob"," ")

    response = user_collection.find_one({"email_id":email_id})
    if not response:
        user_collection.insert_one({"name":name ,"username":username ,"password":password,
                                 "email_id":email_id,"mobile_number":mobile_number ,"dob":dob })
        
        return jsonify({"status":"success","message":"User Register Successfully"})
    
    else:
        return jsonify({"status":"Error","message":"User Already Existes"})

#API for login
@app.route("/login", methods = ["POST"])
def login():
    user_data = request.form
    username = user_data.get("username", " ")
    password = user_data.get("password"," ")
    response = user_collection.find_one({"username":username,"password":password})
    if response:
        access_token = create_access_token(identity = username, expires_delta= datetime.timedelta(hours=2))
        print("access_token", access_token)
        return jsonify({"status":"success","message":"Login Successful"," token":access_token})
    else:
        return jsonify({"status":"Error","message":"Ivalid Credentials"})

#API for fogot password
@app.route("/forgot", methods = ["POST"])
def forgot_password():
    user_data = request.form
    email_id = user_data.get("email_id", " ")
    dob = user_data.get("dob"," ")
    new_password = user_data.get("new_password"," ")
    response = user_collection.find_one({"email_id":email_id,"dob":dob})
    if response:
        user_collection.update_one({"email_id":email_id,"dob":dob},
                                {"$set":{"password":new_password}})
        return jsonify({"status":"success","message":"Password Updated Successfully"})
        
    else:
        return jsonify({"status":"Error","message":"User Not Exist"})

#API for calculator
@app.route("/calculator", methods = ["POST"])
@jwt_required()
def calculator():
    data = request.form
    x = eval(data["x"])
    y = eval(data["y"])
    operation = data["operation"]
    if operation == "addition":
        result = x + y

    elif operation == "subtraction":
        result = x - y

    elif operation == "multiplication":
        result = x * y

    elif operation == "division":
        result = x / y
    
    return jsonify({"status":"Success","result":result})



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5004, debug = True)