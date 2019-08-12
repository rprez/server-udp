import queue
import threading
import os
import sys
import json

from utenotificationserver import StorageDbHandler
from utenotificationserver import SocketHandler_NotificationDistributor
from uteUdpNotificationReceiver import UteUdpReceiver

if __name__ == "__main__":
    udpPort = 12345

    if not os.path.exists("history"):
        os.makedirs("history")

    storageMode = "db"
    if len(sys.argv) == 2:
        if sys.argv[1] == "-filedb":
            storageMode = "file"

    storageQueue = queue.Queue()
    storageQueueLock = threading.Lock()
    config = {}
    dbHandler = None

    if storageMode == "db":
        try:
            config = json.load(open("udpserverconfig.json"))

        except Exception as e:
            print("Error al cargar configuracion")
            print(e)
            exit(0)

        try:
            dbHandler = StorageDbHandler(
                config, storageQueue, storageQueueLock)
            dbHandler.setDaemon(True)
            dbHandler.start()
        except Exception as e:
            print("Error al conectar con base de datos")
            print(e)
            exit(0)

    # notification receiver
    udpQueue = queue.Queue()
    udpLock = threading.Lock()
    udpReceiver = UteUdpReceiver(udpPort, udpQueue, udpLock)
    udpReceiver.setDaemon(True)
    udpReceiver.start()

    resender = SocketHandler_NotificationDistributor(udpQueue, udpLock, storageQueue, storageQueueLock, storageMode)
    resender.setDaemon(True)
    resender.start()

    while True:
        newLock = []
