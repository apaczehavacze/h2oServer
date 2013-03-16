'''
Created on 15-03-2013

@author: Jakub Guzik
'''
import socketserver
from base import TCPHandler 
from config import settings

if __name__ == "__main__":
    server = socketserver.TCPServer((settings.HOST, settings.PORT), TCPHandler.TCPHandler)
    server.serve_forever()
