# For tools contact me: https://t.me/ghostverse
import csv
import is_disposable_email
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
import os
import time
import re

# Function to validate a batch of emails
def validate_batch(email_batch, writer):
    for email in email_batch:
        is_valid_email = check_email(email)
        is_disposable_mail = disposable_email(email)
        is_deliverable_mail, reason = validate_email_format(email)

        domain_address = email.split('@')[1] if '@' in email and len(email.split('@')) > 1 else ''
        writer.writerow([email, is_valid_email, domain_address, is_disposable_mail, is_deliverable_mail, reason])

# Function to check the format of an email
def check_email(s):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b'
    if re.match(pattern, s):
        return "Valid Email"
    else:
        return "Invalid Email"

# Function to check if an email is disposable
def disposable_email(email):
    result = is_disposable_email.check(email)
    return "Yes" if result else "No"

# Function to validate the format and deliverability of an email
def validate_email_format(email):
    try:
        email_info = validate_email(email, check_deliverability=True)
        email_normalized = email_info.normalized
        return "Yes", "-"
    except EmailSyntaxError as e_syntax:
        return "No (Syntax)", str(e_syntax)
    except EmailNotValidError as e_not_valid:
        return "No (Not Deliverable)", str(e_not_valid)
    except Exception as e:
        return "Error", str(e)

# Ask the user for the input CSV file with validation
while True:
    input_csv_file = input("Enter the name of the input CSV file (e.g., email.csv): ")
    if os.path.exists(input_csv_file):
        break
    else:
        print('\033[31m' + f"Error: The input file '{input_csv_file}' does not exist." + '\033[0m')

# Ask the user for the output file and its extension
output_file = input("Enter the name of the output file (e.g., Verified_Email.csv): ")

# Check if the output directory exists
output_dir = os.path.dirname(os.path.abspath(output_file))
if not os.path.exists(output_dir):
    print('\033[31m' + f"Error: The output directory for file '{output_file}' does not exist." + '\033[0m')
    exit(1)

batch_size = 1000  # Adjust the batch size based on your system's capabilities

animation_messages = ['Validating emails   ', 'Validating emails.  ', 'Validating emails.. ', 'Validating emails...']

# Simulate an animation while validating emails
for i in range(30):
    time.sleep(0.1)
    print('\033[32m' + animation_messages[i % 4] + '\033[0m', end='\r')

# Write the verified emails to the output CSV file
try:
    with open(output_file, mode='w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(['Email', 'Validate Email', 'Domain Address', 'Disposable Email', 'Deliverable Email', 'Reason'])  # Write the header row

        # Read email list from the input CSV file provided by the user
        with open(input_csv_file, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            email_batch = []
            
            for row in reader:
                email = row['Email']
                email_batch.append(email)

                if len(email_batch) == batch_size:
                    validate_batch(email_batch, writer)
                    email_batch = []

            # Process the last batch (if any)
            if email_batch:
                validate_batch(email_batch, writer)

except PermissionError:
    print('\033[31m' + f"Error: Permission denied while writing to the file '{output_file}'." + '\033[0m')
    exit(1)
except Exception as e:
    print('\033[31m' + f"Error writing to the output CSV file: {str(e)}" + '\033[0m')
    exit(1)

print('\033[32m' + "Successful. Verified emails saved to " + output_file + '\033[0m')
