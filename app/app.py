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
from werkzeug.exceptions import RequestURITooLarge
from flask_cors import CORS, cross_origin


from setting import session# セッション変数の取得
from user import *# Userモデルの取得

from user_registry import UserLogin, UserRegistry, WordService, ToeicService
from  get_meaning import GetMeaning
from jwt_auth import JwtAuth
from get_youtube_info import GetSubtittle, GetRelatedVideos
from get_sound import GetSoundOfEnglish
#from googleapiclient.discovery import build
#from apiclient.discovery import build

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
    '''app
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

@app.route("/get_subtittle", methods=["POST"])
@cross_origin(supports_credentials=True)
def get_subtittle():
    """
    {
        token: String,
        video_id: String
    }
    """
    subtittle = ""
    token_and_videoid = json.loads(request.get_data().decode())
    gs = GetSubtittle(token_and_videoid["video_id"])

    try:
        subtittle = gs.get_normal_subtittle()
    except:
        subtittle = gs.get_autogenerated_subtittle()
    
    return jsonify({
        "status": 200,
        "subtittle": subtittle
    })

@app.route("/get_related_videoid", methods=["POST"])
@cross_origin(supports_credentials=True)
def get_related_videoid():
    """
    {
        token: String,
        video_id
    }
    apikey = "AIzaSyB5ydOIa5tDNxvehwGnP7aLj_4e7CyyIBI"
    """
    token_and_videoid = json.loads(request.get_data().decode())
    ja = JwtAuth()
    decoded = ja.decode(token_and_videoid['token'])
    grv = GetRelatedVideos(token_and_videoid['video_id'], decoded['key'])

    
    video_and_url = grv.get_videoid_and_url()
    return jsonify({"status":200, "videoInfo": video_and_url})

@app.route("/word_registry", methods=["POST"])
@cross_origin(supports_credentials=True)
def word_registry():
    """
    {
        token: String,
        date: date,
        video_id: string,
        data:[
            {"eng": string, "jp": string}, 
        ]
    }
    """
    token_and_data = json.loads(request.get_data().decode())
    ja = JwtAuth()
    decoded = ja.decode(token_and_data['token'])
    ws = WordService(decoded['id'])
    result = ws.word_registry(token_and_data['video_id'], token_and_data['data'])

    if result:
        return jsonify({"status": 200, "message": "登録成功"})
    
    return jsonify({"status": 400, "message": "登録失敗"})
    
@app.route("/get_all_words", methods=["POST"])
@cross_origin(supports_credentials=True)
def get_all_words():
    """
    {
        token: String
    }
    """
    token = json.loads(request.get_data().decode())
    ja = JwtAuth()
    decoded = ja.decode(token['token'])
    ws = WordService(decoded['id'])
    #result = ws.get_all_words()
    result = ws.get_words_group_by_videoid()
    print(result)
    
    return jsonify({"status":200, "data":result})
    #return jsonify({"status": 200, "message": "取得成功", "data":result})


@app.route("/get_sounds", methods=["POST"])
@cross_origin(supports_credentials=True)
def get_sounds():
    """
    {
        token: String
        data:["apple", "lemon"]
    }
    """
    token_and_data = json.loads(request.get_data().decode())
    success_list, failure_list = GetSoundOfEnglish(token_and_data['data']).get_sound()

    return jsonify({
        "status": 200,
        "success": success_list,
        "failure": failure_list
    })

@app.route("/toeic_info_reg", methods=["POST"])
@cross_origin(supports_credentials=True)
def toeic_info_reg():
    """
    {
        token: String,
        score: Int,
    }
    """
    token_and_data = json.loads(request.get_data().decode())
    ja = JwtAuth()
    decoded = ja.decode(token_and_data['token'])
    toeic_info = ToeicService(decoded['id'], token_and_data['score'])
    level = toeic_info.get_score_level()
    result = toeic_info.score_reg(level)
    if result:
        return jsonify({"status":200, "message":"登録完了"})
    return jsonify({"status":400, "message":"登録失敗"})





if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, threaded=True, debug=True)