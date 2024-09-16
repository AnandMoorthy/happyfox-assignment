import os
import json
import logging

from utils import get_db_connection, get_gmail_service
from helpers import query_builder
from constants import RULES_CONFIG, GMAIL_UNREAD_LABEL, MARK_AS_UNREAD, MARK_AS_READ, MOVE_MESSAGE,\
    EMAIL_PROCESSING_BATCH_SIZE

def process_emails():
    """
    This Function process the emails from the db and apply
    the rules from rules.json file
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    rules = []
    with open(RULES_CONFIG, 'r') as f:
        rules = f.read()
    rules = json.loads(rules).get('rules',[])
    for rule in rules:
        rule_name = rule.get('name')
        logging.info(f'Processing Rule: {rule_name}')
        condition = rule.get('condition')
        filters = rule.get('filters')
        query = query_builder(filters, condition)
        cursor.execute(query)
        
        # Process email ids in batches
        batch_size = EMAIL_PROCESSING_BATCH_SIZE # Adjust this based on requirment
        while True:
            email_batch = cursor.fetchmany(batch_size)
            if not email_batch:
                logging.info('No more records found, switching to next rule...')
                break
            
            email_ids = [i[0] for i in email_batch]
            logging.info(f'Processing batch of {len(email_ids)} emails.')
            
            actions(email_ids, rule)
            logging.info(f'Completed processing Rule: {rule_name}')
        
        email_ids = cursor.fetchall()
        email_ids = [i[0] for i in email_ids]
        if len(email_ids) > 0:
            logging.info(f'Total Records Found: {len(email_ids)}')
            actions(email_ids, rule)
            logging.info(f'Actions Deployed for Rule: {rule_name}')
        print('*'*100)
    return True

def actions(email_ids, rule):
    """
    This is an helper function to run the actions
    specified in the rules.json
    """
    rule_name = rule.get('name')
    logging.info(f'Deploying Action for Rule: {rule_name}')
    action = rule.get('action')
    action_name = action.get('name')
    apply = action.get('apply')
    addLabelIds = []
    RemoveLabelIds = []
    # looping through apply to decide on the action
    for task in apply:
        if task == MARK_AS_UNREAD:
            addLabelIds.append(GMAIL_UNREAD_LABEL)
        elif task == MARK_AS_READ:
            RemoveLabelIds.append(GMAIL_UNREAD_LABEL)
        else:
            logging.debug(
                f'Unidentified task found, please check: {task}. Ignoring for now.')
            continue
    if action_name == MOVE_MESSAGE:
        addLabelIds.append(action.get('destination'))
    service = get_gmail_service()
    body = {
        "ids": email_ids,
        "addLabelIds": addLabelIds,
        "removeLabelIds": RemoveLabelIds
    }
    try:
        service.users().messages().batchModify(
            userId="me", body=body).execute()
        # print('\n')
    except Exception as e:
        logging.exception(f"Exception while deploying actions for Rule: {rule_name}")
        raise

def main():
    logging.basicConfig(level = logging.INFO)
    if not os.path.exists(RULES_CONFIG):
        logging.error(f'{RULES_CONFIG} not found, exiting...')
        raise FileNotFoundError(f"Rule config {RULES_CONFIG} does not exist.")
    process_emails()

if __name__ == '__main__':
    main()