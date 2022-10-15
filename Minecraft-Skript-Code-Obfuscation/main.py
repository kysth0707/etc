from tkinter.filedialog import *
import os
import random

FilePos = askopenfilename(initialdir = os.getcwd(), title = "스크립트 선택", filetypes = (("스크립트 파일", "*.sk"), ("모든 파일", "*.*")))
print(FilePos)


OptionNameList = ["option:", "options:", "Option:", "Options:"]
OptionName = ""
OptionNameRow = 0
OptionEndRow = 0

Alphabets = "abcdefghijklmnopqrstuvwxyz"
Data = None

HeaderList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
HeaderList = list(HeaderList)

def Choose(x):
	return random.choice(HeaderList) + x


with open(FilePos, encoding = 'utf-8') as f:
	Data = f.readlines()

	# Option 찾기
	for RowNum, Row in enumerate(Data):
		print(Row, end="")
		for i in range(4):
			if OptionNameList[i] in Row:
				OptionNameRow = RowNum
				OptionName = OptionNameList[i]
				break
	
	# Option 추가
	if OptionName == "":
		OptionNameRow = 0
		Data.insert(OptionNameRow, "Options:\n")
	
	for y in range(0, 1000):
		try:
			if Data[y + OptionNameRow + 1][0] == "\t":
				pass
			else:
				OptionEndRow = y + OptionNameRow
				break
		except:
			OptionEndRow = y + OptionNameRow
			break
	
	#코드 변환
	for i, Row in enumerate(Data):
		if OptionNameRow > i or i > OptionEndRow:
			Output = ""
			if Row[0] == "\t":
				for x in Row:
					if x in Alphabets:
						Output += f"{{@{Choose(x)}}}"
					else:
						Output += x
				Data[i] = Output


	#알파벳 옵션추가
	for header in HeaderList:
		for alpha in Alphabets:
			Data.insert(OptionEndRow + 1, f"\t{header}{alpha} : {alpha}\n")
	
with open(FilePos, encoding = 'utf-8', mode="w") as f:
	for Row in Data:
		f.write(Row)
	f.close()
