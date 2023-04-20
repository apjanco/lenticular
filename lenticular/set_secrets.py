import os 
import json

def set_secrets():
    secrets = ['HUGGINGFACE_TOKEN']
    for secret in secrets:
        current_secret_value = os.environ.get(secret)
        if current_secret_value is None:
             new_secret_value = input(f"Enter a value for {secret}: ")
             os.environ[secret] = new_secret_value
        else:
            new_secret_value = input(f"Enter a new value for {secret} (currently: {current_secret_value}): ")
            os.environ[secret] = new_secret_value
    # check if credentials.jsons file exists        
    if os.path.exists('credentials.json'):
        # check if credentials.json file is empty
        if os.stat('credentials.json').st_size == 0:
            # if it is empty, delete it
            os.remove('credentials.json')
        # if it is not empty, ask user if they want to overwrite it
        else:
            overwrite = input("credentials.json file already exists. Overwrite? (y/n): ")
            if overwrite == 'y':
                os.remove('credentials.json')
        
    # if it does not exist, create it
    if not os.path.exists('credentials.json'):
        # create credentials.json file
        with open('credentials.json', 'w') as file:
            client_id = input(f"Enter a value for client_id: ")
            project_id = input(f"Enter a value for project_id: ")
            client_secret = input(f"Enter a value for client_secret: ")
            data = {"installed":{"client_id":client_id},"project_id":project_id,"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":client_secret,"redirect_uris":["http://localhost"]}}
            file.write(json.dumps(data))

if __name__ == '__main__':
    set_secrets()   