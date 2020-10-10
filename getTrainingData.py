import os
import re
import json
import time
import smtplib
import easyimap
import html2text

from src.api import API
from src.config import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class getTrainingData:
    
    def static_init() -> None:
        return API.static_init()
    
    def send_mail(receivers, subject, text):
        msg = MIMEMultipart()
        msg['From'] = Config.get_mailaccount()
        msg['To'] = ", ".join(receivers)
        msg['Subject'] = "RE:" + subject
        
        msg.attach(MIMEText(text))
        
        smtpObj = smtplib.SMTP(host=Config.get_smtpserver(), port=Config.get_smtpport())
        smtpObj.starttls()
        try:
            smtpObj.login(Config.get_mailaccount(), Config.get_password())
        except:
            print("Login attempt failed for Sending")
        
        smtpObj.sendmail(Config.get_mailaccount(), receivers, msg.as_string())
        print("SENT: " + msg.as_string())
        smtpObj.quit()
    
    def monitor_email() -> None:
        imapper = easyimap.connect(Config.get_imapserver(), Config.get_mailaccount(), Config.get_password())
        
        f = open("messages.json")
        processed_massages = json.loads(f.read())
        f.close()
        i = 0
        while True:
            print("Searching for command ... ")
            for mail_id in imapper.listids(limit=1000):
                mail = imapper.mail(mail_id)
                body = html2text.html2text(mail.body) 
                if str(mail_id) not in processed_massages:
                    #re.findall("^IMPORTANT COMMAND", body) \ and
                    subject = mail.title
                    citation = u"> From: " + mail.from_addr + '\n'
                    citation += u"> Date: " + mail.date + '\n'
                    citation += u"> Body: " + html2text.html2text(mail.body)
                    #EmailBot.remove_stop_words(html2text.html2text(mail.body))
                    # TODO: process the body and subject through RASA and then send mail reply.
                    # Work on the seperate module for making the web hook call
                    message = html2text.html2text(mail.body)
                    #message = API.post_request(message=html2text.html2text(mail.body))
                    # TODO: Improved on the send mail response
                    #EmailBot.send_mail([str(mail.from_addr)], subject, message)
                    #print(citation)
                    processed_massages[str(mail_id)] =  {'subject':subject, 'message':message, 'ts':int(time.time())}
                    f = open("messages.json", "w")
                    f.write(json.dumps(processed_massages))
                    f.close()
                    i = i + 1
                    f = open(os.getcwd() + '/data/trainingdata/' + str(i) + ".txt", "w")
                    f.write(subject + "\n")
                    f.write(message)
                    f.close()
                    print(str(mail_id) + " processed!")
            #time.sleep(Config.get_refresh())


getTrainingData.static_init()
getTrainingData.monitor_email()
