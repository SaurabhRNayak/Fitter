import flask
import json
import bicepCurls
from datetime import datetime
from flask import url_for, render_template, request, redirect
from pymongo import MongoClient

app = flask.Flask(__name__)
app.static_folder = 'static'

def connect():
    client = MongoClient()
    client = MongoClient('mongodb://localhost:27017')
    global db
    db = client['Fitter']

def insert(data):
    usersT=db.Users
    new_result = usersT.insert_many(data)
    profileT=db.Profiles
    new_result = profileT.insert_many([{
        "username":data[0]["Username"],
        "height":160,
        "calories":55,
        "BMI":24,
        "score":60
    }])
    print('Multiple posts: {0}'.format(new_result.inserted_ids))

def query(data):
    usersT=db.Users
    qresult = usersT.find_one(data)
    print(qresult)
    return(qresult)
def queryp(data):
    profileT=db.Profiles
    qresult = profileT.find_one(data)
    print(qresult)
    return(qresult)
class student:
    def __init__(self, name):
        self.name = name



@app.route('/', methods=['POST', 'GET'])
def login(a="True"):
    global flg
    flg = "True"
    print(a)
    return render_template('Loginn.html')

@app.route('/new_user', methods=['POST', 'GET'])
def new_user():
    return render_template('signup.html')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    user_name = request.form.get('Username', 'dummy')
    mail = request.form.get('Email_Id')
    age = request.form.get('Age')
    gender = request.form.get('gender')
    password = request.form.get('password')
    print(user_name,mail,age,gender,password)
    data=[{ 
        "Username":user_name, 
        "Mail":mail, 
        "Age":age,
        "Gender":gender,
        "pass":password
        }]
    connect()
    insert(data)
    query({"Username":user_name})
    return render_template('Loginn.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    global s
    global flg
    
    
    workouts = {"../static/sprint.jpeg": "Sprint",
                     "../static/shoulder.jpeg": "Shoulder","../static/abs.jpeg":"Abs"}
    favs = {"../static/BicepsCurls.jpeg": "Bicep Curls","../static/pushups.jpeg":"Pushups"}
    if flg == "Activated":
            connect()
            qp=queryp({"username":s.name})
            labels = ["BMI", "Calories Burnt", "Score"]
            values = [qp["BMI"],round(qp["calories"],1),qp["score"]]
            legend = 'My Data'
            return render_template('home_screen.html', user_name=s, Q=workouts, QA=favs, labels=labels, values=values, legend=legend)
    user_name = request.form.get('Username', 'dummy')
    password = request.form.get('password')
    connect()
    check=query({"Username":user_name})
    print(user_name, password)
    if check is not None:
        if check["pass"]== password:
            flg = "Activated"
            s = student(user_name)
            qp=queryp({"username":user_name})
            labels = ["BMI", "Calories Burnt", "Score"]
            values = [qp["BMI"],round(qp["calories"],1),qp["score"]]
            legend = 'My Data'
            return render_template('home_screen.html', user_name=s, Q=workouts, QA=favs, labels=labels, values=values, legend=legend)
    else:
        return(login("False"))


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    d = []
    with open(r"./static/blog_data.txt", 'r') as f:
        d = f.readlines()
        print(d)
    return render_template("blog.html", user_name=s, blogs=d)


@app.route('/forum', methods=['POST', 'GET'])
def forum():
    # d=None
    f = open("./static/forum_content.json", 'r')
    global d
    d = json.load(f)
    f.close()
    # print(type(d))
    # print(d)
    return render_template("forum.html", user_name=s, d=d["values"])


@app.route('/forum_ans/<idx>', methods=['POST', 'GET'])
def forum_ans(idx):
    # print("testing")
    global id
    id = idx
    da = None
    for i in d["values"]:
        if id in i['id']:
            da = i
            break
    return render_template("forum_ans.html", user_name=s, da=da)


@app.route('/forum_ans_sub', methods=['POST', 'GET'])
def forum_ans_sub():
    value = request.form.get('ans')
    for i in d["values"]:
        if id in i['id']:
            print(i)
            print(value)
            i['answer'] = value
            i['answer_ind'] = "True"
            i['ans_author'] = s.name
            json.dump(
                d, open("./flask_app/static/forum_content.json", "w"), indent=2)
            break
    return redirect(url_for('forum'))


@app.route('/leaderboard', methods=['POST', 'GET'])
def leaderboard():
    connect()
    profilesT=db.Profiles
    qresult = profilesT.find().sort("score", -1)
    m={}
    for i in qresult : 
        m[i["username"]]=i["score"]
        print(i)
    return render_template("leaderboard.html", user_name=s, da=m)


@app.route('/timer', methods=['POST', 'GET'])
def timer():
    global timex
    timex = datetime.now()
    print("timex",timex)
    return render_template("timer.html", user_name=s)

@app.route('/timer_calc', methods=['POST', 'GET'])
def timer_calc():
    now = datetime.now()
    print("acfsshj")
    print("now",(now-timex).seconds)
    calories=((now-timex).seconds)*0.102
    connect()
    profileT=db.Profiles
    result = profileT.update_one({'username': s.name}, {'$inc': {'calories': calories}})
    # pdat=queryp({"username":s.name})
    # cal=pdat["calories"]+calories
    print(result)
    return redirect(url_for('home'))

@app.route('/bicep_curl', methods=['POST', 'GET'])
def bicep_curl():
    bicepCurls.func(15)
    connect()
    profileT=db.Profiles
    result = profileT.update_one({'username': s.name}, {'$inc': {'calories': 15*0.15}})
    return redirect(url_for('home'))

if __name__ == '__main__':
    global flg
    flg = "True"
    # forum()
    app.run(debug=True)
