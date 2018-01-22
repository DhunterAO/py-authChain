from client import Client
from account import Account


client1 = Client()
client1.load_account('account1.txt')
client1.create_address()
print(client1.to_json())
