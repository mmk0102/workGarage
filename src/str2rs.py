
# pip install pyserial
import sys
import serial

ComPort = serial.Serial('COM3')
#ComPort = serial.Serial(0)
ComPort.baudrate = 2400
ComPort.bytesize = 8
ComPort.parity = 'N'
ComPort.stopbits = 1
args = sys.argv
z = len(args)
strB = bytearray.fromhex('FFA003010000')
strE = bytes.fromhex('000800B1FD')
strS = bytes.fromhex('20')

#Get texts from users files
#f = open('text1.txt', 'r', encoding="utf-8")
#s1 = f.read()
#f.close()

if z<2: #Clear all
	str = strB+strS+strE
	ComPort.write(str)
	strB[1] = 0xA1
	str = strB+strS+strE
	ComPort.write(str)
	strB[1] = 0xA2
	str = strB+strS+strE
	ComPort.write(str)
	strB[1] = 0xA3
	str = strB+strS+strE
	ComPort.write(str)
	print("must clear ")	
	ComPort.close()        # close port
	quit()
elif z < 4: #Clear string
	n = int(args[1])
	n = n-1
	if n>3: 
		n = 3
	strB[1] = 0xA0 + n
	str = strB+strS+strE
	ComPort.write(str)
	ComPort.close()        # close port
else:
	#string num
	n = int(args[1])
	n = n-1
	if n>3: 
		n = 3
	strB[1] = 0xA0 + n
	#color
	n = int(args[2])
	if n>7: 
		n = 7
	strB[3] =  n

str=strB
for i in args[3:]:
    str=str + i.encode('cp1251') + strS

#str = str + s1.encode('cp1251') 

str=str+strE
#print("must print ")
print(str)

ComPort.write(str)   # write a string

ComPort.close()        # close port


# print("len="+str(len(args)) )