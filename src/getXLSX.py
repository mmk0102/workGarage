import xlrd
import re

# Russian to English letters for compare unified
ru_en_table = str.maketrans({'А': 'A', 'В': 'B','Е': 'E', 'К': 'K','М': 'M', 'Н': 'H','О': 'O', 'Р': 'P','С': 'C', 'Т': 'T','У': 'Y', 'Х': 'X',
'а': 'a', 'в': 'b','е': 'e', 'к': 'k','м': 'm', 'н': 'h','о': 'o', 'р': 'p','с': 'c', 'т': 't', 'у': 'y', 'х': 'x'})

def list_to_file(name, my_list):
    with open(name, 'w') as f:
        for x in my_list:
            f.write("%s\n" % x)

# Open no debt persons
workbook = xlrd.open_workbook("C:\managePanel\\N.xls","rb") # "C:\managePanel\\"  --  "C:\my\work\workGarage\src\\"
#sheet_count = workbook.nsheets

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
    if db != '' and nm != '': # if exist debt
         lst_2.append((str)(nm).strip().translate(ru_en_table).upper())
    elif nm != '':
        lst_1.append((str)(nm).strip().translate(ru_en_table).upper())

# print('A:',lst_1, end=' ')
# print('B:',lst_2, end=' ')

base_num = [] # result = list of numbers
for x in lst_1:
    base_num += re.findall(r"\w\d\d\d\w\w\s*\d+", x)

lst_1 = list(set(lst_1)) # remove duplicates
list_to_file('1.txt',base_num) # write to file

base_num = [] # result = list of numbers
for x in lst_2:
    base_num += re.findall(r"\w\d\d\d\w\w\s*\d+", x)

lst_2 = list(set(lst_2)) # remove duplicates
list_to_file('2.txt',base_num) # write to file

# Open debt persons
workbook = xlrd.open_workbook("C:\my\work\workGarage\src\\D.xls","rb") # "C:\managePanel\\"  current_dir = "C:\my\work\workGarage\src\\"
sheet = workbook.sheet_by_index(0)
num_lst = sheet.col_values(6)
lst_3 = []
for x in num_lst:
    if x != '':
        t = re.findall(r"\w\d\d\d\w\w\s*\d+", (str)(x).strip().translate(ru_en_table).upper())
        lst_3 += t
        print(t)

lst_3 = list(set(lst_3)) # remove duplicates
list_to_file('3.txt',lst_3) # write to file


# check for repitition
for x in lst_1:
    for y in lst_2:
        if x==y:
            print('Номер',x,'совпадает в 1 и 2 списках!!!')
    for z in lst_3:
        if x==z:
            print('Номер',x,'совпадает в 1 и 3 списках')
for y in lst_2:
    for z in lst_3:
        if y==z:
            print('Номер',z,'совпадает в 2 и 3 списках')