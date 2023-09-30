import base64
import io
import srsly
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pdf2image import convert_from_path
from PIL import Image
from rich import print 
from pathlib import Path

class Vision:
    def __init__(self):
        self.credentials = self.get_credentials()
        self.vservice = None
        self.request = None
        self.responses = None
        print('hello!')

    def get_credentials(self):
        try:
            creds = Path().cwd() / 'lenticular' / 'credentials.json'
            print(creds.exists())
            credentials = service_account.Credentials.from_service_account_file(
                creds
            )
            return credentials
        except Exception as e:
            print(e)
            #print(f"[red] Missing Google credentials.json file. Please follow the instructions here:\n https://developers.google.com/drive/api/quickstart/python [/red]")
            #return None
        
    def image_to_byte_array(image: Image) -> bytes:
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format=image.format)
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr

    def jpeg_to_data(self,path:str, language:str, type_:str = 'DOCUMENT_TEXT_DETECTION'):
        
        if self.credentials:
            image = Image.open(path)
            image_content = base64.b64encode(self.image_to_byte_array(image))
            vservice = build('vision', 'v1', credentials=self.credentials)
            request = vservice.images().annotate(body={
                'requests': [{
                    'image': {
                        'content': image_content.decode('UTF-8')
                    },
                    'imageContext': {
                        'languageHints': [language]},
                        'features': [{
                            'type': type_
                        }]
                }]
            })
            responses = request.execute(num_retries=3)
            responses['filename'] = str(path)
            return responses
        
        else:
            print(f"[red] Please set the API key. [/red]")


    def pdf_to_data(self, path:str, language:str, type_:str = 'DOCUMENT_TEXT_DETECTION'):
        policies = srsly.read_yaml("./lenticular/policies.yaml")
        
        if self.credentials:
            images = convert_from_path(path)
            data = []
            for i, image in enumerate(images):
                image_content = base64.b64encode(self.image_to_byte_array(image))
                vservice = build('vision', 'v1',  credentials=self.credentials)
                request = vservice.images().annotate(body={
                    'requests': [{
                        'image': {
                            'content': image_content.decode('UTF-8')
                        },
                        'imageContext': {
                            'languageHints': [language]},
                            'features': [{
                                'type': type_
                            }]
                    }]
                })
                responses = request.execute(num_retries=3)
                responses['page'] = i
                responses['filename'] = str(path)
                data.append(responses)
            return data
        else:
            print(f"[red] Please set the API key. [/red]")