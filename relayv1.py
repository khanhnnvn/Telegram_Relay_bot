from flask import Flask, request, jsonify, abort
import telegram
import redis
import datetime
import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

app = Flask(__name__)
bot = telegram.Bot(token='573653147:AAGK7lM9NG1AW4mFE9Gngj2PKvw_PArITPc')

# Redis zone
redis_db = redis.StrictRedis(host="localhost", port=6379, db=4, password="pass321*")
granted_ip = ""


def read_trusted_ip():
    with open("trusted_ip", "r") as trusted_ip:
        return trusted_ip.readlines()


#@app.before_request
def limit_remote_addr():
    trusted_ips = read_trusted_ip()
    flag = False
    for ip in trusted_ips:
        if request.remote_addr == ip:
            flag = True
            granted_ip = request.remote_addr

    if not flag:
        abort(403)


@app.route('/sendMsg', methods=["POST"])
def send_message():
    chat_id = request.json['chat_id']
    sms = request.json['sms']
    # Save in redis
    redis_db.mset(datetime=datetime.datetime.now(), ip=granted_ip, message=sms)

    bot.send_message(chat_id, sms)
    logger.info('info message')
    return "Done"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, use_reloader=True)