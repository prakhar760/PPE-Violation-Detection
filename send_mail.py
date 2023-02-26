'''
This module sends emails with attachments to the participants
Reference - https://developers.google.com/gmail/api/quickstart/python
'''
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import base64
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
def aunthentication():
    creds = None
    # The file token.json stores the user's access and refresh token,and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds
def prepare_and_send_email(recipient, subject, message_text,file):
    """Prepares and send email with attachment to the participants
    """
    creds = aunthentication()
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        #create message
        msg = create_message('anubhavpatrick@gmail.com', recipient,subject, message_text,file)

        send_message(service, 'me', msg)
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
def create_message(sender, to, subject, message_text,file):
    message=MIMEMultipart()
    message['to']=to
    message['from']=sender
    message['subject']=subject
    
    msg=MIMEText(message_text)
    message.attach(msg)
    
    (content_type,encoding)=mimetypes.guess_type(file)
    
    if content_type is None or encoding is not None:
        content_type='application/octet-stream'
        
    (main_type,sub_type)=content_type.split('/',1)
    
    if main_type== 'text':
        with open(file,'rb')as f:
            msg=MIMEText(f.read().decode('utf-8'),_subtype=sub_type)
    elif main_type== 'image':
        with open(file,'rb')as f:
            msg=MIMEImage(f.read(),_subtype=sub_type)
    elif main_type== 'audio':
        with open(file,'rb')as f:
            msg=MIMEAudio(f.read(),_subtype=sub_type)
    else:
        with open(file,'rb')as f:
            msg=MIMEBase(maintype, sub_type)
            msg.set_payload(f.read())
    filename=os.path.basename(file)
    msg.add_header('Content-Disposition','attachment',filename=filename)
    message.attach(msg)
    raw_msg=base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
    return {'raw':raw_msg.decode('utf-8')}
        
                
        
        
    
    return 
def send_message(service, user_id, message):
    """Send an email message.
    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id,body=message)

        .execute())

        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred: %s' % error)
if __name__ == '__main__':
    prepare_and_send_email('support.ai@giindia.com', 'PRAKHAR SINGH - GMAIL API TASK', 'Hello Sir, Prakhar Singh this side, sending task result of frontend designing','ssfrontend.png')
