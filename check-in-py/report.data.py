# -*- coding: utf-8 -*-  
import win32com.client
import os, sys, time
from datetime import datetime
import calendar
import sendmail
import sendslack
reload(sys)
sys.setdefaultencoding('utf-8')

now = datetime.now()
baseDir = 'check-in-data\\'
personFilePath = baseDir + 'persons.json'
leaveFilePath = baseDir + 'leave.json'
checkInFilePath = baseDir + ('checkin.%s.json' % now.strftime('%Y%m%d'))
leaves = []
persons = []
list_date = {}

def getCheckInData(list_date):
    checkin = {}
    if len(list_date) == 0:
        return list_date
    zk = win32com.client.Dispatch('zkemkeeper.ZKEM.1')
    if zk.Connect_Net('10.1.9.16', 4370):
        print('Connected to 10.1.9.16')

        print("today: %d-%d-%d" % (now.year, now.month, now.day))

        if zk.ReadGeneralLogData(1):  #read All checkin data
            while 1:
                exists, machNum, idNum, emachNum, verifyMode, outMode, year, month, day, hour, minute = zk.GetGeneralLogData(1) #2
                #print(zk.GetGeneralLogData(1))
                if not exists:
                    break
                syear = str(year)
                smonth = str(month)
                sday = str(day)
                if list_date.has_key(syear) and list_date[syear].has_key(smonth) and list_date[syear][smonth].has_key(sday):
                    if (hour > 1 and hour < 12) or (hour == 12 and minute<30):
                        list_date[syear][smonth][sday]["AM"].append(idNum)
                    if hour > 12 or (hour == 12 and minute>30):
                        list_date[syear][smonth][sday]["PM"].append(idNum)
    else:
        print('Connect error')
    zk.Disconnect()
    print(list_date)
    return list_date
        
#read txt
def open_file(path):
    context = ""
    try:
        file_object = open(path)
        context = file_object.read()
        #print(persons)
    except:
        print("open_file error:" + path)
    finally:
        file_object.close( )
    return context

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("not args")
        check_year = str(now.year)
        check_month = str(now.month)
        list_date = {check_year:{check_month:{str(now.day):{"AM":[], "PM":[]}}}}
    else:
        check_year = str(args[0])
        list_date[check_year] = {}
        if len(args) > 1:
            check_month = str(args[1])
            if len(args) > 2:
                list_date = {check_year:{check_month:{args[2]:{"AM":[], "PM":[]}}}}
            else:
                list_date = {check_year:{check_month:{}}}
                count = 1
                while (count < calendar.mdays[int(check_month)]):
                    list_date[check_year][check_month][str(count)] = {"AM":[], "PM":[]}
                    count = count + 1
        else:
            count = 1
            while (count <= 12):
                list_date[check_year][str(count)] = {}
                count_day = 1
                while (count_day < calendar.mdays[count]):
                    list_date[check_year][str(count)][str(count_day)] = {"AM":[], "PM":[]}
                    count_day = count_day + 1
                count = count + 1
    print("=============list_date init=============")
    print(list_date)
    persons = eval(open_file(personFilePath))
    #print(persons)
    leaves = eval(open_file(leaveFilePath))	
    #print(leaves)
    #sys.exit(0)
    
    t = time.time()
    
    sel_data = getCheckInData(list_date)
    #sel_data = {"2018": {"2": {"9": {'AM': [], 'PM': []}}}}
    for month in list_date[check_year]:
        for day in list_date[check_year][month]:
            check_day = datetime(int(check_year), int(month), int(day))
            str_check_day = check_day.strftime('%Y-%m-%d')
            check_weekindex = check_day.weekday()
            check_day_time = time.mktime(datetime.strptime(str_check_day, "%Y-%m-%d").timetuple())
            list_date[check_year][month][day]["Weekindex"] = check_weekindex
            print(check_day)
        
            for person in persons:    
                ssn = person["SSN"]
                
                if str_check_day in leaves["Holiday"]:
                    list_date[check_year][month][day][ssn] = 0 #"Holiday"
                    continue
                if (check_weekindex == 5 or check_weekindex == 6) and (str_check_day not in leaves["Work"]):
                    list_date[check_year][month][day][ssn] = 0 #"Holiday"
                    continue
                    
                if leaves.has_key(ssn) and leaves[ssn] != "":            
                    if check_day_time - time.mktime(datetime.strptime(leaves[ssn]["From"], "%Y-%m-%d").timetuple()) >= 0 and check_day_time - time.mktime(datetime.strptime(leaves[ssn]["To"], "%Y-%m-%d").timetuple()) <= 0:
                        list_date[check_year][month][day][ssn] = 1 #"Leave"
                        continue
                
                # am+pm:2  !am+pm:3  am+!pm:4  !am+!pm:5
                isAM = person["id"] in sel_data[check_year][month][day]["AM"]
                isPM = person["id"] in sel_data[check_year][month][day]["PM"]
                if isAM and isPM:
                    list_date[check_year][month][day][ssn] = 2
                elif not isAM and isPM:
                    list_date[check_year][month][day][ssn] = 3
                elif isAM and not isPM:
                    list_date[check_year][month][day][ssn] = 4
                else:
                    list_date[check_year][month][day][ssn] = 5
    print("=============list_date result=============")
    print(list_date)
    
    f = open(checkInFilePath, 'w')
    f.write(str(list_date))
    f.close()
    
    receivers = []
    msg = ""
    print('receivers:' + msg)
    if len(receivers) > 0:
        print('start reminder...')
        try:
            sendmail.mail_send(receivers)
        except Exception, e:
            print('send email error:' + str(e))

    print("total run time:")
    e = time.time()
    print(e-t)
