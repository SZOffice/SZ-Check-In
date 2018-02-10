# -*- coding: utf-8 -*-  
import win32com.client
import os, sys, time
from datetime import datetime
from jinja2 import Template
import sendmail
reload(sys)
sys.setdefaultencoding('utf-8')

now = datetime.now()
baseDir = 'check-in-data\\'
checkInFilePath = baseDir + ('checkin.%s.json' % now.strftime('%Y%m%d'))
templateFilePath = baseDir + "template.report.html"
reportFilePath = baseDir + "check_in_report.html"
list_date = {}
  
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
        
    list_check_in = eval(open_file(checkInFilePath))
    template_report = str(open_file(templateFilePath))
    
    t = time.time()
    
    template = Template(template_report)
    html = template.render(checkin = list_check_in)
    
    f = open(reportFilePath, 'w')
    f.write(html)
    f.close()
    
    receivers = ["miragelu@seekasia.com"]
    msg = "Report at %s for check in system" % now.strftime('%Y%m%d')
    print('receivers:' + str(receivers))
    if len(receivers) > 0:
        print('start send email...')
        try:
            sendmail.mail_send_report(receivers, msg, reportFilePath)
        except Exception, e:
            print('send email error:' + str(e))

    print("total run time:")
    e = time.time()
    print(e-t)
