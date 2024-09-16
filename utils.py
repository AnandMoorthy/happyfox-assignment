import os
import re

import pickle
import sqlite3
import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from constants import INSERT_QUERY, GMAIL_SCOPES, DB_PATH,\
    GOOGLE_CREDENTIAL_JSON, PICKEL_FILE, EMAIL_PROCESSING_BATCH_SIZE

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

def get_db_connection():
    try:
        connection = sqlite3.connect(DB_PATH)
        logging.info('Database connection established.')
        return connection
    except sqlite3.Error as err:
        logging.error('Error while connecting with DB: %s', err)
        raise

def get_gmail_service():
	creds = None
 
	if os.path.exists(PICKEL_FILE):
     
		with open(PICKEL_FILE, 'rb') as token:
			creds = pickle.load(token)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIAL_JSON, GMAIL_SCOPES)
			creds = flow.run_local_server(port=0)

		with open(PICKEL_FILE, 'wb') as token:
			pickle.dump(creds, token)

	service = build('gmail', 'v1', credentials=creds)
	return service


def store_emails(emails):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    batch = []
    
    for email in emails:
        msg_id = email['id']
        headers = email['payload']['headers']
        from_email = next(header['value'] for header in headers if header['name'] == 'From')
        to_email = next(header['value'] for header in headers if header['name'] == 'To')
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        body = email['snippet']
        received_date = email['internalDate']
        from_email = extract_emails(from_email)
        to_email = extract_emails(to_email)
        
        batch.append((msg_id, from_email, to_email, subject, body, received_date))
        
        if len(batch) == EMAIL_PROCESSING_BATCH_SIZE:
            cursor.executemany(INSERT_QUERY, batch)
            batch.clear()
    
    # Insert any remaining records in the batch
    if batch:
        cursor.executemany(INSERT_QUERY, batch)
    
    conn.commit()
    conn.close()

def extract_emails(text):
    
    try:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
    except Exception as err:
        logging.warning('Got error at email extraction:', err)
        return text
    
    return emails[0]