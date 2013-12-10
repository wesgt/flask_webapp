import datetime
from sqlalchemy import Column, Integer, String, DateTime, UnicodeText
from webapp.database import Base, db_session


class DeviceToken(Base):
    __tablename__ = 'device_token'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    game_id = Column(String(50))
    token = Column(String(64))
    register_date = Column(DateTime)

    def __init__(self, user_id, game_id, token,
                 register_date=datetime.datetime.today()):
        self.user_id = user_id
        self.game_id = game_id
        self.token = token
        self.register_date = register_date

    def __repr__(self):
        return '<DeviceToken user_id {0}>'.format(self.user_id)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class IAPVerifyData(Base):
    __tablename__ = 'iap_verify_data'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    receipt_data = Column(UnicodeText())
    verify_date = Column(DateTime)

    def __init__(self, user_id, receipt_data,
                 verify_date=datetime.datetime.today()):
        self.user_id = user_id
        self.receipt_data = receipt_data
        self.verify_date = verify_date

    def __repr__(self):
        return '<IAPVerifyData user_id {0}>'.format(self.user_id)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()
