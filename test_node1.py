
import flask


test = flask.Flask(__name__)


@test.route('/')
def hello_world():
    return 'Hello, I\'m node1!'


@test.route('/node2')
def get():
    return


test.run(host='127.0.0.1', port=9293)