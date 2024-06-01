import socket
import ssl

from attachment import Attachment
from message import Message
from utils import base64string

class CustomSocket:
    def __init__(self, configuration):
        self.socket = None
        self.configuration = configuration
    
    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()
        
    def connect(self):
        self.socket.connect((self.configuration.host_address, self.configuration.port))
        self.socket = ssl.wrap_socket(self.socket)
        
    def request(self, request):
        self.socket.send((request + '\n').encode())
        recv_data = self.recv_all().decode()
        return recv_data

    def recv_all(self):
        return self.socket.recv(65535)

    def create_message(self):
        subject = self.configuration.subject
        message = Message(self.configuration)
        if not self.configuration.attachments:
            return f'Subject: =?UTF-8?B?{base64string(subject)}?=\n{message.text}\n.\n'
        message.append(message.text)
        attachments = [Attachment(filename).content for filename in self.configuration.attachments]
        [message.append(a) for a in attachments]
        message.end()
        return message.get_content()