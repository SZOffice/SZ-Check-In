# -*- coding: utf-8 -*-  
import win32com.client
import os, sys, time, datetime, random
import sendmail
import sendslack
reload(sys)
sys.setdefaultencoding('utf-8')

baseDir = 'check-in-data\\'
if not os.path.exists(baseDir):
    baseDir = '..\\check-in-data\\'
personFilePath = baseDir + 'persons.json'
leaveFilePath = baseDir + 'leave.json'
leaves = []
persons = []

def getCheckInData():
    last_check_out = {"idNum":"", "hour":0, "minute":0}
    checkin = []
    now = datetime.datetime.now()
    last_work_day = get_last_workday(now)
    zk = win32com.client.Dispatch('zkemkeeper.ZKEM.1')
    
    if zk.Connect_Net('10.1.9.16', 4370):
        print('Connected to 10.1.9.16')

        if zk.ReadGeneralLogData(1):  #read All checkin data
            while 1:
                exists, machNum, idNum, emachNum, verifyMode, outMode, year, month, day, hour, minute = zk.GetGeneralLogData(1) #2
                if not exists:
                    break
                if now.year == year and now.month == month and now.day == day and verifyMode == 1:
                    checkin.append(idNum)
                if last_work_day.year == year and last_work_day.month == month and last_work_day.day == day and verifyMode == 1:
                    if hour > last_check_out["hour"] or (hour == last_check_out["hour"] and minute > last_check_out["minute"]):
                        last_check_out = {"idNum":idNum, "hour":hour, "minute":minute}
    else:
        print('Connect error')
    zk.Disconnect()
    print(last_work_day)
    print(last_check_out)
    return (checkin, last_check_out)
        
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

def get_last_workday(date):
    last_workday = date + datetime.timedelta(days = -1)
    last_workday_str = last_workday.strftime("%Y-%m-%d")
    last_workday_weekIndex = last_workday.weekday()
    
    if last_workday_str in leaves["Holiday"]:   #holiday        
        last_workday = get_last_workday(last_workday)
    if (last_workday_weekIndex == 5 or last_workday_weekIndex == 6) and (last_workday_str not in leaves["Work"]):        
        last_workday = get_last_workday(last_workday)
    
    return last_workday;
    
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("not args")

    persons = eval(open_file(personFilePath))
    #print(persons)
    leaves = eval(open_file(leaveFilePath))
    #print(leaves)
    
    t = time.time()
    str_today = datetime.datetime.now().strftime("%Y-%m-%d")
    weekIndex = datetime.datetime.now().weekday()
    today_time = time.mktime(datetime.datetime.strptime(str_today, "%Y-%m-%d").timetuple())
    
    #print(leaves[str_today])
    if str_today in leaves["Holiday"]:   #holiday
        sys.exit(0)
    if (weekIndex == 5 or weekIndex == 6) and (str_today not in leaves["Work"]):
        sys.exit(0)
        
    (sel_data, last_check_out) = getCheckInData()
    for person in persons:
        ssn = person["SSN"]
        if leaves.has_key(ssn) and leaves[ssn] != "":            
            if today_time - time.mktime(datetime.datetime.strptime(leaves[ssn]["From"], "%Y-%m-%d").timetuple()) >= 0 and today_time - time.mktime(datetime.datetime.strptime(leaves[ssn]["To"], "%Y-%m-%d").timetuple()) <= 0:
                person["Checked"] = True
                continue
                
        if person["id"] in sel_data:
            person["Checked"] = True
            
    receivers = []
    msg = ""
    for person in persons:
        ssn = person["SSN"]
        if person["id"] == last_check_out["idNum"]:
            slack = person["SSN"]
            if person.has_key("Slack"):
                slack = person["Slack"]
            receivers.append(person["SSN"] + "@seekasia.com")
            msg += "<@" + slack.lower() + "> "
            
    print('receivers:' + msg)
    if len(receivers) > 0:
        print('start reminder...')
        try:
            sendmail.mail_send3("钥匙归位提醒", "亲， \n\n  本探根据蛛丝马迹发现昨儿u最晚下班，那么请把钥匙归回原位呗... \n\n  谢谢配合。 \n\nSincerely, \n\nCDC Office", receivers)
        except Exception, e:
            print('send email error:' + str(e))

        try:
            tips = ["{0} 虽然加班再晚也无奖金，不过钥匙还是得交出来滴。", 
                    "最佳晚归奖获得者: {0} 公司是你家, 你爱你家, 但是请记住钥匙是大家的!", 
                    "下班不回家，思想有问题。 {0} 赶快交出钥匙再去写个Bug压压惊", 
                    "{0} 加班那么晚，让其他同事情何以堪？交出钥匙继续写Bug去", 
                    "{0} 如果加班就能拿优秀员工的话，那么请把钥匙留下，让我来!", 
                    "{0} 加班不过是一个程序猿/媛的基本操作. 但是本AI只管钥匙, 无视操作"]
            tip = tips[random.randrange(0, len(tips))]
            sendslack.slack_send(tip.replace("{0}", msg))
        except Exception, e:
            print('send email error:' + str(e))
            
    receivers_in = []
    msg_in = ""
    for person in persons:
        if person["Checked"] == False:
            slack = person["SSN"]
            if person.has_key("Slack"):
                slack = person["Slack"]
            receivers_in.append(person["SSN"] + "@seekasia.com")
            msg_in += "<@" + slack.lower() + "> "
    print('receivers_in:' + msg_in)
    if len(receivers_in) > 0:
        print('start reminder...')
        try:
            sendmail.mail_send(receivers_in)
        except Exception, e:
            print('send email error:' + str(e))
            
        try:
            tips = ["{0} 虽然没有全勤奖，但是来了就请打个卡呗！", 
                    "{0} 上班不打卡，你三老爷他大舅知道不？反正本AI已经知道了。", 
                    "本日最佳忘性奖获得者: {0} 连早卡都没打, 还想不想要工资了!", 
                    "试问SZOffice谁最浪? 那可非{0}莫属，浪起来可是连早卡都不打.", 
                    "{0} Bug什么时候都可以写，麻烦先把早卡打了去！"]
            tip = tips[random.randrange(0, len(tips))]
            sendslack.slack_send(tip.replace("{0}", msg_in))
        except Exception, e:
            print('send email error:' + str(e))
            
    print("total run time:")
    e = time.time()
    print(e-t)
