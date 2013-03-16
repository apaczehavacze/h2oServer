'''
Created on 16-03-2013

@author: Jakub Guzik
'''
import sqlite3
import threading
from os import path
import time
import sys
class DatabaseSync(threading.Thread,Exception):
    def __init__(self,DB_SYNC_TIME):
        self.DB_SYNC_TIME=DB_SYNC_TIME
        self.userList=[]
        threading.Thread.__init__(self)    
        self.connection = sqlite3.connect('dbase.db')
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS LoginAuth (login TEXT not null, hashpass TEXT not null, checked INT not null, PRIMARY KEY(login),UNIQUE(login) ON CONFLICT REPLACE) ")
        #cursor.execute("INSERT INTO LoginAuth VALUES('login','pppp1',1)")
        self.connection.commit()
        cursor.close()
        self.CheckAuth()
        self.BeforeUpdate()
        self.OnUpdate()
        
    def BeforeUpdate(self):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE LoginAuth SET checked=0")
        self.connection.commit()
        cursor.close()

    def CheckAuth(self):
        self.userList=[]
        ite=0
        passwd = "/etc/shadow" if path.exists("/etc/shadow") else "/etc/passwd"
        with open(passwd, "r") as f:
            rows = (line.strip().split(":") for line in f)
            records = [row for row in rows if row[1][0] == "$"]
        while ite !=len(records):
            self.userList.append(records[ite][:2])
            ite=ite+1

    def OnUpdate(self):
        cursor = self.connection.cursor()
        for it in self.userList:
            cursor.execute("INSERT OR REPLACE INTO LoginAuth VALUES (?,?,1)",(it[0],it[1]))
            cursor.execute("DELETE FROM LoginAuth WHERE Checked=0")
        self.connection.commit()
        cursor.close()          
    
    def run(self):

        if self.DB_SYNC_TIME>60 or self.DB_SYNC_TIME<1:
            print ("Check your DB_SYNC_TIME in settings.py!")
            raise 
        while True:
            self.CheckAuth()
            self.BeforeUpdate()
            self.OnUpdate()
            time.sleep(self.DB_SYNC_TIME*60)

p=DatabaseSync(1)
p.run()
