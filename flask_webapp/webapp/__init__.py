import os
import datetime
import logging
from logging import FileHandler, Formatter
from flask import Flask
from webapp.database import db_session, init_db, create_all_table, create_all_test_table


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename, silent=True)

    # TODO logger 配置路徑有問題
    # app.logger.addHandler(create_log_file_handler(app.config.get('LOG_PATH')))
    init_db(app.config['SQLALCHEMY_DATABASE_URI'])

    if not app.config['DEBUG']:
        create_all_table()

    else:
        create_all_test_table()

    return app


def create_log_file_handler(log_path):
    last_slash_index = str.rfind(log_path, '/')
    log_folder = log_path[: last_slash_index]
    log_filename = log_path[last_slash_index + 1:]
    now_date = datetime.date.today()

    if not os.path.isdir(log_folder):
        os.makedirs(log_folder)

    file_handler = FileHandler(log_folder + '\\' +
                               log_filename + now_date.strftime('-%Y-%m-%d')
                               + '.log', mode='a', encoding=None, delay=False)

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))

    return file_handler

app = create_app('config_production.cfg')


@app.teardown_request
def shutdown_session(exception=None):
    if db_session:
        db_session.remove()

@app.route('/mobile/')
def index():
    return 'mobile'

from webapp.in_app_purchase import iap
app.register_blueprint(iap, url_prefix='/mobile')

from webapp.push_notification import notify
app.register_blueprint(notify, url_prefix='/mobile')