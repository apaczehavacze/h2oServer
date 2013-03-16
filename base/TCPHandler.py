'''
Created on 15-03-2013

@author: Jakub Guzik
'''
import socketserver
from os import path
from crypt import crypt
from re import compile as compile_regex




class TCPHandler(socketserver.BaseRequestHandler):    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.user, self.password=self.data.split(b' ', 1)
        self.user=self.user.decode("utf-8")
        self.password=self.password.decode("utf-8")
        print(self.user)
        print(self.password)
        if self.check_auth()==True:
            self.request.sendall(b'True')
        # just send back the same data, but upper-cased
        else:
            self.request.sendall(b'False')
    
    def check_auth(self):
        salt_pattern = compile_regex(r"\$.*\$.*\$")
        passwd = "/etc/shadow" if path.exists("/etc/shadow") else "/etc/passwd"
        with open(passwd, "r") as f:
            rows = (line.strip().split(":") for line in f)
            records = [row for row in rows if row[0] == self.user]
        hush = records and records[0][1]
        #print (records)
        try:
            salt = salt_pattern.match(hush).group()
        except:
            return False
        return crypt(self.password, salt) == hush 
