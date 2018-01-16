from node import Node


address2 = ("127.0.0.1", 8982)
server = ("127.0.0.1", 9919)
node2 = Node([server], address2)
node2.send_to("Hello", server)
