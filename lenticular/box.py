import requests 
from boxsdk import Client, OAuth2

#Go to
#https://developer.box.com/guides/cli/quick-start//
#https://developer.box.com/guides/cli/quick-start/create-oauth-app/

auth = OAuth2(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token='YOUR_DEVELOPER_TOKEN',
)
client = Client(auth)

f = client.file('1200022205243').get()
url = f.get_download_url()
file = requests.get(url)