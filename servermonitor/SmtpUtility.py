import smtplib

class SmtpUtility():
    @staticmethod
    def send(mailprops, content):
        msg = ("From: %s\r\nSubject: Scratch2Catrobat Converter issue\r\nTo: %s\r\n\r\n"
               % (mailprops.smtp_from, ", ".join(mailprops.smtp_send_to)))
        msg = msg + content
        server = smtplib.SMTP_SSL(mailprops.smtp_host, int(mailprops.smtp_port))
        server.ehlo()
        server.login(mailprops.smtp_from, mailprops.smtp_pwd)
        send_to = ", ".join(mailprops.smtp_send_to)
        server.sendmail(mailprops.smtp_from, send_to, msg)
        server.quit()
        pass
