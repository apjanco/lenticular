import base64
import io
import srsly
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pdf2image import convert_from_path
from PIL import Image
from rich import print 


def image_to_byte_array(image: Image) -> bytes:
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def jpeg_to_data(path:str, language:str, type_:str = 'DOCUMENT_TEXT_DETECTION'):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            './lenticular/credentials.json'
        )
    except ValueError:
        print(f"[red] Missing Google credentials.json file. Please follow the instructions here:\n https://developers.google.com/drive/api/quickstart/python [/red]")
        return None
    #TODO can this just load the json credentials file?
    if credentials:
        image = Image.open(path)
        image_content = base64.b64encode(image_to_byte_array(image))
        vservice = build('vision', 'v1', credentials=credentials)
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


def pdf_to_data(path:str, language:str, type_:str = 'DOCUMENT_TEXT_DETECTION'):
    policies = srsly.read_yaml("./lenticular/policies.yaml")
    try:
        credentials = srsly.read_json("./lenticular/credentials.json")
    except ValueError:
        print(f"[red] Missing Google credentials.json file. Please follow the instructions here:\n https://developers.google.com/drive/api/quickstart/python [/red]")
        return None
    
    if credentials:
        images = convert_from_path(path)
        data = []
        for i, image in enumerate(images):
            #Path(f'image{i}.jpg').write_bytes(image_to_byte_array(image))
            image_content = base64.b64encode(image_to_byte_array(image))
            vservice = build('vision', 'v1',  credentials=credentials)
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