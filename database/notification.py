import datetime

from sqlalchemy import Column, Integer, String,BigInteger,Sequence,TIMESTAMP,DECIMAL

from .base import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer,Sequence('id_seq_notif'), primary_key=True)
    imei = Column('imei', BigInteger)
    ip = Column('ip', String(15))
    fecha = Column('fecha', TIMESTAMP)
    ecno = Column('ecno', Integer)
    rssi = Column('rssi', String(10))
    cellid = Column('cellid', Integer)
    log_size = Column('logsize', Integer)
    temp = Column('temp', DECIMAL)
    uptime = Column('uptime', Integer)

    def __init__(self,imei,ip,fecha,ecno,rssi,cellid,log_size,temp,uptime) -> None:
        self.imei = imei
        self.ip = ip
        self.fecha = fecha
        self.ecno = ecno
        self.rssi = rssi
        self.cellid = cellid
        self.log_size = log_size
        self.temp = temp
        self.uptime = uptime

    def __init__(self,message : dict) -> None:
        self.imei = message.get('imei')
        self.ip = message.get('ip')
        self.fecha = datetime.datetime.strptime(message.get('fecha'), '%y-%m-%d %H:%M:%S')
        self.ecno = message.get('EC/NO')
        self.rssi = message.get('rssi')
        self.cellid = message.get('cellid')
        self.log_size = message.get('logSize')
        self.temp = message.get('temp')
        self.uptime = message.get('uptime')