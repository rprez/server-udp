from database.base import Session, engine, Base
from database.alert import  Alert
from database.notification import Notification

class NotificationDatabase:

    @staticmethod
    def storeNotification(notis):

        # 2 - generate database schema
        Base.metadata.create_all(engine)

        # 3 - create a new session
        session = Session()

        for noti in notis:
            if "alert" in noti:
                newMessage = Alert(noti)
                #self.insertAlert(tableName+"_alert", noti)
            else:
                newMessage = Notification(noti)
                #self.insertNotification(tableName, noti)
            session.add(newMessage)
            session.commit()
        session.close()
