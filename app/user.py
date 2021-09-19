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
    __tablename__ = 'user'
    id = Column('user_id', Integer, primary_key=True)
    name = Column('user_name', String(200))
    password = Column('password', String(255))
    mail = Column('mail', String(200), unique=True)

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)