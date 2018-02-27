import smtplib

class SmtpUtility():
    @staticmethod
    def send(mailprops, content):
        msg = ("From: %s\r\nTo: %s\r\n\r\n"
               % (mailprops.smtp_from, ", ".join(mailprops.smtp_send_to)))
        msg = msg + content
        server = smtplib.SMTP(mailprops.smtp_host, mailprops.smtp_port)
        server.set_debuglevel(1)
        server.login(mailprops.smtp_from, mailprops.smtp_pwd)
        server.sendmail(mailprops.smtp_from, mailprops.smtp_send_to, msg)
        server.quit()
        pass
