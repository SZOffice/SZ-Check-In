# -*- coding: utf-8 -*-  
import os, sys, time
from datetime import datetime
import pypyodbc
import sendmail
import sendslack

baseDir = 'check-in-data\\'
dataFilePath = baseDir + 'att2000.mdb'
personFilePath = baseDir + 'persons.json'
leaveFilePath = baseDir + 'leave.json'
leaves = []
persons = []

#定义conn
def mdb_conn(db_name, password = ""):
    """
    功能：创建数据库连接
    :param db_name: 数据库名称
    :param db_name: 数据库密码，默认为空
    :return: 返回数据库连接
    """
    str = 'Driver={Microsoft Access Driver (*.mdb)};PWD' + password + ";DBQ=" + db_name
    #print(str)
    conn = pypyodbc.connect(str, unicode_results=False)

    return conn

#查询记录
def mdb_sel(cur, sql):
    """
    功能：向数据库查询数据
    :param cur: 游标
    :param sql: sql语句
    :return: 查询结果集
    """
    try:
        cur.execute(sql)
        return cur.fetchall()
    except:
        return []

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
    
    if not os.path.exists(dataFilePath):
        try:
            sendmail.mail_send_admin("check in system database file not exists")
        except Exception, e:
            print('send email error:' + str(e))
        sys.exit(0)
    conn = mdb_conn(dataFilePath)
    cur = conn.cursor()
    
    t = time.time()
    str_today = datetime.now().strftime("%Y-%m-%d")
    today_time = time.mktime(datetime.strptime(str_today, "%Y-%m-%d").timetuple())
    weekIndex = datetime.now().weekday()

    #print(leaves[str_today])
    if str_today in leaves["Holiday"]:   #holiday
        sys.exit(0)
    if (weekIndex == 5 or weekIndex == 6) and (str_today not in leaves["Work"]):
        sys.exit(0)
    
    sql = "SELECT u.SSN FROM USERINFO u Inner join CHECKINOUT c on u.USERID=c.USERID where checktime>#" + str_today + "#"
    sel_data = mdb_sel(cur, sql)    
    for person in persons:
        ssn = person["SSN"]
        if leaves.has_key(ssn) and leaves[ssn] != "":            
            if today_time - time.mktime(datetime.strptime(leaves[ssn]["From"], "%Y-%m-%d").timetuple()) >= 0 and today_time - time.mktime(datetime.strptime(leaves[ssn]["To"], "%Y-%m-%d").timetuple()) <= 0:
                person["Checked"] = True
                continue
        for sel in sel_data:
            if ssn == sel[0]:
                person["Checked"] = True
                break
    #print(persons)
    receivers = []
    msg = ""
    for person in persons:
        if person["Checked"] == False:
            receivers.append(person["SSN"] + "@seekasia.com")
            msg += "<@" + person["SSN"].lower() + "> "
    print('receivers:' + msg)
    if len(receivers) > 0:
        print('start reminder...')
	try:
            sendmail.mail_send(receivers)
	except Exception, e:
            print('send email error:' + str(e))
	
	try:
            sendslack.slack_send("Hi, " + msg + " 你们早上没打卡, 请补打!")
	except Exception, e:
            print('send email error:' + str(e))
            
    cur.close()    #关闭游标
    conn.close()   #关闭数据库连接
    
    print("total run time:")
    e = time.time()
    print(e-t)
