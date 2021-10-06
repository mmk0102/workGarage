import xlrd
import re

# Russian to English letters for compare unified
ru_en_table = str.maketrans({'А': 'A', 'В': 'B','Е': 'E', 'К': 'K','М': 'M', 'Н': 'H','О': 'O', 'Р': 'P','С': 'C', 'Т': 'T','У': 'Y', 'Х': 'X',
'а': 'a', 'в': 'b','е': 'e', 'к': 'k','м': 'm', 'н': 'h','о': 'o', 'р': 'p','с': 'c', 'т': 't', 'у': 'y', 'х': 'x'})

def list_to_file(name, my_list):
    with open(name, 'w') as f:
        for x in my_list:
            f.write("%s\n" % x)

workbook = xlrd.open_workbook("C:\my\work\workGarage\src\\N.xls","rb")
sheet_count = workbook.nsheets
print(sheet_count)

#for sheetno in range(sheet_count):
sheet = workbook.sheet_by_index(0)
print ("Sheet name:", sheet.name)
debt_lst = sheet.col_values(18)
num_lst = sheet.col_values(6)
# print('A:',num_lst, end=' ')
# print('B:',debt_lst, end=' ')

lst_1 = []
lst_2 = []
# Processing for White and Grey list of car numbers (lists 1 and 2)
for nm, db in zip(num_lst, debt_lst):
    print((str)(nm).strip(), (str)(db).strip())
    
    if db != '' and nm != '': # if exist debt
         lst_2.append((str)(nm).strip().translate(ru_en_table).upper())
    elif nm != '':
        lst_1.append((str)(nm).strip().translate(ru_en_table).upper())

# print('A:',lst_1, end=' ')
# print('B:',lst_2, end=' ')

base_num = [] # result = list of numbers
for x in lst_1:
    base_num += re.findall(r"\w\d\d\d\w\w\d+", x)# re.findall(u"^[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}$", x)
list_to_file('1.txt',base_num)

base_num = [] # result = list of numbers
for x in lst_2:
    base_num += re.findall(r"\w\d\d\d\w\w\d+", x)# re.findall(u"^[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}$", x)
list_to_file('2.txt',base_num)
