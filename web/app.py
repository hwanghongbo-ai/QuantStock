# coding=utf-8
from flask import Flask

from controller.test import test
from controller.ApiTradeData import stock
from controller.ApiStatData import stat

app = Flask(__name__)
app.register_blueprint(test, url_prefix='/test')
app.register_blueprint(stock,url_prefix='/data')
app.register_blueprint(stat,url_prefix='/stat')


# HOST = '127.0.0.1'
PORT = 7002
DEBUG = True


@app.route('/')
def whoami():  # put application's code here
    return 'This is stock data platform by HHB!'


if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG)
