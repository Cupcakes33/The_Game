from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib
import time

app = Flask(__name__)

ca=certifi.where()
client = MongoClient('')
db = client.db

SECRET_KEY = ''

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.thegame.find_one({"user_id": payload['id']})
        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return render_template('login.html', msg="로그인 유지 시간이 만료되어, 재 로그인이 필요합니다.")
    except jwt.exceptions.DecodeError:
        return render_template('login.html', msg="로그인 후 이용 가능합니다.")

@app.route('/game')
def game():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.thegame.find_one({"user_id": payload['id']})
        return render_template('game.html', nickname=user_info['user_nickname'])
    except jwt.ExpiredSignatureError:
        return render_template('login.html', msg="로그인 유지 시간이 만료되어, 재 로그인이 필요합니다.")
    except jwt.exceptions.DecodeError:
        return render_template('login.html', msg="로그인 후 이용 가능합니다.")


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
    db.thegame.insert_one({'user_id': id_receive, 'user_pw': pw_hash, 'user_nickname': nickname_receive, 'score':0,'sub_score':0})
    # db.thegame.insert_one({'user_id': id_receive, 'authority':)
    return jsonify({'result': 'success'})


# [로그인 API]
@app.route('/api/login', methods=['POST'])
def api_login():
    login_id = request.form['login_id']
    login_pw = request.form['login_pw']

    pw_hash = hashlib.sha256(login_pw.encode('utf-8')).hexdigest()

    result = db.thegame.find_one({'user_id': login_id, 'user_pw': pw_hash})

    if result is not None:
        payload = {
            'id': login_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [닉네임, 유저네임 체크]
@app.route('/api/duplicate/id', methods=['GET'])
def api_duplicateCheck_id():
    id_receive = request.args.get('id_give')
    duplicateId = db.thegame.find_one({'user_id': id_receive})

    if duplicateId == None:
        return jsonify({'result': 'not_duplicate'})
    else:
        return jsonify({'result': 'duplicate'})


@app.route('/api/duplicate/nickname', methods=['GET'])
def api_duplicateCheck_nickname():
    nickname_receive = request.args.get('nickname_give')

    duplicateNickname = db.thegame.find_one({'user_nickname': nickname_receive})

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

        userinfo = db.thegame.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route('/rank')
def rank():

    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.thegame.find_one({"user_id": payload['id']})
        return render_template('rank.html', nickname=user_info['user_nickname'], sub_score=user_info['sub_score'], score=user_info['score'])
    except jwt.ExpiredSignatureError:
        return render_template('login.html', msg="로그인 유지 시간이 만료되어, 재 로그인이 필요합니다.")
    except jwt.exceptions.DecodeError:
        return render_template('login.html', msg="로그인 후 이용 가능합니다.")


@app.route('/rank/game_end')
def rank_game_end():

    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.thegame.find_one({"user_id": payload['id']})
        return render_template('rank.html', nickname=user_info['user_nickname'], sub_score=user_info['sub_score'], score=user_info['score'], game_end=1)
    except jwt.ExpiredSignatureError:
        return render_template('login.html')
    except jwt.exceptions.DecodeError:
        return render_template('login.html')


@app.route("/ranks", methods=["GET"])
def rank_get():
    data = list(db.thegame.find({}, {'_id': False}))
    return jsonify({'data': data})


@app.route("/game", methods=["POST"])
def web_game_post():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.thegame.find_one({"user_id": payload['id']})

    user_id = user_info['user_id']
    sub_score = int(request.form['score_give'])

    db.thegame.update_one({'user_id': user_id}, {'$set': {'sub_score' : sub_score}})

    re_user_info = db.thegame.find_one({"user_id": payload['id']})

    re_score = int(re_user_info['score'])
    re_sub_score = int(re_user_info['sub_score'])

    if re_score < re_sub_score :
        db.thegame.update_one({'user_id': user_id}, {'$set': {'score' : re_sub_score}})

    return jsonify({'result': 'success'})

@app.route('/user', methods=['GET'])
def web_firstweek1_get():
   comment_list = list(db.thegame_comments.find({}, {'_id': False}))
   return jsonify({'comments':comment_list})

@app.route('/api/report', methods=['POST'])
def report_user():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    report_user = payload['id']

    date = request.form['date']
    comments_info = db.thegame_comments.find_one({'date': date})

    if report_user not in comments_info['report_user']:
        comments_info['report_user'].append(report_user)
        db.thegame_comments.update_one({'date': date}, {'$set': {
            'report_user': comments_info['report_user'],
            'report_count': comments_info['report_count'] + 1}})
        return jsonify({'msg': '신고가 완료되었습니다 !'})
    else:
        return jsonify({'msg': '이미 신고를 한 댓글입니다'})



@app.route('/user', methods=['POST'])
def web_firstweek1_post():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.thegame.find_one({"user_id": payload['id']})
    comments_counter = db.thegame_comments_counter.find_one({"space_name": 'thegame_comments_counter'})['comments_count']
    user_id = user_info['user_id']
    user_nickname = user_info['user_nickname']
    comment = request.form['comment']
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    doc = {
        '_id': comments_counter + 1,
       'user_ID':user_id,
       'user_nickname': user_nickname,
       'comment':comment,
        'date': date,
        'report_user' : [],
        'report_count': 0,
    }
    db.thegame_comments.insert_one(doc)
    db.thegame_comments_counter.update_one({'space_name': 'thegame_comments_counter'}, {'$set': {'comments_count' : comments_counter + 1}})
    return jsonify({'msg': 'saved comment'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
