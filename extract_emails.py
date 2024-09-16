import os
import logging

from utils import get_gmail_service, store_emails
from constants import DB_PATH

def fetch_emails(service, max_results=10):
    emails = []
    page_token = None
    while len(emails) < max_results:
        results = service.users().messages().list(userId='me', maxResults=min(100, max_results-len(emails)), pageToken=page_token).execute()
        messages = results.get('messages', [])
        emails.extend([service.users().messages().get(userId='me', id=msg['id']).execute() for msg in messages])
        page_token = results.get('nextPageToken')
        if not page_token:
            break
    return emails

def main():
    logging.basicConfig(level=logging.INFO)

    if not os.path.exists(DB_PATH):
        logging.error("Database does not exist: %s", DB_PATH)
        raise FileNotFoundError(f"Database file {DB_PATH} does not exist.")

    email_count = input('Enter number of emails to process: ')
    
    try:
        email_count = int(email_count)
    except ValueError as err:
        raise ValueError("Invalid input, please enter a valid number.") from err

    if email_count <= 0:
        raise ValueError('Email count should be greater than 0')

    gmail_services = get_gmail_service()
    emails = fetch_emails(gmail_services, email_count)
    store_emails(emails)
    logging.info('Extraction done...')

if __name__ == '__main__':
    main()
