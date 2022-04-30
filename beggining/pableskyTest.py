# Make sure you have installed the required packages:
#   pip install requests

from textwrap import indent
import requests
import json

url = 'https://api-us.restb.ai/vision/v2/multipredict'
payload = {
    # Add your client key
    'client_key': 'b717829c286243060e2429cc405e60bc480b18b2a4fe84b462e47cdf2ff41283',
    'model_id': 're_roomtype_global_v2,re_features_v3,re_appliances_v2',
    # Add the image URL you want to classify
    'image_url': 'https://static.inmofactory.com/images/inmofactory/documents/1/88767/19843271/299050732.jpg?rule=web_948x542'
}

# Make the classify request
response = requests.get(url, params=payload)

# The response is formatted in JSON
json_response = response.json()
print(type(json_response['response']['solutions']['re_features_v3']['detections']))