import mysql.connector


class dbConnector:


    def connectdb():
        connection = mysql.connector.connect(
            host="localhost",
            user="botuser",
            passwd="intel#789",
            database="intgbot",
            auth_plugin="mysql_native_password"
        )
        return connection

    def closedb(connection):
        connection.close()

    def rollbackdb(connection):
        connection.rollback()
