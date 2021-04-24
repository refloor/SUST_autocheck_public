import smtplib
from email.mime.text import MIMEText

class EmailSender:
    __from_addr:str = None
    __pwd:str = None
    __emailer:smtplib.SMTP_SSL = None
    def __init__(self, from_addr, pwd) -> None:
        self.__from_addr = from_addr
        self.__pwd = pwd
        self.__emailer = smtplib.SMTP_SSL('smtp.qq.com', 465)
        self.__emailer.login(self.__from_addr, self.__pwd)
    def send(self, to_addr:str, content:str, subject:str) -> bool:
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = self.__from_addr
        msg['To'] = to_addr
        self.__emailer = smtplib.SMTP_SSL('smtp.qq.com', 465)
        #self.__emailer.login(self.__from_addr, self.__pwd)
        try:
            self.__emailer.login(self.__from_addr, self.__pwd)
            self.__emailer.send_message(msg=msg, from_addr=self.__from_addr, to_addrs=to_addr)
            return True
        except smtplib.SMTPException as e:
            print(e)
        return False

def main():
    msg_from = 'ccccccccheer@foxmail.com'
    msg_to = 'nnnnnnnnnick@qq.com'
    subject = 'test email'
    content = '第一封测试邮件'
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    s = smtplib.SMTP_SSL('smtp.qq.com', 465)
    s.login(msg_from, pwd)
    s.send_message(msg=msg, from_addr=msg_from, to_addrs=msg_to)
    return

if __name__ == "__main__":
    main()