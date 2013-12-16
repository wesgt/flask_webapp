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
    bid = Column(String(50))
    transaction_id = Column(String(50), unique=True)
    udid = Column(String(50))
    product_id = Column(String(50))
    purchase_date = Column(String(50))
    quantity = Column(String(20))
    #receipt_data = Column(UnicodeText())
    verify_date = Column(DateTime)

    def __init__(self):
        pass

    def __repr__(self):
        return '<IAPVerifyData user_id {0}>'.format(self.user_id)

    @staticmethod
    def create_for_ios6(udid, verify_data,
                        verify_date=datetime.datetime.today()):
        iap_verify_data = IAPVerifyData()
        iap_verify_data.bid = verify_data.get('bid')
        iap_verify_data.transaction_id = verify_data.get('transaction_id')
        iap_verify_data.udid = udid
        iap_verify_data.product_id = verify_data.get('product_id')
        iap_verify_data.purchase_date = verify_data.get('purchase_date')
        iap_verify_data.quantity = verify_data.get('quantity')
        iap_verify_data.verify_date = verify_date

        return iap_verify_data

    @staticmethod
    def create_for_ios7(udid, bundle_id, in_app_data,
                        verify_date=datetime.datetime.today()):
        iap_verify_data = IAPVerifyData()
        iap_verify_data.bid = bundle_id
        iap_verify_data.transaction_id = in_app_data.get('transaction_id')
        iap_verify_data.udid = udid
        iap_verify_data.product_id = in_app_data.get('product_id')
        iap_verify_data.purchase_date = in_app_data.get('purchase_date')
        iap_verify_data.quantity = in_app_data.get('quantity')
        iap_verify_data.verify_date = verify_date

        return iap_verify_data

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()
