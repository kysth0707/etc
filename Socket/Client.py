import socket
from threading import Thread

HOST = 'localhost'
PORT = 3000

def ReceiveMessage(Socket):
	while True:
		try:
			Message = Socket.recv(1024)
			if not Message:
				break
			print(Message.decode())
		except:
			pass


def Run():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Socket:
		Socket.connect((HOST,PORT))
		
		Temp=Thread(target=ReceiveMessage, args=(Socket,))
		Temp.daemon=True
		Temp.start()

		UserName = None

		while True:
			if UserName == None:
				Message=input()
				UserName = Message.strip()
			else:
				Message=input(f"[{UserName}] : ")

			if Message=="/quit":
				Socket.send(Message.encode())
				break
			Socket.send(Message.encode())

if __name__ == "__main__":
	Run()