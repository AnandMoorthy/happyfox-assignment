### Steps to run the script

1. Open Command Line
2. Clone this repo
3. Create Virutal Environment(Follow: https://docs.python.org/3/library/venv.html) and activate
4. Run `pip install -r requirements.txt` to install the dependencies
5. Login to Google Developer Console and create Gmail API app and copy the credentials to `credentials.json` and move it to this folder
6. Run `db_seeds.py` to setup DB in local
7. Run `python -m unittest discover` to run the unittest cases
8. Run `python extract_emails.py` and enter the number of email to process to download and store in the DB, this will openup an Gmail OAuth. Please give necessary permission.
9. Modify the `rules.json` file as required
10. Run `python apply_rules_to_emails.py` to apply the rules and actions from rules.json to the data we stored in the DB which will reflect in actual Gmail account

### TODO

#### There are more features can be added in the future
1. Implement Message Queue to handle large volume of the emails
2. Implement Vector indexing for the text columns to improve the DB lookup
