#!/usr/bin/python

import sys, getopt, string, yaml, smtplib, codecs
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.base import MIMEBase

class MyEmail:
    """A mail model"""
    def __init__(self, from_, to, subject, body):
        self.from_ = from_
        self.to = to
        self.subject = subject
        self.body = body
        self.reply_to = ""

    def __str__(self):
        return "  from:  "+self.from_+"\n    to:  "+self.to+"\n  r_to:  "+self.reply_to+"\n  subj:  "+self.subject+"\n  body:\n"+self.body+"\n"

class MyMailer:
    """A mailer for sending emails """
    def __init__(self, cfg_file_name, emails_file_name):
        try:
            self.cfg_file_name = cfg_file_name
            stream = open(self.cfg_file_name, "r")
            self.config = yaml.load(stream)
            self.emails_file_name = emails_file_name
            stream = open(self.emails_file_name, "r")
            self.emails = yaml.load(stream)
            self.smtp_cfg = self.config["smtp_cfg"]
        except Exception, e:
            print "Error loading file: ", e
        self.build_emails()

    def build_emails(self):
        self.emails_to_send = []
        for entry in self.emails["emails"]:
            vars_ = self.emails["vars"].copy()
            body = entry["email"]["body"]
            if body.startswith("file://"):
                bodyFile = open(string.replace(body, "file://", ""), "r")
                body = bodyFile.read()
                bodyFile.close()
            # override global vars with local vars
            for var_name, var_val in entry["vars"].items():
                vars_[var_name] = var_val
            # replacing
            for var_name, var_val in vars_.items():
                body = string.replace(body, "__"+var_name+"__", var_val)
                for name, value in entry["email"].items():
                    entry["email"][name] = string.replace(value, "__"+var_name+"__", var_val)
            email = MyEmail(entry["email"]["sender"], entry["email"]["recipient"], entry["email"]["subject"], body)
            email.reply_to = entry["email"]["reply_to"]
            self.emails_to_send.append(email)

    def print_emails(self):
        i = 1
        for email in self.emails_to_send:
            print "---"
            print str(i)+":\n"+str(email)
            i=i+1

    def send_emails(self):
        for email in self.emails_to_send:
            self.send_email(email)

    def send_email(self, email):
        try:
            msg = MIMEText(email.body, "plain", 'utf-8')
            msg['subject'] = email.subject
            msg['from'] = email.from_
            msg['to'] = email.to
            if email.reply_to is not "":
                msg.add_header('reply-to', email.reply_to)
            s = smtplib.SMTP(self.smtp_cfg['host'], self.smtp_cfg['port'])
            s.ehlo()
            s.ehlo
            s.login(self.smtp_cfg['username'], self.smtp_cfg['password'])
            s.sendmail(email.from_, email.to, msg.as_string())
            s.quit()
            print "Email to " + email.to + " sent!"
        except Exception, e:
            print "Unable to send email to " + email.to + " :-("
            print "the exception: ", str(e)

def main(argv):
    config_file = "config.yml"
    emails_file = ""
    print_ = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],"c:e:ph",["config=","emails=","print", "help"])
    except getopt.GetoptError:
        print 'email-sender.py -c <config_file> -e <emails_file> [-p]'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print 'email-sender.py -c <config_file> -e <emails_file> [-p]'
            sys.exit()
        elif opt in ("-c", "--config"):
            config_file = arg
        elif opt in ("-e", "--emails"):
            emails_file = arg
        elif opt in ("-p", "--print"):
            print_ = True

    mailer = MyMailer(config_file, emails_file)
    if print_:
        mailer.print_emails()
    else:
        mailer.send_emails()
    print "\n_________________________________________"
    print "Thanks for having used this script, if you want to contribute you can fork it here https://github.com/matttmezza/email-sender"
if __name__ == "__main__":
   main(sys.argv[1:])