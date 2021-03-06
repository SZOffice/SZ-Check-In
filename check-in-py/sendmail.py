# -*- coding: utf-8 -*-   
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host="smtp.126.com"  #设置服务器
mail_user="ifelse01@126.com"    #用户名
mail_pass="******"   #口令 

sender = 'ifelse01@126.com'
receivers = ['miragelu@seekasia.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
body = "亲， \n\n  您今天上班未打卡， 打个卡去呗... \n\n  谢谢配合。 \n\nSincerely, \n\nCDC Office"

def mail_send2(receivers):  
    print('send mail start...' )
    msg = MIMEText(body, 'plain', 'utf-8')
    msg["From"] = sender  
    msg["To"] = ""  
    msg["Subject"] = "打卡提醒"  
    smtpObj = smtplib.SMTP() 
    smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass) 
    smtpObj.sendmail(sender, receivers, msg.as_string())  
    smtpObj.quit()  
    print('send mail finished...')
    

def mail_send(receivers):  
    print('send mail start...') 
    msg = MIMEText(body, 'plain', 'utf-8')
    msg["From"] = 'SZ-OA@seekasia.com'  
    msg["To"] = ""  
    msg["Subject"] = "打卡提醒"  
    smtpObj = smtplib.SMTP("10.101.1.52")
    smtpObj.sendmail(sender, receivers, msg.as_string())  
    smtpObj.quit()  
    print('send mail finished...')

def mail_send_report(receivers, message, attachFilePath):  
    from email.mime.multipart import MIMEMultipart
    print('send mail start...')  
    msg = MIMEMultipart()
    msg["From"] = Header('SZ-OA@seekasia.com', 'utf-8')
    msg["To"] = Header('check in report', 'utf-8')
    msg["Subject"] = Header('check in report', 'utf-8')
    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    
    att1 = MIMEText(open(attachFilePath, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="check_in_report.html"'
    msg.attach(att1)

    smtpObj = smtplib.SMTP("10.101.1.52")
    smtpObj.sendmail(sender, receivers, msg.as_string())  
    smtpObj.quit()  
    print('send mail finished...')
    
def mail_send_admin(message):  
    print('send mail to admin start...')
    msg = MIMEText(message, 'plain', 'utf-8')
    msg["From"] = 'SZ-OA@seekasia.com'  
    msg["To"] = "miragelu@seekasia.com"  
    msg["Subject"] = "打卡提醒出错"  
    smtpObj = smtplib.SMTP("10.101.1.52")
    smtpObj.sendmail(sender, ['miragelu@seekasia.com', 'candu@seekasia.com', 'echoliao@seekasia.com'], msg.as_string())  
    smtpObj.quit()  
    print('send mail finished...' )

def mail_send3(subject, message, receivers):  
    print('send mail start...')
    msg = MIMEText(message, 'plain', 'utf-8')
    msg["From"] = 'SZ-OA@seekasia.com'  
    msg["To"] = ""  
    msg["Subject"] = subject 
    smtpObj = smtplib.SMTP("10.101.1.52")
    smtpObj.sendmail(sender, receivers, msg.as_string())
    smtpObj.quit()  
    print('send mail finished...' )