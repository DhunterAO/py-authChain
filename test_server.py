from node import Node


server_address = ("127.0.0.1", 9919)
server = Node([], server_address)
server.start()
