from client import Client


client1 = Client()
client1.load_account('account2.txt')
print(client1.to_json())
