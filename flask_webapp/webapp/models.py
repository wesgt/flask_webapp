from sqlalchemy import Column, Integer, String
from webapp.database import Base, db_session


class DeviceToken(Base):
    __tablename__ = 'device_token'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True)
    token = Column(String(50))

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def __repr__(self):
        return '<DeviceToken user_id {0}>'.format(self.user_id)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()
