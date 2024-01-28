from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

messages = ["h","sd","asd","asdfasdf","asdfasdfsaf"]



def read_file(file_name):
    file = open(file_name,"r")
    data = file.read()
    file.close()
    return data

def first_number():
    data = read_file("users.csv")
    data = data.split("\n")
    needed = data[-1].split(",")
    if needed[-1] == 'email':
        return 0
    else:
        return int(needed[-1])

def save_new_user(user,user_number):
    users = open('users.csv',"a") 
    users.write(f"\n{user['name']},{user['username']},{user['password']},{user['email']},{user_number}")
    users.close()

@app.route("/failure")
def failure():
    return render_template('fail.html')

@app.route("/create_login", methods=['POST','GET'])
def create_login():
    return render_template('account_creation.html')

@app.route("/temp/create_login", methods=['POST','GET'])
def create_login_temp():
    if request.method == "POST":
        new_user = {}
        new_user['name'] = request.form['name']
        new_user['username'] = request.form['username']
        new_user['password'] = request.form['password']
        new_user['email'] = request.form['email']
        print(f"{new_user['name']},{new_user['username']},{new_user['password']},{new_user['email']}")

        if new_user["name"] == "" or new_user['username'] == "" or new_user['password'] == "" or new_user['email'] == "":
            print("failed")
            return redirect("/create_login")
        else:
            last_user_number = first_number() + 1
            save_new_user(new_user,last_user_number)
            return redirect('/')

@app.route('/users/<name>',methods = ["POST","GET"])
def users_page(name):
    return render_template('Main.html',msgs = messages)


def check_user(username,password):
    content = read_file()
    content = content.split("\n")
    for users in range(1,len(content)):
        login = content[users].split(",")
        if login[0] == username and login[0] == password:
            return True
    return False


@app.route('/temp/login_master', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['Username']
        password = request.form['Password']
        
        if user != "":
            return redirect(url_for('users_page',name = user))
        else:
            return redirect('/failure')

@app.route('/login',methods=['POST','GET'])
@app.route('/',methods=['POST','GET'])
def login_page():
    return render_template("index.html")

#host="127.0.0.1"
app.run(debug=True,port=8080,host="172.17.226.129")