import time

from attachment import Attachment
from configuration import Configuration
from custom_socket import CustomSocket
from message import Message
from utils import base64string

def main():
    configuration = Configuration("./data/config.json")
    with CustomSocket(configuration) as client:
        client.connect()
        client.recv_all()
        client.request(f'EHLO {configuration.user_name}')
        
        base64login = base64string(configuration.user_address)
        base64password = base64string(configuration.password)
        
        client.request('AUTH LOGIN')
        client.request(base64login)
        
        loginMessage = client.request(base64password)
        print(loginMessage)
        if "2.7.0" not in loginMessage:
            print("invalid login or password")
            exit()
            
        print('FROM:', client.request(f'MAIL FROM:<{configuration.user_address}>')[10::])
        for recipients in configuration.recipients:
            time.sleep(1)
            print(client.request(f'RCPT TO:{recipients}')[10::])
        
        print(client.request('DATA'))
        print(client.request(client.create_message())[10::])


if __name__ == "__main__":
    main()
