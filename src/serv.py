import sys
import time
import serial
from datetime import datetime
from textwrap import wrap

# настройка цвета текста
COLOR = "01" # Красный - 01, Зеленый - 02, Желтый - 03, Синий - 04, Пурпурный - 05, Голубой - 06, Белый - 07

# длительность одного рекламного сообщения (сек)
WAIT_TIME = 35 # время отображения сообщения для водителя после въезда (time of display of message for the driver after entry)

# часы отображения рекламы (с .. по ..)
START_TIME_VIEW = 7
END_TIME_VIEW = 21

# текущая директория
current_dir = "C:\managePanel\\" # "C:\managePanel\\"  current_dir = "C:\my\work\workGarage\src\\"

justPrint = False # для отладки - только печать без использования сом-порта (панели). (use without com port, just print, for debug)

strWelcome1 = "Privet"
strWelcome2 = "Privet"
strWelcome3 = "Privet"
strMess1, strMess2, strMess3, strMess4 = "Приветствуем", "Здравствуйте", "Въезд запрещен", "Dont understand"
if not justPrint:
    ComPort = serial.Serial('COM3')
    ComPort.baudrate = 2400
    ComPort.bytesize = 8
    ComPort.parity = 'N'
    ComPort.stopbits = 1

# Choose string on TAB (1-4)
strB1 = bytearray.fromhex('FFA003'+COLOR+'0000') # prefix FF, addr, shrift, color, x, y
strB2 = bytearray.fromhex('FFA103'+COLOR+'0000')
strB3 = bytearray.fromhex('FFA203'+COLOR+'0000')
strB4 = bytearray.fromhex('FFA303'+COLOR+'0000')

listStrB = [strB1,strB2,strB3,strB4]

# Choose string on TAB (1-8)
strC1 = bytearray.fromhex('FFA001'+COLOR+'000A')
strC2 = bytearray.fromhex('FFA001'+COLOR+'0000')
strC3 = bytearray.fromhex('FFA101'+COLOR+'000A')
strC4 = bytearray.fromhex('FFA101'+COLOR+'0000')
strC5 = bytearray.fromhex('FFA201'+COLOR+'000A')
strC6 = bytearray.fromhex('FFA201'+COLOR+'0000')
strC7 = bytearray.fromhex('FFA301'+COLOR+'000A')
strC8 = bytearray.fromhex('FFA301'+COLOR+'0000')

# Russian to English letters for compare unified
ru_en_table = str.maketrans({'А': 'A', 'В': 'B','Е': 'E', 'К': 'K','М': 'M', 'Н': 'H','О': 'O', 'Р': 'P','С': 'C', 'Т': 'T','У': 'Y', 'Х': 'X',
'а': 'a', 'в': 'b','е': 'e', 'к': 'k','м': 'm', 'н': 'h','о': 'o', 'р': 'p','с': 'c', 'т': 't', 'у': 'y', 'х': 'x'})

listStrC = [strC1,strC2,strC3,strC4,strC5,strC6,strC7,strC8]

strE = bytes.fromhex('000800B1FD') # type (stt, dinam), speed, status(00-clear, 01-no clear), bright, end
strE_no_clear = bytes.fromhex('000801B1FD')
strS = bytes.fromhex('20') # Space

cnt_ads = -1  # counter for ads messages
tm = time.time() - WAIT_TIME + 1 # первую рекламму напечатает через секунду после вкл.
time60 = time.time() # для 60 сек событий
isShown = True # Есть напечатанное приветствие для авто. (по умолчанию 1 что бы при включении печатал рекламу)

def portWrite(str):
    if not justPrint:
        ComPort.write(str)
    print(str)

# Get texts welcome from WelcomeANSI.txt
def readWelcomes():
    try:
        with open(current_dir+"WelcomeANSI.txt", 'r', encoding='cp1251', errors='replace', newline='') as f:
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
        with open(current_dir+str, 'r', encoding='cp1251', errors='replace', newline='') as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]
            #print(content[0].encode("cp1251"))
            return content
    except Exception as e:
        print("No Mess file, greetings will by def "+str(e))

#read white, grey, black numbers of car
def readList(fileName):
    global ru_en_table
    try:
        with open(current_dir+fileName, 'r', encoding='utf-8', errors='replace', newline='') as f: #-sig
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip().translate(ru_en_table).upper() for x in content]
            return content
    except Exception as e:
        print("No Mess file, greetings will by def "+str(e))

