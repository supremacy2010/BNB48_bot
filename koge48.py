import random
import json
import time
import ConfigParser
import mysql.connector
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class Koge48:
    def __init__(self,host,user,passwd,database):

        self._mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        self._mycursor = self._mydb.cursor()

        self._prob = 0.06
        self._tries = 0
        return
    def changeBalance(self,userid,number,memo=""):
        newblocksql = "INSERT INTO changelog (uid,differ,memo) VALUES (%s,%s,%s)"
        self._mycursor.execute(newblocksql,(userid,number,memo))
        self._mydb.commit()

        updatebalsql = "INSERT INTO balance (uid,bal) VALUES (%s,%s) ON DUPLICATE KEY UPDATE bal=bal+%s"
        self._mycursor.execute(updatebalsql,(userid,number,number))
        self._mydb.commit()

    def getBalance(self,userid):
        self._mycursor.execute("SELECT `bal` FROM `balance` WHERE `uid` = {}".format(userid))
        res = self._mycursor.fetchone()
        if res is None:
            return 0
        else:
            return res[0]
    def mine(self,minerid):
        self._tries+=1;
        if random.random()<self._prob:
            self.changeBalance(minerid,1,"mining")            
            self._tries = 0
            logger.warning("{} mined one".format(minerid))
            return True
        else:
            return False
