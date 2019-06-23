import os
import tgalice
import mongomock
from pymongo import MongoClient




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

    manager = tgalice.dialog_manager.CascadeDialogManager(
        tgalice.dialog_manager.FAQDialogManager('faq.yaml', matcher='cosine'),
        tgalice.dialog_manager.GreetAndHelpDialogManager(
            greeting_message=TEXT_HELP,
            help_message=TEXT_HELP,
            default_message='Я вас не понимаю.',
            exit_message='Всего доброго! Было приятно с вами пообщаться!'
        )
    )
    connector = tgalice.dialog_connector.DialogConnector(
        dialog_manager=manager,
        storage=tgalice.session_storage.MongoBasedStorage(mongo_db, collection_name='sessions'),
    )
    server = tgalice.flask_server.FlaskServer(connector=connector, collection_for_logs=mongo_logs)
    server.parse_args_and_run()
