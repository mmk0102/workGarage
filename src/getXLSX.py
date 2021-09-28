import xlrd
import pandas

workbook = xlrd.open_workbook("C:\my\work\workGarage\src\\N.xls","rb")
sheet_count = workbook.nsheets
print(sheet_count)
#for sheetno in range(sheet_count): 
sheet = workbook.sheet_by_index(0)
print ("Sheet name:", sheet.name)
ku_ind_lst = sheet.col_values(0)
sys_name_lst = sheet.col_values(6)
print('A:',ku_ind_lst)
print('B:',sys_name_lst)
