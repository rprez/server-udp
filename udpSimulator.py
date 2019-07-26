import json
import socket
import threading
import datetime
import time
import random
import sys


class UteUdpSimulator(threading.Thread):
    
    def __init__(self,host,port,count_notification,count_alert,interval):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.host=host
        self.port=port
        self.interval=interval
        
        self.count_notification = count_notification
        self.count_alert = count_alert
        self.logSize=0
        self.temp=25
        self.uptime=0
    
        
    def gen_timestamp(self):
        # gera um datetime no formato yyyy-mm-dd hh:mm:ss.000000
        year = 2018
        month = random.randint(11, 12)
        day = random.randint(1, 28)
        hour = random.randint(1, 23)
        minute = random.randint(1, 59)
        second = random.randint(1, 59)
        microsecond = random.randint(1, 999999)
        date = datetime.datetime(
            year, month, day, hour, minute, second, microsecond)
        return date
    

    def randomImei(self):
        return random.randrange(100000000000000,999999999999999)

    def createRandomAlert(self):
        
        """
        { "imei":359486064904103 ,"ip":"192.168.210.18","fecha": "19-5-17 8:56:8","alert":"lastgasp sent"}
       
           { "imei":359486064904103 ,"ip":"192.168.210.18","fecha": "19-5-17 8:56:8","alert":"lastgasp sent"}
      
          { "imei":359486064903246 ,"ip":"192.168.210.16","fecha": "19-5-17 10:30:29","alert":"lastgasp sent"}
        """
        
        packet={}
        
        packet['imei']=self.randomImei()
        packet['ip']="192.168.210.18"
        packet['fecha']=datetime.datetime.now().__format__("%y-%m-%d %H:%M:%S")
        packet['alert']="lastgasp sent"
        
        return packet
    def createNewRandomPacket(self):
       
        dbm=random.randint(1,100)
        self.logSize+= random.randint(1,100)
        self.uptime+=self.interval
        packet={}
        
        packet['imei']=self.randomImei()
        packet['rssi']=" -88 dmb"
        packet['ip']=str(random.randint(1,255))+"."+str(random.randint(1,255))+"."+str(random.randint(1,255))+"."+str(random.randint(1,255))
        packet['fecha']=datetime.datetime.now().__format__("%y-%m-%d %H:%M:%S")
    
        packet['rssi']="-%d dbm"%(dbm)
        packet['EC/NO']=32
        packet['cellid']=str(random.randint(100,20000))
        packet['logSize']=self.logSize
        packet['temp']=self.temp + random.randint(1,50)/10
        packet['uptime']=self.uptime
        
        return packet
        
    def run(self):
        messages_notification = [self.createNewRandomPacket() for _ in range(self.count_notification)]
        messages_alert = [self.createRandomAlert() for _ in range(self.count_alert)]

        for m in messages_notification + messages_alert:
            self.sock.sendto(json.dumps(m,indent=0, sort_keys=True).encode(), (self.host, self.port))
            time.sleep(self.interval)
        print(f"Alertas {self.count_alert} Errores: {self.count_notification}")
           
           
print(sys.argv)
if len(sys.argv) == 6:

    simu = UteUdpSimulator(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5]))
    simu.start()
else:
    print("usage: <ip> <port> <count_notification> <count_alert> <interval>")
       