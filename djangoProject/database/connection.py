import os
import mysql.connector
from mysql.connector import Error


class DataBase:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open(self):
        try:
            DATABASE_URL = os.environ.get('JAWSDB_URL',
                                          'mysql://nuaorjd9fsoxr85j:i2gssvcqatfgrjwd@qzkp8ry756433yd4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ge45smj62w7no3mh')
            db_url = DATABASE_URL.split('/')
            creds, host_and_port, database = db_url[2].split('@')[0], db_url[2].split('@')[1], db_url[3]
            user, password = creds.split(':')[0], creds.split(':')[1]
            host, port = host_and_port.split(':')[0], host_and_port.split(':')[1]

            self.connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Successfully connected to the database")

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")


"""if __name__ == "__main__":
    db = DataBase()
    db.open()
    db.close()"""