import requests

from src.config import Config

class APIError(Exception):
    def __init__(self, status):
        self.status = status
        
    def __str__(self):
        return "APIError: status={}".format(self.status)

class API:
    
    def static_init():
        return Config.static_init()
    
    def _url(path):
        return Config.get_webhookurl() + path

    def post_request(sender="EmailBot", message="") -> str:
        # TODO: Process the body to get the relevent body text
        msg = message[:message.find('Regards')].replace('\n', '')
        msg = msg[:msg.find('Thanks')].replace('\n', '')
        resp = requests.post(API._url(""), json={
            'sender': sender,
            'message': msg
        })
        
        if resp.status_code != 200:
            raise APIError('Connection Failure: {}'.format(resp.status_code))
        else:
            response = "You mail is important to us. We will get back to you shortly with details on your query."
            if resp.json():
                response = ""
                for item in resp.json():
                    response += item['text'] + "\n\r"
                    
            response += "\n\nRegards,\nSupport Team"
            return response