# Work with car number
def readStrHandler(line):
    try:
        strList = line.split(",")
        strDirection = strList[6]

        strDirection = strDirection.strip("\"")
        if strDirection == "РЎРЅРёР·Сѓ РІРІРµСЂС…": # РЎРЅРёР·Сѓ РІРІРµСЂС… это 'Снизу вверх' - авто выезжает
            print('Car is go out - do nothing')
            return None

        strNum = strList[1] # number
        strNum = strNum.strip("\"")
        return strNum
    except Exception as e:
        if len(line) != 2: # этот случай возникает при не пустой строке
            print("Can't recognize num: ", len(line), str(e))
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
                str=listStrB[i] + x.encode('cp1251') + strE
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
    global WAIT_TIME
    global isShown
    global tm
    dt = time.time() - tm
    # Условие смены рекламы по времени
    if dt > 80:
        tm = time.time()
        isShown = True
    #print('dT = ',dt)
    if dt>WAIT_TIME and isShown:
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
    global cnt_ads, time60
    thefile.seek(0,2)
    while True:
        # 60 секундные события
        if time.time() - time60 > 60:
            time60 = time.time()
            print("one minute gone")
            readFiles() #read adv. mess and etc. from files
        try:
            line = thefile.readline()
            if not line:
                clear = checkForClear()
                time.sleep(0.2)
                if clear:
                    hour = datetime.now().hour
                    if cnt_ads > -1 and hour > START_TIME_VIEW and hour < END_TIME_VIEW: # show reclamu in certan hours
                        print("Print Ads hour =",hour)
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

def readFiles():
    global strWelcome1, strWelcome2, strWelcome3, strMess1, strMess2, strMess3, strMess4, cnt_ads, ads_list, list1, list2, list3
    #read greetings and messages
    try:
        strWelcome1, strWelcome2, strWelcome3 = readWelcomes()
        mes_str = readMessages("MessageANSI.txt")
        strMess1, strMess2, strMess3, strMess4 = mes_str[0:4]
    except Exception as e:
        print("Ex: MessageANSI.txt read",e)
        strMess1, strMess2, strMess3, strMess4 = "Приветствуем", "Здравствуйте", "Въезд запрещен", "Dont understand"

    try:
        ads_list = readMessages("reclamaANSI.txt")
    except Exception as e:
        print("Ex: reclamaANSI.txt read",e)
    
    if len(ads_list):   # если есть список рекламных сообщений
        if cnt_ads == -1: # первое считываение
            cnt_ads = 0     # делаем счетчик валидным
        elif cnt_ads >=  len(ads_list): # если число сообщений уменьшилось и меньше текущего
            cnt_ads = 0     # переходим в начало списка
    
    #read numbers list of cars
    list1 = readList('1.txt')
    list2 = readList('2.txt')
    list3 = readList('3.txt')

if __name__ == '__main__':

    #read adv. mess and etc. from files
    readFiles()

    #avtomarshall file
    logfile = open(current_dir+"VehicleRegistrationLog.csv","r", encoding='cp1251', errors='replace', newline='')
    loglines = follow(logfile)

    for line in loglines:
        #print(line)
        if len(line) > 2: # если строка не пустая
            strNum = readStrHandler(line)
        else:
            strNum = None
        isShown = False
        if strNum:
            #print string 1
            print(strNum)
            strMess = strMess4
            strWelc = strWelcome1
            numExist = False
            
            #search in List 3 - HIGH PRIORITY
            if not numExist:
                for x in list3:
                    if x.find(strNum) != -1:
                        strMess = strMess3
                        strWelc = strWelcome3
                        print("welcome3 " + strNum)
                        numExist = True
                        break
            #search in List 1 - MIDDLE PRIORITY
            for x in list1:
                if x.find(strNum) != -1:
                    strMess = strMess1
                    strWelc = strWelcome1
                    print("welcome1 " + strNum)
                    numExist = True
                    break
            #search in List 2 - LOW PRIORITY
            if not numExist:
                for x in list2:
                    if x.find(strNum) != -1:
                        strMess = strMess2
                        strWelc = strWelcome2
                        print("welcome2 " + strNum)
                        numExist = True
                        break

            if not numExist:
                print("welcome4 (no recognize) " + strNum)

            str=strB1 + strWelc.encode('cp1251') + strS + strNum.encode('cp1251') +strE
            portWrite(str)
            #print string 2,3,4
            printMessages(strMess, 1) #print string 1 from (0..3)
            tm = time.time()
            isShown = True