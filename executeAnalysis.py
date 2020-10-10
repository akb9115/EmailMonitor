import mysql.connector

from src.api import API
from src.config import Config

from dbConnector import dbConnector
from getTestData import getTestData


class executeAnalysis:

    def static_init() -> None:
        return API.static_init()

    def __init__(self):
        return

    def getAccountProfiles():
        connection = dbConnector.connectdb()
        dbcursor = connection.cursor()
        dbcursor.execute("SELECT tenant_id FROM accountprofile")
        result = dbcursor.fetchall()
        tenIdList = []

        for row in result:
            tenIdList.append(row[0])

        dbConnector.closedb(connection)
        return tenIdList

    def getEmailBotConfig(tenantId):
        connection = dbConnector.connectdb()
        dbcursor = connection.cursor()
        dbcursor.execute("SELECT * FROM emailbotconfig where tenant_id=\'" + tenantId + "\'")
        result = dbcursor.fetchall()
        dbConnector.closedb(connection)
        return result[0]

    def execute(self):
        if Config.is_enabledb():
            tenantIdList = executeAnalysis.getAccountProfiles()
        else:
            tenant_id = Config.get_tenantid()
            tenantIdList = [tenant_id]

        #print(tenantIdList)
        print(Config.is_enabledb())
        for tenantId in tenantIdList:
            if Config.is_enabledb():
                emailbotconfig = executeAnalysis.getEmailBotConfig(tenantId)
            else:
                emailbotconfig = (tenantId, Config.get_imapserver(), Config.get_smtpserver(), str(Config.get_smtpport()), Config.get_mailaccount(), Config.get_password(), str(Config.get_refresh()), Config.get_apiendpoint())
            print(emailbotconfig)
            getTestData.monitor_email(tenantId, emailbotconfig)


executeAnalysis.static_init()
executeAnalysis().execute()
