import os
import tgalice
import mongomock
from pymongo import MongoClient

from navec import Navec

import logging

logging.basicConfig(level=logging.INFO)

TEXT_HELP = (
    'Привет! Я бот, который умеет работать и в Телеграме и в Алисе.'
    '\nЯ не умею делать примерно ничего, но могу с вами поздороваться.'
    '\nКогда вам надоест со мной говорить, скажите "выход".'
)
TEXT_FAREWELL = 'Всего доброго! Если захотите повторить, скажите "Алиса, включи навык тест tgalice".'


if __name__ == '__main__':
    mongo_url = os.environ.get('MONGODB_URI')
    if mongo_url:
        mongo_client = MongoClient(mongo_url)
        mongo_db = mongo_client.get_default_database()
    else:
        mongo_client = mongomock.MongoClient()
        mongo_db = mongo_client.db
    mongo_logs = mongo_db.get_collection('message_logs')

    w2v = Navec.load('navec_hudlit_v1_12B_500K_300d_100q.tar')

    manager = tgalice.dialog_manager.CascadeDialogManager(
        tgalice.dialog_manager.FAQDialogManager('faq.yaml', matcher=tgalice.nlu.matchers.W2VMatcher(w2v=w2v)),
        tgalice.dialog_manager.GreetAndHelpDialogManager(
            greeting_message=TEXT_HELP,
            help_message=TEXT_HELP,
            default_message='Я вас не понимаю.',
            exit_message='Всего доброго! Было приятно с вами пообщаться!'
        )
    )
    connector = tgalice.dialog_connector.DialogConnector(
        dialog_manager=manager,
        storage=tgalice.session_storage.MongoBasedStorage(database=mongo_db, collection_name='sessions'),
        log_storage=tgalice.storage.message_logging.MongoMessageLogger(database=mongo_db, detect_pings=True)
        # log_storage=tgalice.storage.message_logging.BaseMessageLogger()
    )
    server = tgalice.flask_server.FlaskServer(connector=connector)
    server.parse_args_and_run()
