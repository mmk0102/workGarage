import sys
import serial
import time

from textwrap import wrap

justPrint = False #use without com port, just print, for debug

strWelcome1 = "Privet"
strWelcome2 = "Privet"
strWelcome3 = "Privet"
if not justPrint:
    ComPort = serial.Serial('COM3')
    ComPort.baudrate = 2400
    ComPort.bytesize = 8
    ComPort.parity = 'N'
    ComPort.stopbits = 1

# Choose string on TAB (1-4)
strB1 = bytearray.fromhex('FFA003010000') # addr, shrift, color, x, y
strB2 = bytearray.fromhex('FFA103010000')
strB3 = bytearray.fromhex('FFA203010000')
strB4 = bytearray.fromhex('FFA303010000')

listStrB = [strB1,strB2,strB3,strB4]

# Choose string on TAB (1-8)
strC1 = bytearray.fromhex('FFA00101000A')
strC2 = bytearray.fromhex('FFA001010000')
strC3 = bytearray.fromhex('FFA10101000A')
strC4 = bytearray.fromhex('FFA101010000')
strC5 = bytearray.fromhex('FFA20101000A')
strC6 = bytearray.fromhex('FFA201010000')
strC7 = bytearray.fromhex('FFA30101000A')
strC8 = bytearray.fromhex('FFA301010000')

listStrC = [strC1,strC2,strC3,strC4,strC5,strC6,strC7,strC8]

strE = bytes.fromhex('000800B1FD') # type (stt, dinam), speed, status(00-clear, 01-no clear), bright, end
strE_no_clear = bytes.fromhex('000801B1FD')
strS = bytes.fromhex('20') # Space

cnt_ads = -1  # counter for ads messages
tm = time.time()
isShown = False

def portWrite(str):
    if not justPrint:
        ComPort.write(str)
    print(str)

# Get texts welcome from WelcomeANSI.txt
def readWelcomes():
    try:
        with open("WelcomeANSI.txt", 'r', encoding='cp1251', errors='replace', newline='') as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]
            #print(content[0].encode("cp1251"))
            return content[0:3]
    except Exception as e:
        print("No Welcome file, greetings will by def "+str(e))

# Get text messages from MessageANSI.txt
def readMessages(str):
    try:
        with open(str, 'r', encoding='cp1251', errors='replace', newline='') as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]
            #print(content[0].encode("cp1251"))
            return content
    except Exception as e:
        print("No Mess file, greetings will by def "+str(e))

#read white, grey, black numbers of car
def readList(fileName):
    try:
        with open(fileName, 'r', encoding='cp1251', errors='replace', newline='') as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]
            #print(content[0].encode("cp1251"))
            return content
    except Exception as e:
        print("No Mess file, greetings will by def "+str(e))

# Work with car number
def readStrHandler(line):
    try:
        strList = line.split(",")
        strNum = strList[1] # number
        strNum = strNum.strip("\"")
        strNum = strNum.casefold()
        return strNum
    except Exception as e:
        print("Can't recognize num: "+line)
        return None

#print to Panel (0-3) or (0-7) strings, take str, and start num of 'Big string': 0..3
def printMessages(str, k):
    global listStrB
    global listStrC
    MAX_STR = 4

    #protect if second param is incorrect
    if k>=MAX_STR:
        print('K too big')
        return
    try:
        list = wrap(str, 24, break_long_words=True)
        if list.__len__() <= MAX_STR-k:
            for i, x in enumerate(list):
                str=listStrB[i+1] + x.encode('cp1251') + strE
                portWrite(str)
        else:
            list = wrap(str, 38, break_long_words=True)
            print("print little type:")
            print(str)
            for i, x in enumerate(list[:(MAX_STR-k)*2]):
                
                if i & 1: # odd
                    strEnd = strE_no_clear
                else:	# even
                    strEnd = strE

                str=listStrC[i+2*k] + x.encode('cp1251') + strEnd #each string has two
                time.sleep(0.4)
                portWrite(str)
    except Exception as e:
        print("print wrapped mess error:"+ str(e))

def checkForClear():
    global isShown
    global tm
    dt = time.time()-tm
    #print(dt)
    if dt>20 and isShown:
        isShown = False
        str=strB1 + strS + strE
        portWrite(str)
        str=strB2 + strS + strE
        portWrite(str)
        str=strB3 + strS + strE
        portWrite(str)
        str=strB4 + strS + strE
        portWrite(str)
        print("Clear by time")
        return True

# Read new line endless cycle - server
def follow(thefile):
    global cnt_ads
    thefile.seek(0,2)
    while True:
        try:
            line = thefile.readline()
            if not line:
                clear = checkForClear()
                time.sleep(0.2)
                if clear:
                    print("Print Ads")
                    printMessages(ads_list[cnt_ads], 0) #print string 1 from (0..3)
                    cnt_ads += 1
                    if cnt_ads >= len(ads_list):
                        cnt_ads = 0
                continue
            yield line
        except Exception as e:
            print("end..."+str(e))
            logfile.close()
            raise ValueError
            if not justPrint:
                ComPort.close()        # close port

if __name__ == '__main__':
    
    #read greetings and messages
    try:
        strWelcome1, strWelcome2, strWelcome3 = readWelcomes()
        mes_str = readMessages("MessageANSI.txt")
        strMess1, strMess2, strMess3, strMess4 = mes_str[0:4]
    except Exception as e:
        print("Ex: MessageANSI.txt read",e)
        strMess1, strMess2, strMess3, strMess4 = "Приветствуем","Здравствуйте","Въезд запрещен","Dont understand"
    
    try:
        ads_list = readMessages("AnyRecordsANSI.txt")
    except Exception as e:
        print("Ex: AnyRecordsANSI.txt read",e)
    
    if len(ads_list):   # если есть список рекламных сообщений
        cnt_ads = 0     # делаем счетчик валидным
    
    #read numbers list of cars
    list1 = readList('1.txt')
    list2 = readList('2.txt')
    list3 = readList('3.txt')
    list1 = [x.casefold() for x in list1]
    list2 = [x.casefold() for x in list2]
    list3 = [x.casefold() for x in list3]
    
    #avtomarshall file
    logfile = open("VehicleRegistrationLog.csv","r", encoding='cp1251', errors='replace', newline='')
    loglines = follow(logfile)

    for line in loglines:
        #print(line)
        strNum = readStrHandler(line)
        isShown = False
        if strNum:
            #print string 1
            print(strNum)
            strMess = strMess4
            strWelc = strWelcome1
            numExist = False

            #search in List 1
            for x in list1:
                if x.find(strNum) != -1:
                    strMess = strMess1
                    strWelc = strWelcome1
                    print("welcome1 " + strNum)
                    numExist = True
                    break
            #search in List 2
            if not numExist:
                for x in list2:
                    if x.find(strNum) != -1:
                        strMess = strMess2
                        strWelc = strWelcome2
                        print("welcome2 " + strNum + " / "+ list2[0]+ " / "+ list3[0])
                        numExist = True
                        break
            #search in List 3
            if not numExist:
                for x in list3:
                    if x.find(strNum) != -1:
                        strMess = strMess3
                        strWelc = strWelcome3
                        print("welcome3 " + strNum)
                        numExist = True
                        break
            if not numExist:
                print("welcome4(1) " + strNum+ " / "+ list2[0])

            str=strB1 + strWelc.encode('cp1251') + strS + strNum.encode('cp1251') +strE
            portWrite(str)
            #print string 2,3,4
            printMessages(strMess, 1) #print string 1 from (0..3)
            tm = time.time()
            isShown = True







