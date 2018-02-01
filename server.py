from constant import SERVER_ADDRESS
from node import Node


class Server:
    def __init__(self, port=9000):
        self._node = Node(port=port)
        self._node.add_address(SERVER_ADDRESS)

    def start(self):
        self._node.start()


if __name__ == '__main__':
    test_server = Server(port=9000)
    test_server.start()
