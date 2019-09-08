# -*- coding: utf-8 -*-

import time
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib


def sendFailureEmailWithAttachment(eMailIDs,payLoad):
        

        emails = [eMailIDs]
        sender = 'SampleEmailAccount'
        smtpserver = smtplib.SMTP("smtp.ADdomain.com",25)
        user = 'replace_with_userID'
        password = 'replace_with_password'
        smtpserver.ehlo()

        smtpserver.ehlo
        smtpserver.login(user, password)
   
        msg = MIMEMultipart()
        msg['Subject'] = "Powerplay cube build job failure."
        html = """\
               <html>
                               <head></head>
                               <body> 
                               The Cube build job has failed. Please review below for more information as well as the log files.

                               </body>
               </html>
               """
        mailBody = MIMEText(html, 'html')
        mailAttach = MIMEBase('application', "octet-stream")
        mailAttach.set_payload(open(payLoad , "rb").read())
         
        mailAttach.add_header('Content-Disposition', 'attachment', filename=payLoad)
     
        
        msg.attach(mailAttach)
        msg.attach(mailBody)

        smtpserver.sendmail(sender, emails, msg.as_string())
        smtpserver.close()
        return smtpserver.sendmail,smtpserver.close   
    
def sendSuccessEmailWithAttachment(eMailIDs,payLoad):
        

        emails = [eMailIDs]
        sender = 'SampleEmailAccount'
        smtpserver = smtplib.SMTP("smtp.ADdomain.com",25)
        user = 'replace_with_userID'
        password = 'replace_with_password'
        smtpserver.ehlo()

        smtpserver.ehlo
        smtpserver.login(user, password)
   
        msg = MIMEMultipart()
        msg['Subject'] = "Powerplay cube build job success."
        html = """\
               <html>
                               <head></head>
                               <body> 
                               The Cube build job sucessfully. Please review below for more information as well as the log file for cube build time and addl info.

                               </body>
               </html>
               """
        mailBody = MIMEText(html, 'html')
        mailAttach = MIMEBase('application', "octet-stream")
        part.set_payload(open(payLoad , "rb").read())
         
        mailAttach.add_header('Content-Disposition', 'attachment', filename=payLoad)
     
        
        msg.attach(mailAttach)
        msg.attach(mailBody)

        smtpserver.sendmail(sender, emails, msg.as_string())
        smtpserver.close()
        return smtpserver.sendmail,smtpserver.close   
