# Secrets

```
$ lenticular secrets
```

To access Drive and/or Box, you will need credentials to prove that you have permission to access files on those services. I'll refer to these as secrets.  You will need to go into Box and Drive to gain the necessary credentials.  Once you have them, you can add them to lenticular's settings with this command:  



This command will prompt you to enter several values and will check for a `credentials.json` file which is required to access Drive. 

## Drive credentials 

To generate a `credentials.json` file, follow [these instructions from Google.]( https://developers.google.com/drive/api/quickstart/python) When you download the credentials file, it should look something like this inside:

```json
{
    "installed":
        {
            "client_id":"8944032.apps.googleusercontent.com",
            "project_id":"project-234812",
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"GOCSP-Ztr45L-q6iqb7","
            redirect_uris":["http://localhost"]
        }
}
```

Open the file in a text editor and copy the contents.  When you run `lenticular secrets`, you'll be prompted to paste the contents into the terminal.  Your data will be saved as a `credentials.json` file. When you run `lenticular drive-download <folder id>` for the first time, a login page will open in your browser.  Log in as you normally would with Google and the press "continue." That is all you need to access files and folders that you own or have been shared with you on Google Drive.  

# Box credentials 

Box requires a similar set of tokens to authenticate with the Box API. If you know the managers of your enterprise Box service, it's always a good idea to say "hello" and let them know why you need access and what you plan to do with the data. Only they can authorize an app, so you'll need their help.  In the meantime, you can get a temporary developer key that will do the job. 

1. Go to this page to [create a new oauth application](https://developer.box.com/guides/cli/quick-start/create-oauth-app/)
2. Create a new Box app, and click on "Create an App +"
3. You'll then need to log in with your Pennkey
4. Grant access to box in the popup 
5. You can now enter a name for your app, and click "Create App"
6. Head over to the [Developer Console](https://upenn.app.box.com/developers/console) and find your app in the "My Apps" section.
7. Click on the card for you project and then open the "Configuration" tab. 
8. In the section for "OAuth 2.0 Credentials," you'll see values for Client ID and Client Secret.  When you run `lenticular secrets` you'll be asked for three secrets.  The `BOX_CLIENT_ID` is the value you see as Client ID.  `BOX_CLIENT_SECRET` is Client Secret.
9. Finally, `BOX_DEVELOPER_TOKEN` can be found in the "Developer Token" section, just above the "OAuth 2.0 Credentials" section. You may need to click on a blue "Generate Developer Token" button. Note that this token is only valid for 60 minutes. When it runs out, you can get a new developer token by refreshing the page and clicking the blue button again once the hour has passed. 

<hr>

Once you've set the credentials with `lenticular secrets` you can now access all your file in Drive of Box and download them to your local computer.

To continue, go to either the [Box](../box) or [Drive](../drive) page. 