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

        notis = [Alert(x) if "alert" in x else Notification(x) for x in notis]

        for newMessage in notis:
            session.add(newMessage)
            session.commit()
        session.close()
