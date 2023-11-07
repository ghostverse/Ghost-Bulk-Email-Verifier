# For tools contact me: https://t.me/ghostverse
import csv
import re
import email
import is_disposable_email
from email_validator import validate_email, EmailNotValidError
import os
import time

# Ask the user for the input CSV file
input_csv_file = input("Enter the name of the input CSV file (e.g., email.csv): ")

# Ask the user for the output file and its extension
output_file = input("Enter the name of the output file (e.g., Verified_Email.csv): ")

# Initialize the list for verified emails
verified_emails = []

def checkemail(s):
    pattern = r'\b[A-Za-z0.9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pattern, s):
        return "Valid Email"
    else:
        return "Invalid Email"

def disposableEmail(email):
    result = is_disposable_email.check(email)
    if result:
        return "Yes"
    else:
        return "No"

def emailValidate(email):
    try:
        emailinfo = validate_email(email, check_deliverability=True)
        email = emailinfo.normalized
        return "Yes", "-"
    except EmailNotValidError as e:
        return "No", str(e)

# Check if the input CSV file exists
if not os.path.exists(input_csv_file):
    print('\033[31m' + f"Error: The input file '{input_csv_file}' does not exist." + '\033[0m')
    exit(1)

animation_messages = ['Validating emails   ', 'Validating emails.  ', 'Validating emails.. ', 'Validating emails...']

# Simulate an animation while validating emails
for i in range(30):
    time.sleep(0.1)
    print('\033[32m' + animation_messages[i % 4] + '\033[0m', end='\r')

# Write the verified emails to the output CSV file
try:
    with open(output_file, mode='w', newline='') as output_csv:  # Use 'w' mode to write, overwriting the file
        writer = csv.writer(output_csv)
        writer.writerow(['Email', 'Validate Email', 'Domain Address', 'Disposable Email', 'Deliverable Email', 'Reason'])  # Write the header row

        # Read email list from the input CSV file provided by the user
        with open(input_csv_file, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                email = row['Email']
                isvalidemail = checkemail(email)
                isDisposableMail = disposableEmail(email)
                isDeliverableMail, isReason = emailValidate(email)
                verified_emails.append([email, isvalidemail, email.split('@')[1], isDisposableMail, isDeliverableMail, isReason])

        writer.writerows(verified_emails)
except Exception as e:
    print('\033[31m' + f"Error writing to the output CSV file: {str(e)}" + '\033[0m')
    exit(1)

print('\033[32m' + "Successful. Verified emails saved to " + output_file + '\033[0m')
