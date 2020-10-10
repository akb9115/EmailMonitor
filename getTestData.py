import os
import re
import sys
import requests
import json
import time
import smtplib
import easyimap
import html2text
import mysql.connector
from dbConnector import dbConnector
from executeEmailTfIdf import executeEmailTfIdf
from executeCNNModel import executeCNNModel

from src.api import API
from src.config import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class getTestData:

    """
    def static_init() -> None:
        return API.static_init()
    """

    def insertAnalysisData(tenant_id, acc_user, message_keywords, predicted_key, prediction_accuracy, request_ts, batchprocess_time):
        try:
            connection = dbConnector.connectdb()
            dbcursor = connection.cursor()
            sql = "insert into analysisdata(tenant_id, acc_user, message_keywords, predicted_key, prediction_accuracy, request_ts, creation_time, batchprocess_time) values(%s, %s, %s, %s, %s, %s, %s, %s)"
            creation_time = int(time.time())
            val = (tenant_id, acc_user, message_keywords, predicted_key, prediction_accuracy, request_ts, creation_time, batchprocess_time)
            #print(val)
            dbcursor.execute(sql, val)
            connection.commit()
        except:
            print('error')
            dbConnector.rollbackdb(connection)
        dbConnector.closedb(connection)

    #def send_mail(receivers, subject, text):
    def send_mail(emailBotConfig, receivers, subject, text):
        msg = MIMEMultipart()
        msg['From'] = Config.get_mailaccount()
        msg['To'] = ", ".join(receivers)
        msg['Subject'] = "RE:" + subject
        
        msg.attach(MIMEText(text))
        
        #smtpObj = smtplib.SMTP(host=Config.get_smtpserver(), port=Config.get_smtpport())
        smtpObj = smtplib.SMTP(host=emailBotConfig[2], port=emailBotConfig[3])
        smtpObj.starttls()
        try:
            #smtpObj.login(Config.get_mailaccount(), Config.get_password())
            smtpObj.login(emailBotConfig[4], emailBotConfig[5])
        except:
            print("Login attempt failed for Sending")

        #smtpObj.sendmail(Config.get_mailaccount(), receivers, msg.as_string())
        smtpObj.sendmail(emailBotConfig[4], receivers, msg.as_string())
        #print("SENT: " + msg.as_string())
        smtpObj.quit()
    
    #def monitor_email() -> None:
        #imapper = easyimap.connect(Config.get_imapserver(), Config.get_mailaccount(), Config.get_password())
    def monitor_email(tenantId, emailBotConfig) -> None:

        imapper = easyimap.connect(emailBotConfig[1], emailBotConfig[4], emailBotConfig[5])
        f = open("messages.json")
        processed_messages = json.loads(f.read())
        f.close()
        #i = 0
        #while True:
        print("Checking email server ... ")
        batchprocess_time = int(time.time())
        for mail_id in imapper.listids(limit=1000):
            mail = imapper.mail(mail_id)
            body = html2text.html2text(mail.body)
            if str(mail_id) not in processed_messages:
                #re.findall("^IMPORTANT COMMAND", body) \ and
                subject = mail.title
                customeremailid = mail.from_addr
                try:
                    customername = customeremailid[:customeremailid.index('<')]
                except:
                    customername = customeremailid[:customeremailid.index('@')]
                #print(customername)

                citation = u"> From: " + mail.from_addr + '\n'
                citation += u"> Date: " + mail.date + '\n'
                citation += u"> Body: " + html2text.html2text(mail.body)
                mailTimestamp = mail.date
                #EmailBot.remove_stop_words(html2text.html2text(mail.body))
                # TODO: process the body and subject through RASA and then send mail reply.
                # Work on the seperate module for making the web hook call
                message = html2text.html2text(mail.body)
                #message = API.post_request(message=html2text.html2text(mail.body))
                # TODO: Improved on the send mail response

                #print(citation)
                processed_messages[str(mail_id)] =  {'subject':subject, 'message':message, 'ts':batchprocess_time}
                f = open("messages.json", "w")
                f.write(json.dumps(processed_messages))
                f.close()
                mailcontent = subject + "\n" + message
                #i = i + 1
                #f = open(os.getcwd() + '/data/testdata/' + str(i) + ".txt", "w")
                #f.write(subject + "\n")
                #f.write(message)
                #f.close()
                print(mail_id, mail.from_addr, " processed!")
                executeEmailTfIdfObj = executeEmailTfIdf()
                executeModelObj = executeCNNModel()
                #if "enanko" or "akshay" or "sunny" or "priyanka" in mail.from_addr:
                #if "atin" in mail.from_addr:
                #if "avisheko" in mail.from_addr:
                try:
                    #keywords = executeEmailTfIdfObj.executeTFIDF(str(i) + ".txt")
                    keywords = executeEmailTfIdfObj.executeTFIDF(mailcontent)
                    orderId = keywords[0]
                    message_keywords = 'none odderid ' + keywords[1] + ' ' + keywords[2]
                    email_template_category, confidence = executeModelObj.execute(message_keywords)
                except:
                    email_template_category = 0

                if email_template_category == 0:
                    email_template_filename = 'unknown_template'
                elif email_template_category == 1:
                    email_template_filename = 'status_template'
                elif email_template_category == 2:
                    email_template_filename = 'track_template'
                elif email_template_category == 3:
                    email_template_filename = 'cancel_template'
                elif email_template_category == 4:
                    email_template_filename = 'complain_template'
                #print(email_template_filename)

                try:
                    if Config.is_enabledb():
                        getTestData.insertAnalysisData(tenantId, str(mail.from_addr), message_keywords, email_template_filename, str(confidence), mailTimestamp, str(batchprocess_time))
                    file = open(os.getcwd() + '/data/template/' + email_template_filename, 'r', encoding="utf8", errors='ignore')
                    email_response = file.read().strip()
                    file.close()
                    #print(email_template_category)
                    if email_template_category != 0:
                        email_response = email_response.replace("{ORDER_ID}", orderId)
                        #email_response = email_response.replace("{TRACK_ID}", trackId)
                        endpointUrl = emailBotConfig[7]
                        #print(endpointUrl)
                        if email_template_category == 1:
                            r = requests.get(endpointUrl + 'orders/' + orderId)
                            json_response = r.json()
                            email_response = email_response.replace("{CUSTOMER_FIRST_NAME}", customername)
                            email_response = email_response.replace("{ORDER_STATUS}", json_response[0]['order_status'])
                            email_response = email_response.replace("{ITEM_TITLE}", json_response[0]['item_title'])
                            email_response = email_response.replace("{SHIPMENT_ADDRESS}", json_response[0]['shipment_address'])
                            email_response = email_response.replace("{ESTIMATED_DELIVERY_TIME}", json_response[0]['estimated_delivery_time'])
                            email_response = email_response.replace("{TRACKING_ID}", json_response[0]['tracking_id'])
                            email_response = email_response.replace("{SHOPPING_WEBSITE}", json_response[0]['shopping_website'])
                        elif email_template_category == 2:
                            r = requests.get(endpointUrl + 'tracking/' + orderId)
                            json_response = r.json()
                            email_response = email_response.replace("{CUSTOMER_FIRST_NAME}", customername)
                            email_response = email_response.replace("{SHIPMENT_DATE}", json_response[0]['shipment_date'])
                            email_response = email_response.replace("{SHIPMENT_SERVICE_NAME}", json_response[0]['shipment_service_name'])
                            email_response = email_response.replace("{SHIPMENT_DURATION}", json_response[0]['shipment_duration'])
                            email_response = email_response.replace("{SHIPMENT_ADDRESS}", json_response[0]['shipment_address'])
                            email_response = email_response.replace("{TRACKING_POSITION}", json_response[0]['tracking_position'])
                            email_response = email_response.replace("{TRACKING_ID}", json_response[0]['tracking_id'])
                            email_response = email_response.replace("{SHOPPING_WEBSITE}", json_response[0]['shopping_website'])
                        elif email_template_category == 3:
                            r = requests.put(endpointUrl + 'cancel/' + orderId)
                            json_response = r.json()
                            #print(json_response)
                            email_response = email_response.replace("{CUSTOMER_FIRST_NAME}", customername)
                            email_response = email_response.replace("{ORDER_STATUS}", json_response[0]['order_status'])
                        elif email_template_category == 4:
                            r = requests.put(endpointUrl + 'complaint/' + orderId)
                            json_response = r.json()
                            #print(json_response)
                            email_response = email_response.replace("{CUSTOMER_FIRST_NAME}", customername)
                            email_response = email_response.replace("{ORDER_STATUS}", json_response[0]['order_status'])
                            email_response = email_response.replace("{COMPLAIN_NUMBER}", json_response[0]['complain_number'])
                    #print(json_response)
                    email_response = email_response + '\n\n\n >>>>>>>>>>>>>>> \n\n You wrote below mail :\n\n\n' + message
                    #getTestData.send_mail(emailBotConfig, [str(mail.from_addr)], subject, email_response)
                except:
                    e = sys.exc_info()[0]
                    print("<p>Error: %s</p>" % e)

            #time.sleep(int(emailBotConfig[6]))


#getTestData.static_init()
#getTestData.monitor_email()
