# -*- coding: utf-8 -*-  
import win32com.client
import os, sys, time, random
from datetime import datetime
import sendmail
import sendslack
reload(sys)
sys.setdefaultencoding('utf-8')

baseDir = 'check-in-data\\'
personFilePath = baseDir + 'persons.json'
leaveFilePath = baseDir + 'leave.json'
leaves = []
persons = []

def getCheckInData():
    checkin = []
    zk = win32com.client.Dispatch('zkemkeeper.ZKEM.1')
    if zk.Connect_Net('10.1.9.16', 4370):
        print('Connected to 10.1.9.16')

        now = datetime.now()
        print("today: %d-%d-%d" % (now.year, now.month, now.day))

        if zk.ReadGeneralLogData(1):  #read All checkin data
            while 1:
                exists, machNum, idNum, emachNum, verifyMode, outMode, year, month, day, hour, minute = zk.GetGeneralLogData(1) #2
                if not exists:
                    break
                if now.year == year and now.month == month and now.day == day and verifyMode == 1:
                    checkin.append(idNum)
    else:
        print('Connect error')
    zk.Disconnect()
    print(checkin)
    return checkin
        
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

    persons = eval(open_file(personFilePath))
    #print(persons)
    leaves = eval(open_file(leaveFilePath))	
    #print(leaves)
    
    t = time.time()
    str_today = datetime.now().strftime("%Y-%m-%d")
    today_time = time.mktime(datetime.strptime(str_today, "%Y-%m-%d").timetuple())
    weekIndex = datetime.now().weekday()

    #print(leaves[str_today])
    if str_today in leaves["Holiday"]:   #holiday
        sys.exit(0)
    if (weekIndex == 5 or weekIndex == 6) and (str_today not in leaves["Work"]):
        sys.exit(0)
     
    sel_data = getCheckInData()
    for person in persons:
        ssn = person["SSN"]
        if leaves.has_key(ssn) and leaves[ssn] != "":            
            if today_time - time.mktime(datetime.strptime(leaves[ssn]["From"], "%Y-%m-%d").timetuple()) >= 0 and today_time - time.mktime(datetime.strptime(leaves[ssn]["To"], "%Y-%m-%d").timetuple()) <= 0:
                person["Checked"] = True
                continue
                
        if person["id"] in sel_data:
            person["Checked"] = True
    #print(persons)
    receivers = []
    msg = ""
    for person in persons:
        if person["Checked"] == False:
            slack = person["SSN"]
            if person.has_key("Slack"):
                slack = person["Slack"]
            receivers.append(person["SSN"] + "@seekasia.com")
            msg += "<@" + slack.lower() + "> "
    print('receivers:' + msg)
    if len(receivers) > 0:
        print('start reminder...')
        try:
            sendmail.mail_send(receivers)
        except Exception, e:
            print('send email error:' + str(e))

        try:
            tips = ["{0} 虽然没有全勤奖，但是来了就请打个卡呗！", 
					"{0} 上班不打卡，你三老爷他大舅知道不？反正本AI已经知道了。", 
					"本日最佳忘性奖获得者: {0} 连早卡都没打, 还想不想要工资了!", 
					"试问SZOffice谁最浪? 那可非{0}莫属，浪起来可是连早卡都不打.", 
					"{0} Bug什么时候都可以写，麻烦先把早卡打了去！"]
            tip = tips[random.randrange(0, len(tips))]
            sendslack.slack_send(tip.replace("{0}", msg))
        except Exception, e:
            print('send email error:' + str(e))
            
    print("total run time:")
    e = time.time()
    print(e-t)
