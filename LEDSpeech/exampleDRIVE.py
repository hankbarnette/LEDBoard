from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from apiclient import errors
from apiclient.http import MediaFileUpload

import oauth2client
from oauth2client import client
from oauth2client import tools


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = '/home/pi/Desktop/Credentials/client_secret.json'
APPLICATION_NAME = 'Speech Recognition LED Board'


messageFile = '/home/pi/Desktop/Python/LEDSpeech/spokenMessages.txt'
messageFileTitle = 'spokenMessages.txt'
messageFileID = '0B_c8EUKFDVmpLUtDNjJzOEJXcDA'
messageFileDescription = 'Messages Spoken via Raspberry PI'
messageFileMIMETYPE = 'text/plain'
LEDFolderID = '0B_c8EUKFDVmpTW1HZ1dLRFpla0E'


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'SpeechRecognition.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getMessages(service):
    
    #Gets Message File
    print("Getting Files")
    #results = service.files().list(maxResults=10).execute()
    query = "title contains 'spokenMessage'"
    results = service.files().list(q=query).execute()
    items = results.get('items', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['title'], item['id']))
            parents = service.parents().list(fileId=item['id']).execute()
            for parent in parents['items']:
                print ('Parents: %s' % parent['id'])
                

def insertFile(service, title, description, parent_id, mime_type, filename):
    
    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {'title':title,'description':description,'mimeType':mime_type}

    #Set Parent Folder
    if parent_id:
        body['parents'] = [{'id':parent_id}]

    try:
        print("Trying to upload...")
        file = service.files().insert(body=body,media_body=media_body).execute()
        return file
    except errors.HttpError as error:
        print("An error occured: %s" % error)
        return None
    
def updateFile(service, file_id, new_title, new_description, new_mime_type, new_filename, new_revision):

    try:
        print('Uploading file: %s' % new_title)
        #Get the file to update
        file = service.files().get(fileId=file_id).execute()

        #update metadata
        file['title'] = new_title
        file['description'] = new_description
        file['mimeType'] = new_mime_type

        #File Content
        media_body = MediaFileUpload(new_filename,mimetype=new_mime_type,resumable=True)

        #Send the request
        updated_file = service.files().update(fileId=file_id,body=file,newRevision=new_revision,media_body=media_body).execute()

        return updated_file
    except errors.HttpError as error:
        print ('Update error occured: %s' % error)
        return None
    

#setup drive
def setupDrive():
    print("Setting up DRIVE...")
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    return service


if __name__ == '__main__':
    service = setupDrive()
    #getMessages(service)
    updateFile(service,messageFileID,messageFileTitle,messageFileDescription,messageFileMIMETYPE,messageFile,0)
    #insertFile(service, "Test File raspberry.txt","Sample Description",LEDFolderID,"text/plain",messageFile)



