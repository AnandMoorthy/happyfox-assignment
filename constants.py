EMAIL_PROCESSING_BATCH_SIZE = 100
DB_PATH = 'happyfox.db'
INSERT_QUERY = "INSERT OR IGNORE INTO emails (id, from_email, to_email, subject, message, received_date) VALUES (?, ?, ?, ?, ?, ?)"
GMAIL_SCOPES = [
     'https://www.googleapis.com/auth/gmail.modify', 
     'https://www.googleapis.com/auth/gmail.readonly'
    ]
GOOGLE_CREDENTIAL_JSON = 'credentials.json'
PICKEL_FILE = 'token.pickle'
RULES_CONFIG = 'rules.json'
GMAIL_UNREAD_LABEL = 'UNREAD'
MARK_AS_UNREAD = 'Mark as unread'
MARK_AS_READ = 'Mark as read'
MOVE_MESSAGE = 'Move Message'