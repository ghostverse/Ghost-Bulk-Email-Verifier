import csv
import re
import email
import is_disposable_email
from email_validator import validate_email, EmailNotValidError

# Ask the user for the input CSV file
input_csv_file = input("Enter the name of the input CSV file (e.g., email.csv): ")

# Ask the user for the output file and its extension
output_file = input("Enter the name of the output file (e.g., Verified_Email.csv): ")

# Initialize the list for verified emails
verified_emails = []

def checkemail(s):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pattern, s):
        return '\033[32m' + "Valid Email" + '\033[0m'
    else:
        return '\033[31m' + "Invalid Email" + '\033[0m'

def disposableEmail(email):
    result = is_disposable_email.check(email)
    if result:
        return '\033[31m' + "Yes" + '\033[0m'
    else:
        return '\033[32m' + "No" + '\033[0m'

def emailValidate(email):
    try:
        emailinfo = validate_email(email, check_deliverability=True)
        email = emailinfo.normalized
        return '\033[32m' + "Yes" + '\033[0m', "-"
    except EmailNotValidError as e:
        return '\033[31m' + "No" + '\033[0m', str(e)

# Read email list from the input CSV file provided by the user
with open(input_csv_file, encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        email = row['Email']
        isvalidemail = checkemail(email)
        isDisposableMail = disposableEmail(email)
        isDeliverableMail, isReason = emailValidate(email)
        verified_emails.append([email, isvalidemail, email.split('@')[1], isDisposableMail, isDeliverableMail, isReason])

# Write the verified emails to the output CSV file
with open(output_file, mode='w', newline='') as output_csv:
    writer = csv.writer(output_csv)
    writer.writerow(['Email', 'Validate Email', 'Domain Address', 'Disposable Email', 'Deliverable Email', 'Reason'])
    writer.writerows(verified_emails)

print('\033[32m' + "Successful." + '\033[0m', f"Verified emails saved to {output_file}")
