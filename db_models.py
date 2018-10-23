from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db_handler import base
from hashlib import md5
import time
from datetime import datetime

class User(base):
    __tablename__='Users'

    id=Column(Integer, primary_key=True)
    name=Column(String(40), index=True, unique=True)
    passwd=Column(String(30))
    key=Column(String(128))
    messages=relationship('Message', backref='author', lazy='dynamic')

    def set_passwd(self, passwd):
        self.passwd=md5(str(passwd).encode()).hexdigest()

    def check_passwd(self, passwd):
        return self.passwd==md5(str(passwd).encode()).hexdigest()
    
    def set_key(self):
        pre_key=self.passwd+str(time.time())
        self.key=md5(pre_key.encode()).hexdigest()

    def __repr__():
        return '<User {}>'.format(self.name)

class Message(base):
    __tablename__='Messages'

    id=Column(Integer, primary_key=True)
    text=Column(String(300))
    user_id=Column(Integer, ForeignKey('user.id'))
    timestamp=Column(DateTime, index=True, default=datetime.utcnow())

   def  __repr__():
       return '<Message: {}>'.format(self.text)
