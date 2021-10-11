import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.sql.expression import true
from setting import Base
from setting import ENGINE



class User(Base):
    """
    user テーブル用
    """
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True)
    password = Column('password', String(255))
    mail = Column('email', String(200), unique=True)
    api_key = Column('youtube_api_key', String(255))
    last_watched_video_id = Column('last_watched_video_id', String(30))

class Toeic_info(Base):
    """
    toeic_info テーブル
    """
    __tablename__ = 'toeic_info'
    id = Column('user_id', Integer, primary_key=True)
    score = Column('toeic_score', Integer)
    level = Column('toeic_level', Integer)

class Words(Base):
    """
    words テーブル
    """
    __tablename__ = 'words'
    id = Column('user_id', Integer, primary_key=True)
    video_id = Column('video_id', String(30))
    english = Column('english', String(30))
    japanese = Column('japanese', String(200))
    day = Column('watched_day', Date)




def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)