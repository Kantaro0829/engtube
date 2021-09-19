from flask import Flask, jsonify, make_response, request, abort
import json
import base64
import pymysql
import requests
import time
import datetime
import hashlib#ハッシュ化用
import jwt
from sqlalchemy import exc, func
from flask_cors import CORS, cross_origin


from setting import session# セッション変数の取得
from user import *# Userモデルの取得

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=['GET'])
@cross_origin(supports_credentials=True)
def index():
    return jsonify({"name": "Kantaro", "stand":"The World"})

@app.route("/new_user_reg", methods=["POST"])
@cross_origin(supports_credentials=True)
def new_user_reg():
    '''
    受け取るJSON : user_info[]
    {
        "name": String,
        "password": String,
        "email": String
    }
    '''
    start = time.time()#計測開始
    user_info = json.loads(request.get_data().decode())

    #user table にレコードの追加
    try:
        user = User()
        user.name = user_info['name']
        user.password = hashlib.sha256(user_info['password'].encode()).hexdigest()
        user.mail = user_info['email']

        session.add(user)#insert
        session.flush()
        session.commit()#commit

        jwt_payload={}

        jwt_payload['id'] = user.id

        key = "secret_key_goes_here"
        encoded = jwt.encode(jwt_payload, key, algorithm="HS256")
        print(encoded)

        elapsed_time = time.time() - start

        session.close()

        return jsonify({
            "status": 200,
            "token": encoded,
            "elapsedTimeOfLoginService": elapsed_time
        })
    except exc.SQLAlchemyError as e:
        message = None
        if type(e) is exc.IntegrityError:
            message = "メールアドレスがすでに登録されています"
            elapsed_time = time.time() - start
            print(type(e))
            return jsonify({
                "status": 400,
                "message": message,
                "elapsedTime": elapsed_time
            })
        elapsed_time = time.time() - start
        return jsonify({"status":400, "massage":"DBに問題あるかも", "elapsedTime": elapsed_time})




@app.route("/login", methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    '''
    受け取るjson: user_info[]
    {
        "email": mail,
        "password": password
    }
    '''
    start = time.time()
    user_info = json.loads(request.get_data().decode())
    try:

        user = User()#User テーブルレコード参照開始
        # mail_existance = session.query(func.count(User.mail)).\
        #     filter(User.mail == user_info['email'])
        # print("メールアドレスの個数：", mail_existance, "type:", type(mail_existance))

        auth_pass = session.query(User.password).\
            filter(User.mail == user_info['email']).\
                one()
        
        print(auth_pass[0]+"　は　"+str(user_info['email'])+"　のパスワード！！")

        #パスワードをハッシュ化して比較
        if hashlib.sha256(user_info['password'].encode()).hexdigest() == auth_pass[0]:


            id = session.query(User.id).\
                filter(User.mail == user_info['email']).\
                    one()
            
            print("変数idの中身は：", id)
            print("変数idの中身は：", id[0])
            #print("変数idの中身は：", len(id))
            jwt_payload={}

            jwt_payload['id'] = id[0]

            key = "secret_key_goes_here"
            encoded = jwt.encode(jwt_payload, key, algorithm="HS256")
            print(encoded)
            session.close()
            elapsed_time = time.time() - start



            session.close()

            return jsonify({
                        "status": 200,
                        "token": encoded,
                        "elapsedTime": elapsed_time
                    })
        
        session.close()
        
        return jsonify({
                "status": 400,
                "message": "failed to login"
                })
    except:
        return jsonify({
            "status": 400,
            "message": "正しいメールアドレスまたはパスワードを入力してください"
        })


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, threaded=True, debug=True)