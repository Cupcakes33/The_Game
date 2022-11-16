from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()
client = MongoClient('mongodb+srv://cupcakes33:1q2w3e4r!@maindb.ozotx3u.mongodb.net/?retryWrites=true&w=majority')
db = client.db

SECRET_KEY = 'UNIVERSE'

import jwt
import datetime
import hashlib


#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"user_id": payload['id']})
        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
      #로그인 중일 경우 로그인 페이지 접근 불가할 수 있도록 설정
      token_receive = request.cookies.get('mytoken')
      try:
          payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
          return redirect(url_for("home"))
      except jwt.ExpiredSignatureError:
          return render_template('login.html')
      except jwt.exceptions.DecodeError:
          return render_template('login.html')


@app.route('/register')
def register():

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return redirect(url_for("home"))
    except jwt.ExpiredSignatureError:
        return render_template('register.html')
    except jwt.exceptions.DecodeError:
        return render_template('register.html')

#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    db.user.insert_one({'user_id': id_receive, 'user_pw': pw_hash, 'user_nickname': nickname_receive, 'score':0})

    return jsonify({'result': 'success'})


# [로그인 API]
@app.route('/api/login', methods=['POST'])
def api_login():
    login_id = request.form['login_id']
    login_pw = request.form['login_pw']

    pw_hash = hashlib.sha256(login_pw.encode('utf-8')).hexdigest()

    result = db.user.find_one({'user_id': login_id, 'user_pw': pw_hash})

    if result is not None:
        payload = {
            'id': login_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [닉네임, 유저네임 체크]
@app.route('/api/duplicate/id', methods=['GET'])
def api_duplicateCheck_id():
    id_receive = request.args.get('id_give')
    print(id_receive)
    duplicateId = db.user.find_one({'user_id': id_receive})
    print(duplicateId)
    if duplicateId == None:
        return jsonify({'result': 'not_duplicate'})
    else:
        return jsonify({'result': 'duplicate'})


@app.route('/api/duplicate/nickname', methods=['GET'])
def api_duplicateCheck_nickname():
    nickname_receive = request.args.get('nickname_give')
    print(nickname_receive)
    duplicateNickname = db.user.find_one({'user_nickname': nickname_receive})
    print(duplicateNickname)
    if duplicateNickname == None:
        return jsonify({'result': 'not_duplicate'})
    else:
        return jsonify({'result': 'duplicate'})







# [유저 정보 확인 API]
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)