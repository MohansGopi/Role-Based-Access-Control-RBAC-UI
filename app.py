
#required libraries
from flask import Flask,request,render_template,redirect,session,make_response
from flask_jwt_extended import set_access_cookies,create_access_token,jwt_required,JWTManager
from secret_ket import jwt_secret_key,flask_secret_key
from datetime import timedelta
import time
import json
from bcrypt import *
from hmac import compare_digest


#flask and jwt init
app = Flask(__name__)

#variable for the logics
login_attempt:int = 0
stat_time, waiting_time = 1,0
create_acnt = ''

#required configuration of jwt
app.secret_key = flask_secret_key
app.config['JWT_SECRET_KEY'] =jwt_secret_key
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)


#index file rendering from flask server
@app.route('/',methods=['POST','GET'])
def main():
    global login_attempt,create_acnt #login attempts
    if 'is_logged_in' not in session:
        if request.method == 'POST':
            #login logics
            name = request.form['user_name']
            password = request.form['paswd']

            #getting user_data from database
            file = open("user_database/user_credentials.json")
            user_cred = json.loads(file.read())

            #checking the user name is in the data base
            user_name_in_database = dict()
            for data in user_cred['cred']:
                if compare_digest(name,data['user_id']):
                    user_name_in_database = data
            if user_name_in_database =={}:
                create_acnt = "Create a account"
                return redirect("/register")

            if checkpw(password.encode("utf-8"),user_name_in_database['password'].encode("utf-8")):

                session['user_id']=user_name_in_database['user_id']
                session['is_logged_in'] = True
                session['user_role'] = user_name_in_database['role']
                #implementing jwt
                #create atoken
                access_token = create_access_token(identity=session['user_id'])

                resp = make_response(render_template("index.html",name = session['user_id']))
                set_access_cookies(resp, access_token)

                return resp
            else:
                login_attempt+=1
                return redirect('/login')
        return redirect("/login")
    else:
        return render_template('index.html',name = session['user_id'])

#login page rendering
@app.route("/login")
def login_page():
    global login_attempt
    global stat_time, waiting_time
    if "is_logged_in" not in session:
        if login_attempt==4:
            stat_time = time.time()
            waiting_time = 600  # seconds - 10 mins
            login_attempt+=1
        elif login_attempt>=10:
            stat_time = time.time()
            waiting_time = 3600 #seconds - 1hr
            login_attempt = 0
        elapsed_time = time.time() - stat_time  # Calculate elapsed time

        if elapsed_time <= waiting_time : # 600 seconds = 10 minutes
            return render_template("blocked_page.html",set_time = waiting_time)
        else:
            if login_attempt>=1:
                return render_template("login.html",error="Invalid credentials")
            return render_template("login.html")
    else:
        return redirect("/")
#register logic
@app.route("/register",methods=['POST','GET'])
def register_page():
    global create_acnt
    if 'is_logged_in' not in session:
        if request.method == 'POST':
            f_name = request.form['first_name']
            l_name = request.form['last_name']
            email = request.form['email']
            role = request.form['role']
            password = request.form['passwd']
            password_re = request.form['passwd_re']

            #input validation
            if (len(f_name)<10 and len(l_name)<10
                    and 8<=len(password)<=20 and 8<=len(password_re)<=20 and password == password_re):
                user_data = dict()
                user_data['user_id'] = f"{f_name}_{l_name}"
                user_data['first name'] = f_name
                user_data['last name'] = l_name
                user_data['email'] = email
                user_data['role'] = role
                user_data['password'] = (hashpw(password.encode('utf-8'), salt=gensalt())).decode('utf-8')
                user_data['re-password'] = (hashpw(password_re.encode('utf-8'), salt=gensalt())).decode('utf-8')

                try:
                    file = open("user_database/user_credentials.json")
                except:
                    file = open("user_database/user_credentials.json", "w")
                    init_dit = {"cred": []}
                    json.dump(init_dit, file)
                    file = open("user_database/user_credentials.json")

                data_file = json.loads(file.read())
                data_file['cred'].insert(0,user_data)
                file = open('user_database/user_credentials.json','w')
                json.dump(data_file,file,indent=4)
                return redirect("/login")
    return render_template("register.html",error = create_acnt)

#logout logic
@app.route("/logout")
def logout_logic():
    session.clear()
    resp = make_response(redirect("/login"))
    for cookie_name in request.cookies:
        resp.delete_cookie(cookie_name)
    return resp


#protected data
@app.route("/protected",methods=['POST','GET'])
@jwt_required()
def protected_page():
    project_det = "The client want to built a so called google map for find the location of dora's house"
    company_det = "investment : 70000 USD ; profit : 10000 USD "
    employee_det = "Name : 'xxx';age:45"
    msg = "ACCESS DENIED"
    data = request.form.get("role")
    if (data == 'employee_details' or data == "project details") and session['user_role'] == 'MANAGER':
        if data=="employee_details":
            msg = employee_det
        elif data=='project details':
            msg = project_det
        return render_template("index.html",name=session['user_id'],protected_msg = msg)
    elif (data == 'firm details' or data == 'employee_details' or data == "project details") and session['user_role']=='ADMIN':
        if data=="employee_details":
            msg = employee_det
        elif data=='project details':
            msg = project_det
        elif data == 'firm details':
            msg = company_det
        return render_template('index.html',name=session['user_id'],protected_msg=msg)
    if data == 'project details' and session['user_role'] == 'EMPLOYEE':
        msg = project_det
        return render_template('index.html',name=session['user_id'],protected_msg=msg)
    else:
        return render_template('index.html',name=session['user_id'],protected_msg=msg)


if __name__ == "__main__":
    app.run(debug=True)

