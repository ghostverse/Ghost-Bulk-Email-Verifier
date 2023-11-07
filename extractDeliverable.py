# For tools contact me: https://t.me/ghostverse
import csv
import os

# Ask the user for the input CSV file
input_csv_file = input("Enter the name of the input CSV file (e.g., email.csv): ")

# Ask the user for the output file and its extension
output_file = input("Enter the name of the output file (e.g., Deliverable_Email.csv): ")

# Initialize a list for deliverable emails
deliverable_emails = []

# Check if the input CSV file exists
if not os.path.exists(input_csv_file):
    print('\033[31m' + f"Error: The input file '{input_csv_file}' does not exist." + '\033[0m')
    exit(1)

# Read the email list from the input CSV file and extract deliverable emails
try:
    with open(input_csv_file, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            deliverable = row['Deliverable Email']
            if deliverable == 'Yes':
                email = row['Email']
                deliverable_emails.append(email)
except Exception as e:
    print('\033[31m' + f"Error reading the input CSV file: {str(e)}" + '\033[0m')
    exit(1)

# Write the deliverable emails to the output CSV file
try:
    with open(output_file, mode='w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(['Deliverable Email'])  # Write the header row

        for email in deliverable_emails:
            writer.writerow([email])
except Exception as e:
    print('\033[31m' + f"Error writing to the output CSV file: {str(e)}" + '\033[0m')
    exit(1)

print('\033[32m' + f"Deliverable emails saved to {output_file}" + '\033[0m')
