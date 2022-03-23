import pandas as pd
import numpy as np
import xlrd
import openpyxl
import os
from pandas import DataFrame


#ön izleme limiti
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 100)

with open("Ethernet_Function_Setting_Bridge_Setting.csv",'r') as f:
    with open("df1.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)

with open("iPASOLINK iX_Equipment_Setup_Radio_Configuration.csv",'r') as f:
    with open("df2.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)

with open("QoS_Configuration_Port_Setting.csv",'r') as f:
    with open("df3.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)

with open("QoS_Configuration_Classify_Setting_-_Active_Classify_Profile_Information.csv",'r') as f:
    with open("df4.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)

df1= pd.read_csv("df1.csv",  usecols=[0,2,3,10,11])
df2= pd.read_csv("df2.csv",  usecols=[0,2,3,11,15])
df3= pd.read_csv("df3.csv",  usecols=[0,2,3,11,24,30])
df4= pd.read_csv("df4.csv",  usecols=[0,2,3,11,12])

n1=df1.loc[df1["10GbE / GbE MAX Frame Size [byte]"] != "9600 [byte]"]
n2=df1.loc[df1["FE Max Frame Size [byte]"] != "2000 [byte]"]

n3=df2.loc[df2["TX Power Control {(No.1)|(SW GRP1)}"]=="MTPC"]
n3.drop(["Reference Modulation {(No.1)|(SW GRP1)}"],axis=1,inplace=True)

n4=df2.loc[df2["Reference Modulation {(No.1)|(SW GRP1)}"]!="4-QAM"]
n4=df2.loc[df2["Reference Modulation {(No.1)|(SW GRP1)}"]!="CQPSK"]
n4=df2.loc[df2["Reference Modulation {(No.1)|(SW GRP1)}"]!="QPSK"]
n4.drop(["TX Power Control {(No.1)|(SW GRP1)}"],axis=1,inplace=True)


n5=df3.loc[df3["Scheduling Mode"]=="4xSP"]
n5.drop(["Class 0 Queue Length [kbyte]","Class 1 Queue Length [kbyte]"],axis=1,inplace=True)
n6=df3.loc[df3["Scheduling Mode"]=="8XSP"]
n6=df3.loc[df3["Class 0 Queue Length [kbyte]"]!=512]
n6=df3.loc[df3["Class 1 Queue Length [kbyte]"]!=512]

df41=df4["Classify Priority"].apply(str)+'*'+df4["Classify Internal Priority"].apply(str)
df4.insert(loc=0, column='check_n7',value=df41)
n71=df4.loc[df4['check_n7']=="4*4"]
n72=df4.loc[df4['check_n7']=="5*5"]
n7=n71.append(n72, ignore_index=True)
n7.drop(["check_n7"],axis=1,inplace=True)

wr5 = pd.ExcelWriter('NEC_Check.xlsx')
n1.to_excel(wr5, sheet_name='MTU_SIZE_GB')
n2.to_excel(wr5, sheet_name='MTU_SIZE_FE')
n3.to_excel(wr5, sheet_name='ATPC')
n4.to_excel(wr5, sheet_name='REF_MOD')
n5.to_excel(wr5, sheet_name='QOS_CLASS_4')
n6.to_excel(wr5, sheet_name='QOS_CLASS_8')
n7.to_excel(wr5, sheet_name='QOS_CLASS_PRI')
wr5.save()


os.remove("df1.csv")
os.remove("df2.csv")
os.remove("df3.csv")
os.remove("df4.csv")
