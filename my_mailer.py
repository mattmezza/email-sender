import string
import yaml
import smtplib
import codecs
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.base import MIMEBase

class MyMailer:
    """A mailer for dareed testing """
    def __init__(self, cfg_file_name, mail_file_name):
        self.cfg_file_name = cfg_file_name
        stream = open(self.cfg_file_name, "r")
        self.info = yaml.load(stream)
        self.mail_file_name = mail_file_name
        self.mail_file = open(self.mail_file_name, 'r')
        self.mail_string = self.mail_file.read()
        self.mail_file.close()
        self.build_emails()

    def build_emails(self):
        self.emails = []
        body = ""
        for entry in self.info["emails"]:
            body = string.replace(self.mail_string, '__name__', entry["name"])
            body = string.replace(body, '__loginlink__', entry["loginlink"])
            body = string.replace(body, '__username__', entry["username"])
            body = string.replace(body, '__password__', entry["password"])
            body = string.replace(body, '__fbemail__', entry["fbemail"])
            body = string.replace(body, '__fbpassword__', entry["fbpassword"])
            email = {}
            email["body"] = body
            email["to"] = entry["recipient"]
            email["from"] = entry["sender"]
            email["reply_to"] = entry["reply_to"]
            email["subject"] = entry["subject"]
            self.emails.append(email)

    def print_emails(self):
        print self.emails

    def send_emails(self):
        smtp_cfg = self.info["smtp_cfg"]
        for email in self.emails:
            try:
                msg = MIMEText(email["body"], "plain", 'utf-8')
                msg['subject'] = email['subject']
                msg['from'] = email['from']
                msg['to'] = email['to']
                msg.add_header('reply-to', email['reply_to'])
                s = smtplib.SMTP(smtp_cfg['host'], smtp_cfg['port'])
                s.ehlo()
                s.ehlo
                s.login(smtp_cfg['username'], smtp_cfg['password'])
                s.sendmail(email['from'], email['to'], msg.as_string())
                s.quit()
                print "Email to " + email['to'] + " sent!"
            except Exception, e:
                print "Unable to send email to " + email['to'] + " :-("
                print "the exception: ", str(e)

mailer = MyMailer("emails_to_send.yml", "mail.html")
# mailer.print_emails()
mailer.send_emails()
