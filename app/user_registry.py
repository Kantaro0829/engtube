#from _typeshed import Self
from sqlalchemy.engine import engine_from_config
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import user
from setting import session# セッション変数の取得
from user import *# Userモデルの取得
import hashlib#ハッシュ化用
import datetime

class UserRegistry():

    def __init__(self, user_info):
        self.password = hashlib.sha256(user_info['password'].encode()).hexdigest()
        self.mail = user_info["email"]
        self.api_key = user_info["api_key"]
        self.dic = {}

    def new_user_reg(self):
        user = User()
        user.mail = self.mail
        user.api_key = self.api_key
        user.password = self.password
        dic = {}

        session.add(user)#データ登録
        session.flush()
        session.commit()#コミット

        #自動で生成されたID
        id = user.id
        key = user.api_key
        session.close

        self.dic = {"id": id, "key":key}
        return self.dic
    
    def update_user(self):
        pass

class UserLogin():
    def __init__(self, user_info):
        self.password = hashlib.sha256(user_info['password'].encode()).hexdigest()
        self.mail = user_info['email']
        self.dic = {}
    
    def login(self):
        user = User()

        #このメールアドレスのパスワードを抽出
        auth_pass = session.query(User.password).\
            filter(User.mail == self.mail).\
                one()

        print(auth_pass[0], "は", self.mail, "のパスワード！！")

        #パスワード比較
        if self.password == auth_pass[0]:
            
            id = session.query(User.id).\
                    filter(User.mail == self.mail).\
                        one()
            
            key = session.query(User.api_key).\
                    filter(User.id == id[0]).\
                        one()

            print("id: ", id[0])
            print("apiKey: ", key[0])

            self.dic = {"id": id[0], "key": key[0]}

            session.close

            return self.dic
        
        else:
            self.dic = {"id": 0}
            return self.dic

class WordService():
    def __init__(self, id):
        self.id = id
        self.watched_day = datetime.date.today()
    
    def word_registry(self, video_id, eng_and_jp):

        count = len(eng_and_jp)# 登録したい単語の数
        for i in eng_and_jp:
            words = Words()
            words.id = self.id
            words.video_id = video_id
            words.day = self.watched_day
            words.english = i['eng']
            words.japanese = i['jp']

            session.add(words)#データ登録
            session.flush()

            count = count - 1
        session.commit()#コミット

        if count == 0:
            return true
        
        return false
    
    def get_all_words(self):
        words = Words()

        all_eng_and_jp = session.query(Words.english, Words.japanese).\
            filter(Words.id == self.id).\
                all()

        print(all_eng_and_jp)
        print("userId === ", self.id)

        session.close()
        data_list = []
        for i in all_eng_and_jp:
            word_dic = {}
            word_dic['eng'] = i[0]
            word_dic['jp'] = i[1]
            data_list.append(word_dic)

        print("送るListの中身：", data_list)

        return data_list
    
    def tuple_to_dict(self, list):
        data_list = []
        for i in list:
            word_dic = {}
            word_dic['eng'] = i[0]
            word_dic['jp'] = i[1]
            data_list.append(word_dic)
        
        return data_list
    
    def get_words_group_by_videoid(self):
        words = Words()

        all_video_id = session.query(Words.video_id).\
            filter(Words.id == self.id).\
                group_by(Words.video_id).\
                        all()
        
        print(all_video_id)
        
        data_list = []

        for id in all_video_id:
            eng_and_jp_list = session.query(Words.english, Words.japanese).\
                filter(Words.id == self.id, Words.video_id == id[0]).\
                    all()
            
            data_list.append(self.tuple_to_dict(eng_and_jp_list))
            
        print(data_list)

        return data_list

class ToeicService():
    def __init__(self, id, score):
        self.id = id
        self.score = score

    def get_score_level(self):
        
        if self.score > 800:
            return 8
        elif self.score > 700:
            return 7
        elif self.score > 600:
            return 6
        elif self.score > 500:
            return 5
        else:
            return 4
    
    def score_reg(self, level):
        tf = Toeic_info()
        tf.id = self.id
        tf.score = self.score
        tf.level = level

        session.add(tf)
        session.flush()
        session.commit()
        print("登録完了")
        print("id=", tf.id, "score=", tf.score, "level=", tf.level)
        session.close()

        return true
        
