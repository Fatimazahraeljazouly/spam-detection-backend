import requests
import json



def SendMail(data):
    url = "http://127.0.0.1:5000/sendEmail"
    payload = json.dumps(data) 
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)  
    print(response.text)