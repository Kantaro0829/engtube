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

from user_registry import UserLogin, UserRegistry
from  get_meaning import GetMeaning
from jwt_auth import JwtAuth

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=['GET'])
@cross_origin(supports_credentials=True)
def index():
    ur = UserRegistry("password", "mail.com", "key")
    dic_temp = ur.new_user_reg()
    print(dic_temp)
    return jsonify(dic_temp)

@app.route("/new_user_reg", methods=["POST"])
@cross_origin(supports_credentials=True)
def new_user_reg():
    '''
    受け取るJSON : user_info[]
    {
        "password": String,
        "email": String,
        "api_key": String
    }

    '''
    start = time.time()#計測開始
    user_info = json.loads(request.get_data().decode())
    print(user_info)

    #user table にレコードの追加
    try:
        ur = UserRegistry(user_info)
        dic_temp = ur.new_user_reg()
        jwt_auth = JwtAuth()
        #token生成
        token = jwt_auth.encode(dic_temp)
        temp = {
            "status": 200,
            "token": token
        }

        return jsonify(temp)
        
    except exc.SQLAlchemyError as e:
        message = None
        if type(e) is exc.IntegrityError:
            message = "メールアドレスがすでに登録されています"
            print(type(e))
            return jsonify({
                "status": 400,
                "message": message,
        })
        return jsonify({"status":400, "massage":"DBに問題あるかも"})

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
    user_info = json.loads(request.get_data().decode())
    try:
        ul = UserLogin(user_info)
        id_and_apikey = ul.login()

        if id_and_apikey['id'] != 0:
            jwt_auth = JwtAuth()
            token = jwt_auth.encode(id_and_apikey)

            return jsonify({"status":200, "token":token})

        return jsonify({
            "status": 400,
            "message": "正しいメールアドレスまたはパスワードを入力してください"
        })
    except:
        return jsonify({
            "status": 400,
            "message": "db のエラー？"
        })

@app.route("/get_meaning", methods=["POST"])
@cross_origin(supports_credentials=True)
def get_meaning():
    """
    受け取るJson
    {
        token: String,
        data: [apple, lemon]
    }
    """
    token_and_data = json.loads(request.get_data().decode())
    gm = GetMeaning(token_and_data['data'])

    result_list, failure_list = gm.scrape_from_weblio()
    return jsonify({
        "status": 200,
        "data": result_list,
        "failure": failure_list
    })



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, threaded=True, debug=True)