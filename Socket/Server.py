import socketserver
import threading

HOST = 'localhost'
PORT = 3000

Lock = threading.Lock()

class MyUserManager:
	Users = {}

	def __init__(self) -> None:
		pass

	def AddUser(self, Username, Connection, Address) -> bool:
		if Username in self.Users:
			Connection.send(f"이미 존재하는 닉네임입니다.")
			return False
		
		Lock.acquire()
		self.Users[Username] = (Connection, Address)
		Lock.release()

		self.sendMessageToAll(f"JOIN : {Username}")

		return True

	def RemoveUser(self, UserName) -> bool:
		if UserName not in self.Users:
			return False
		
		Lock.acquire()
		del self.Users[UserName]
		Lock.release()

		self.sendMessageToAll(f"QUIT : {UserName}")

		return True

	def MessageHandler(self, UserName, Message : str) -> bool:
		Message = Message.strip()
		if Message[0] == "/":
			Message = Message.strip().split(' ')
			if Message[0] == "/quit":
				self.RemoveUser(UserName)
				return False
			
			elif Message[0] == "/list":
				self.sendMessage(UserName, f"===== {len(self.Users)} 명 =====")
				i = 0
				for i, Name in enumerate(self.Users.keys()):
					self.sendMessage(UserName, f"{i}. {Name}\n")

			elif Message[0] == "/msg":
				try:
					print(Message[1], ''.join(Message[2:]))
					self.sendMessage(Message[1], f"[{UserName}] -> 당신 : {''.join(Message[2:])}")
				except:
					self.sendMessage(UserName, "잘못된 명령어 입니다!")

			elif Message[0] == "/help":
				self.sendMessage(UserName, "/quit : 종료하기\n")
				self.sendMessage(UserName, "/msg [닉네임] [메세지] : 메세지 보내기\n")
				self.sendMessage(UserName, "/quit : 종료하기\n")

			return True
		
		self.sendMessageToAll(f"[{UserName}] : {Message}", WithoutUser = UserName)
		return True

	def sendMessage(self, UserName, Message : str) -> bool:
		Connection = self.Users[UserName][0]
		Connection.send(Message.encode())
		return True

	def sendMessageToAll(self, Message : str, WithoutUser = "") -> bool:
		for Connection, Address in self.Users.values():
			if self.Users.get(WithoutUser) != (Connection,Address):
				Connection.send(Message.encode())
		return True

class MyTCPHandler(socketserver.BaseRequestHandler):
	UserManager = MyUserManager()

	def handle(self) -> None:
		print(f"JOIN : {self.client_address[0]}")

		try:
			UserName = self.Register()
			Message = self.request.recv(1024)

			while Message:
				print(f"[{UserName}] : {Message.decode()}")

				if self.UserManager.MessageHandler(UserName, Message.decode()) == False:
					self.request.close()
					break

				Message = self.request.recv(1024)

		except Exception as e:
			print(e)
			print(f"QUIT : {self.client_address[0]}")
			self.UserManager.RemoveUser(UserName)

	def Register(self):
		while True:
			self.request.send("ID : ".encode())
			MyUserName = self.request.recv(1024)
			MyUserName = MyUserName.decode().strip()
			if self.UserManager.AddUser(MyUserName, self.request, self.client_address):
				return MyUserName

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass



def Run():
	print("실행 중입니다. ctrl + c 로 종료")

	try:
		Server = ChatingServer((HOST, PORT), MyTCPHandler)
		Server.serve_forever()

	except KeyboardInterrupt:
		print("서버 종료")
		Server.shutdown()
		Server.server_close()

if __name__ == "__main__":
	Run()