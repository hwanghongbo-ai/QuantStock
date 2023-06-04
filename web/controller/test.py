from flask import Blueprint
import logging

logger = logging.getLogger(__name__)
test = Blueprint('test',__name__)

@test.route('/test')
def testfun():  # put application's code here
    return 'test hhb!'


