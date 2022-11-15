from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib

ca = certifi.where()
client = MongoClient('mongodb+srv://cupcakes33:1q2w3e4r!@maindb.ozotx3u.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.db
SECRET_KEY = 'UNIVERSE'


#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg='토큰이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg='로그인 정보가 존재하지 않습니다.'))

@app.route('/login')
def login():
    msg = request.args.get('msg')
    return render_template('login_page.html', msg=msg)

@app.route('/register')
def register():
    return render_template('login_page.html')

# @app.route('/api/login', methods=['POST'])
# def api_login():

@app.route('/api/login', methods=['POST'])
def api_login():
    login_id = request.form['login_id']
    login_pw = request.form['login_pw']

    pw_hash = hashlib.sha256(login_pw.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id':login_id, 'pw':pw_hash})

    if result is not None:
        payload = {
            'id': login_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result':'success', 'token':token})
    else:
        return jsonify({'result':'fail', 'msg':'invalid ID or PW'})


# @app.rout('/api/register', methods=['POST'])
# def api_register():
#     regist_id = request.form['regist_id']
#     regist_pw = request.form['regist_pw']
#     regist_nickname = request.form['regist_nickname']
#
#     pw_hash = hashlib.sha256(regist_pw.encode('utf-8')).hexdigest()
#
#


# 랭킹 확인 부분
@app.route('/rank')
def rank():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.find_one({"user_id": payload['id']})
        return render_template('rank.html', nickname=user_info["user_nickname"],score=user_info["score"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route("/ranks", methods=["GET"])
def rank_get():
    data = list(db.find({}, {'_id': False}))

    return jsonify({'data': data})


@app.route("/ranks", methods=["POST"])
def rank_post():
    data = json.loads(request.form['data'])
    user_Id = data['user_id']
    score = int(data['score'])

    db.update_one({'user_id': user_Id},{'$set':{'score':score}})

    return jsonify({'msg': '스코어 업데이트 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
