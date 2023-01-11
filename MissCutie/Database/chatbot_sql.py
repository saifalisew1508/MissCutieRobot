import threading
from sqlalchemy import Column, String
from MissCutie.Database import BASE, SESSION
class MissCutieChats(BASE):
    __tablename__ = "misscutie_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

MissCutieChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_misscutie(chat_id):
    try:
        chat = SESSION.query(MissCutieChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()

def set_misscutie(chat_id):
    with INSERTION_LOCK:
        misscutiechat = SESSION.query(MissCutieChats).get(str(chat_id))
        if not misscutiechat:
            misscutiechat = MissCutieChats(str(chat_id))
        SESSION.add(misscutiechat)
        SESSION.commit()

def rem_misscutie(chat_id):
    with INSERTION_LOCK:
        misscutiechat = SESSION.query(MissCutieChats).get(str(chat_id))
        if misscutiechat:
            SESSION.delete(misscutiechat)
        SESSION.commit()


def get_all_misscutie_chats():
    try:
        return SESSION.query(MissCutieChats.chat_id).all()
    finally:
        SESSION.close()
