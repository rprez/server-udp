import json
import threading
from datetime import datetime
import time
import os
import shutil
from NotificationDBStorageAlchemy import  NotificationDatabase

def parseDate(dir):
    
    pedazos=dir.split("-")
    if len(pedazos)==3:
        try:
            y=int(pedazos[0])
            m=int(pedazos[1])
            d=int(pedazos[2])
                        
            return datetime(year=y,month=m,day=d)
        except Exception as e:
            return None
    
    return None

def borrarHistorialViejo(diasConservados):
    
    fechaHoy=datetime.now()
    dirs=os.listdir("./history")
    for d in dirs:
        fechaDir=parseDate(d)
        if fechaDir!=None:
            if (fechaHoy - fechaDir).days > diasConservados:
                print("es necesario borrar directorio %s"%(d))
                try:
                    shutil.rmtree("./history/"+d)
                    print("directorio %s borrado"%(d))
                except Exception as e:
                    print (e)
                    print("directorio %s no se puedo borrar"%(d))

def getFolder(msg):
    
    return msg['fecha'].split(" ")[0]


def saveNoticationToDiskTest(msg):
    subFolderDay = getFolder(msg)                      
    if not os.path.exists("history/" + subFolderDay):
        os.makedirs("history/" + subFolderDay)
         
    if "ip" in msg:
        
        msgString = json.dumps(msg, indent=0, sort_keys=False)
        iptext = msg["ip"]
        iptext = iptext.replace(".", "_")
        fname = "history/" + subFolderDay + "/" + iptext + datetime.now().strftime('_%Y-%m-%d-%H-%M-%S-%f') + ".json"
                       
        saveStringToFile(fname, msgString)


def saveNoticationToDisk(msg):
    subFolderDay = datetime.now().strftime('%Y-%m-%d')                            
    if not os.path.exists("history/" + subFolderDay):
        os.makedirs("history/" + subFolderDay)
         
    if "ip" in msg:
        
        msgString = json.dumps(msg, indent=0, sort_keys=False)
        iptext = msg["ip"]
        iptext = iptext.replace(".", "_")
        fname = "history/" + subFolderDay + "/" + iptext + datetime.now().strftime('_%Y-%m-%d-%H-%M-%S-%f') + ".json"
                       
        saveStringToFile(fname, msgString)


def saveStringToFile(fname, msgEnString):
    
    archivo = open(fname, "w+")        
    archivo.write(msgEnString)                       
    archivo.close()   

class HistoryCleaner (threading.Thread):
    
    def __init__(self,diasConservados):
                threading.Thread.__init__(self)
                
                self.diasConservados = diasConservados         
    
    def run(self):     
    
        while True:            
            borrarHistorialViejo(self.diasConservados)
            time.sleep(60)

        
class StorageDbHandler (threading.Thread):
    
    def __init__(self,dbConfig,sq,sqlock):
                threading.Thread.__init__(self)
                
                self.dbConfig=dbConfig
                self.sq=sq
                self.sqlock=sqlock
                self.tableName="notifications"
                #self.diasConservados = diasConservados         
    
    def run(self):

        while True:
            toSave = []
            self.sqlock.acquire()
            while not self.sq.empty():
                toSave.append(self.sq.get())
            self.sqlock.release()

            if len(toSave) > 0:
                NotificationDatabase.storeNotification(toSave)
            time.sleep(1)



class SocketHandler_NotificationDistributor (threading.Thread):
    
    def __init__(self, udpQueue, udpLock,sq,sqlock,storageMode):
                threading.Thread.__init__(self)
                
                self.udpQueue = udpQueue
                self.udpLock = udpLock    
                
                self.sq=sq
                self.sqlock=sqlock 
                self.storageMode=storageMode
    

    def run(self):     
    
        while True:            

            # distribute new Messages
            if not self.udpQueue.empty():
                msgs = []
                self.udpLock.acquire()
                while not self.udpQueue.empty():
                    msgs.append(self.udpQueue.get())
                self.udpLock.release()
                
                for m in msgs:
                    if self.storageMode=="db":
                        self.sqlock.acquire()
                        self.sq.put(m)
                        self.sqlock.release()
                    elif self.storageMode=="file":
                        saveNoticationToDiskTest(m)
            else:
                time.sleep(1)
       

