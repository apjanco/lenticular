import base64
import io
import srsly
from googleapiclient.discovery import build
from pdf2image import convert_from_path
from PIL import Image
from rich import print 


def image_to_byte_array(image: Image) -> bytes:
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def jpeg_to_data(path:str, language:str, type_:str = 'DOCUMENT_TEXT_DETECTION'):
    secrets = srsly.read_yaml("./lenticular/secrets.yaml")
    APIKEY = secrets.get("GOOGLE_API_KEY", None)
    if APIKEY:
        image = Image.open(path)
        image_content = base64.b64encode(image_to_byte_array(image))
        vservice = build('vision', 'v1', developerKey=APIKEY)
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
    APIKEY = policies.get("google_api_key", None)
    if APIKEY:
        images = convert_from_path(path)
        data = []
        for i, image in enumerate(images):
            #Path(f'image{i}.jpg').write_bytes(image_to_byte_array(image))
            image_content = base64.b64encode(image_to_byte_array(image))
            vservice = build('vision', 'v1', developerKey=APIKEY)
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