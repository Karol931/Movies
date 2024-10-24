from rest_framework.exceptions import APIException
import re

class RequestDataException(APIException):
    status_code = 400
    default_code = 'request data'
    default_detail = 'Provided wrong request data'

class TitleException(APIException):
    title = ''
    status_code = 400
    default_code = 'title' 
    detail = {default_code: f'There is no media named title in the database.'}
    

    def __init__(self, title):
        if title:
            self.title = title
        self.detail['title'] = re.sub(r'title' ,title, self.detail['title'])
    
class ServerNameException(APIException):
    title = ''
    status_code = 400
    default_code = 'server' 
    detail = {default_code: f'There is no server named server_name in the database.'}
    

    def __init__(self, server_name):
        if server_name:
            self.title = server_name
        self.detail['server'] = re.sub(r'server_name' ,server_name, self.detail['server'])

class ScrapingException(APIException):
    status_code = 400
    default_code = 'scraping'
    default_detail = {default_code: f'Couldn\'t scrap required parameters'}
