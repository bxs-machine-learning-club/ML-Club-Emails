__author__ = "Michael"

"""This script sends an email to members in the ML Club.
    Make sure to credit Michael Batavia for future usage of the script in the club
"""
import os
from string import Template
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import argparse
import csv


def read_contacts(csv_file):
    first_names = []
    emails = []
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', encoding='utf-8') as contacts:
            reader = csv.DictReader(contacts)
            for contact in reader:
                first_name = contact["Given Name"]
                email = contact["E-mail 1 - Value"]
                first_names.append(first_name)
                emails.append(email)

    return first_names, emails


def read_template(message_file):
    if os.path.exists(message_file):
        with open(message_file, mode="r", encoding="utf-8") as message:
            message_content = message.read()
        return Template(message_content)


def get_credentials(credentials_file):
    if os.path.exists(credentials_file):
        with open(credentials_file, mode="r", encoding="utf-8") as message:
            message_content = message.readline()
        return message_content.split(", ")[0], message_content.split(", ")[1]


def setup_email(contacts_file, message_file, html_template, title):
    user, pwd = get_credentials('credentials.txt')
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.starttls()
    server.login(user, pwd)
    create_email(contacts_file, message_file, html_template, server, title)


def create_email(contacts_file, message_file, html_template, server, subject):
    names, emails = read_contacts(contacts_file)
    print(emails)
    message_template = read_template(message_file)
    print(message_template)
    html_email_template = read_template(html_template)

    for name, email in zip(names, emails):
        msg = EmailMessage()
        message = message_template.substitute(PERSON_NAME=name.title())
        html_email: str = html_email_template.substitute(MESSAGE=message)

        user = get_credentials('credentials.txt')[0]
        print(user)
        msg['To'] = email
        # msg['To'] = 'bataviam@bxscience.edu'
        msg['From'] = user
        msg['Subject'] = subject

        # images = ('logo.png', '../images/zach.jpg',
        #          '../images/michael.png', '../images/montaha.png', '../images/robert.png')

        msg.set_content(MIMEText(html_email, 'html'))
        server.send_message(msg)
        print('success!', name, email)

        del msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("contacts_file", help="The csv file of the contacts to send this email to.")
    parser.add_argument("message_file", help="The message file for the message to send in the email.")
    parser.add_argument("html_template", help="The HTML template for the nice display in the email")
    parser.add_argument("subject", help="The subject of the email to send.")

    args = parser.parse_args()
    subject = args.subject if args.subject else "<no subject>"
    setup_email(args.contacts_file, args.message_file, args.html_template, subject)
