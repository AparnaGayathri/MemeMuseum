from flask import Flask, render_template, request, session  
import requests
import ibm_db
import re
import json
import webbrowser
app = Flask(__name__)
app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;UID=zvx10976;PASSWORD=D91uDoGA3fSKiqJx;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt;", "", "")
print("Connection successful")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/meme')
def about1():
    return render_template('meme.html')


@app.route('/logout')
def about4():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        # name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM REGISTER1 WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO REGISTER1 VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM REGISTER1 WHERE email =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account['EMAIL']
            userid = account['EMAIL']
            session['email'] = account['EMAIL']
            msg = 'Logged in successfully !'
            return render_template('meme.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
            return render_template('loginmeme.html', msg=msg)
    else:
        msg = 'Incorrect username / password !'
        return render_template('loginmeme.html', msg=msg)

@app.route('/test',methods=['POST','GET'])
def meme():
    if request.method == 'POST':
        keywords = request.form["key"]
        print(keywords)

        url = "https://humor-jokes-and-memes.p.rapidapi.com/memes/search"

        querystring = {"keywords":keywords,"media-type":"image","keywords-in-image":"false","min-rating":"3","number":"3"}

        headers = {
            "X-RapidAPI-Key": "f6aa295cbbmsh1d9ad874863152fp18d768jsn2d83efd33da1",
            "X-RapidAPI-Host": "humor-jokes-and-memes.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        print(response.json())
        print(response.text)
        output = json.loads(response.text)
        print(output)
        op1 = output['memes'][0]['url']
        op2 = output['memes'][1]['url']
    return render_template('memeoutput.html',output1=op1,output2=op2)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')