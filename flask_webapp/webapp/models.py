import datetime
from sqlalchemy import Column, Integer, String, DateTime
from webapp.database import Base, db_session


class DeviceToken(Base):
    __tablename__ = 'device_token'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    game_id = Column(String(50))
    token = Column(String(50))
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
