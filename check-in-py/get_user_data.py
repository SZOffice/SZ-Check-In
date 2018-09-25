# -*- coding: utf-8 -*-  
import win32com.client
import os, sys, time
from datetime import datetime
import calendar

now = datetime.now()
baseDir = 'check-in-data\\'
if not os.path.exists(baseDir):
    baseDir = sys.path[0] + '\\..\\check-in-data\\'
personFilePath = baseDir + 'persons.json'
leaveFilePath = baseDir + 'leave.json'
checkInFilePath = baseDir + ('checkin.%s.json' % now.strftime('%Y%m%d'))
leaves = []
persons = []
list_date = {}

def getAllUserInfo():
    list_info = []
    zk = win32com.client.Dispatch('zkemkeeper.ZKEM.1')
    if zk.Connect_Net('10.1.9.16', 4370):
        print('Connected to 10.1.9.16')

        if zk.ReadAllUserID(1):  #read All checkin data
            while 1:
                info = {}
                dwMachineNumber, dwEnrollNumber, Name, Password, Privilege, dwEnable = zk.GetAllUserInfo(1)
#机器号  dwEnrollNumber 
#用户号   Name 
#用户姓名   Password 
#用户密码   Privilege 
#用户权限，0 为普通用户，1 为登记员，2 为管理员，3 为超级管理员   dwEnable 
                #print(zk.GetGeneralLogData(1))
                if not dwMachineNumber:
                    print('GetAllUserInfo error')
                    break
                info["dwMachineNumber"] = dwMachineNumber
                info["dwEnrollNumber"] = dwEnrollNumber
                info["Name"] = Name
                info["Password"] = Password
                info["Privilege"] = Privilege
                info["dwEnable"] = dwEnable
                list_info.append(info)
    else:
        print('Connect error')
    zk.Disconnect()
    print(info)
    return info

if __name__ == "__main__":
    t = time.time()
    
    args = sys.argv[1:]
    if not args:
        print("not args")
    else:
        param1 = str(args[0])
    
    users = getAllUserInfo()
    f = open("./users.json", 'w')
    f.write(str(users))
    f.close()
        
    print("total run time:")
    e = time.time()
    print(e-t)
