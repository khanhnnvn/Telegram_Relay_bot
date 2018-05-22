import datetime
import logging
import os

import redis
import telegram
from flask import Flask, request, abort

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


app = Flask(__name__)

token = os.environ.get(
    'TELEGRAM_TOKEN',
    '573653147:AAGK7lM9NG1AW4mFE9Gngj2PKvw_PArITPc'
)
bot = telegram.Bot(token)

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
try:
    REDIS_PORT = int(os.environ.get('REDIS_PORT'))
except ValueError:
    REDIS_PORT = 6379

try:
    REDIS_DB = int(os.environ.get('REDIS_DB'))
except ValueError:
    REDIS_DB = 4

REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

# Redis zone
redis_db = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD
)

TRUSTED_IP_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'trusted_ip'
)


GRANTED_IPS = []
with open(TRUSTED_IP_FILE, "r") as f:
    for line in f:
        GRANTED_IPS.append(line.rstrip())


@app.before_request
def limit_remote_addr():
    if request.remote_addr not in GRANTED_IPS:
        abort(403)


@app.route('/sendMsg', methods=["POST"])
def send_message():
    chat_id = request.json['chat_id']
    sms = request.json['sms']
    # Save in redis
    redis_db.mset(
        datetime=datetime.datetime.now(),
        ip=request.remote_addr,
        message=sms
    )

    bot.send_message(chat_id, sms)

    return "Done"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, use_reloader=True)
