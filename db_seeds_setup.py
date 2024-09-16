from utils import get_db_connection
import time

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails 
        (
            id TEXT PRIMARY KEY, 
            from_email TEXT, 
            to_email TEXT, 
            subject TEXT, 
            message TEXT, 
            received_date INTEGER
        )
    ''')

    # Adding Index to make the search faster
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_from_email ON emails(from_email);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_to_email ON emails(to_email);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_subject ON emails(subject);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_message ON emails(message);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_received_date ON emails(received_date);')

    # Dummy initial data
    dummy_data = [
        ("1", "john@example.com", "jane@example.com", "Hello, Jane!", "Just wanted to say hi.", int(time.time())), 
        ("2", "support@amazon.com", "user@example.com", "Your Order has been Shipped", "Your order #12345 is on its way.", int(time.time())),
        ("3", "news@newsletter.com", "subscriber@example.com", "Weekly Newsletter", "Here is your weekly news digest.", int(time.time())),
        ("4", "alice@example.com", "bob@example.com", "Meeting Reminder", "Don't forget our meeting tomorrow.", int(time.time())),
        ("5", "alerts@bank.com", "customer@example.com", "Account Alert", "Suspicious activity detected in your account.", int(time.time()))
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO emails (id, from_email, to_email, subject, message, received_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', dummy_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
