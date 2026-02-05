from mysql.connector import errors, OperationalError
import mysql.connector
from dotenv import load_dotenv
import os

class connection_db:
    def __init__(self):
        self._cnx = None

    def db_connect(self):
        if self._cnx == None:
            try:
                load_dotenv()
                config = {
                    "host": os.getenv("API_SQL_HOST"),
                    "user": os.getenv("API_SQL_USER"),
                    "password": os.getenv("API_SQL_PW"),
                    "database": os.getenv("API_SQL_DB"),
                    "port": os.getenv("API_SQL_PORT"),
                }

                self._cnx = mysql.connector.connect(pool_name="db_pooling",
                                                    pool_size=5,
                                                    **config)
            except errors.ConnectionTimeoutError:
                print("超過線時間")
            except errors.PoolError:
                print("連線池發生錯誤")
            except Exception:
                print("連線異常")
        
    def db_cnx(self):
        if self._cnx != None:
            return self._cnx
    
    def restart_connect(self):
            self._cnx.reconnect(attempts=2, delay=3)