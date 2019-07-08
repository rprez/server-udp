import datetime

from sqlalchemy import Column, Integer, String,Sequence,TIMESTAMP

from .base import Base

class Alert(Base):
    __tablename__ = "notifications_alert"
    id = Column(Integer,Sequence('id_seq_alert'), primary_key=True)
    imei = Column('imei', String(32))
    ip = Column('ip', TIMESTAMP)
    fecha = Column('fecha', TIMESTAMP)
    alert = Column('alert', String(40))

    def __init__(self,imei,ip,fecha,alert) -> None:
        self.imei = imei
        self.ip = ip
        self.fecha = fecha
        self.alert = alert

    def __init__(self, message: dict) -> None:
        self.imei = message.get('imei')
        self.ip = message.get('ip')
        self.fecha = datetime.datetime.strptime(message.get('fecha'), '%y-%m-%d %H:%M:%S')
        self.alert = message.get('alert')
