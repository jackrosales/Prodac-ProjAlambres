import requests
import time

class HTTPDataSender:
    data_post = []
    data_get =[]
    post_api_url = 'http://localhost:5000/datos_json/'
    get_api_url = 'http://localhost:5000/datos_json/status'
    
    def __init__(self, post_api_url, get_api_url):
        self.post_api_url = post_api_url
        self.get_api_url = get_api_url

    def send_data(self, data):
        try:
            response = requests.post(self.api_url, json=data)
            if response.status_code == 200:
                print('HTTP POST request successful.')
            else:
                print('HTTP POST request failed. Status code:', response.status_code)
        except requests.exceptions.RequestException as e:
            print('HTTP POST request error:', e)
    
    def receive_data(self):
        
        response = requests.get(self.get_api_url)
        return response


