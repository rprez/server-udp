from database.base import Session, engine
from database.alert import  Alert
from database.notification import Notification

class NotificationDatabase:

    @staticmethod
    def storeNotification(notis):

        # create a new session
        session = Session()
        print(notis)
        notis = [Alert(x) if "alert" in x else Notification(x) for x in notis]

        for newMessage in notis:
            session.add(newMessage)
            session.commit()
        session.close()

    @staticmethod
    def store(notis):

        #create a new session
        session = Session()

        newMessage = Alert(notis) if "alert" in notis else Notification(notis)


        session.add(newMessage)
        session.commit()
        session.close()