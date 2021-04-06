import datetime
import smtplib
import socket
import time
from email.mime.text import MIMEText

from mako.template import Template

import config
import ip_cache_checker

# 邮箱账户设置
email_config = config.ConfigHelper.get_config()


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('223.5.5.5', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def send_mail(content="公司笔记本IP定时公告"):
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = email_config.sender
    message['To'] = 'matrix'
    message['Subject'] = '公司笔记本-IP定时公告'

    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(email_config.mail_host, email_config.mail_port)
        smtp_obj.login(email_config.mail_user, email_config.mail_password)
        smtp_obj.sendmail(email_config.sender, email_config.receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


if __name__ == '__main__':
    print('脚本开始执行 [%s] ============================' % datetime.datetime.now())
    ip = get_ip()
    check_result = ip_cache_checker.check_ip_change(ip)
    if not check_result.result:
        print('无需发送邮件. 脚本结束')
    else:
        print('即将发送邮件...')
        template = Template(filename='template.html')
        content = template.render(ip=ip, time=check_result.last_m_time)
        send_mail(content)
    print('\n')
