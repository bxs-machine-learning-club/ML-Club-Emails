__author__ = "David"

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
import subprocess
import stdiomask

contactsPath=r'C:\Users\School\Downloads\ML-Club-Emails-master\contacts.csv'
messagePath=r'C:\Users\School\Downloads\ML-Club-Emails-master\message42120.txt'
templatePath=r'C:\Users\School\Downloads\ML-Club-Emails-master\email_template.html'

testing=1

def passwordcheck(usr,psw):
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    try:
        server.login(usr,psw)
        ret = True
    except:
        ret = False
    server.quit()
    return ret

user=input('User Email: ')
pwd=stdiomask.getpass(prompt='Password: ', mask='*')
   
while(passwordcheck(user,pwd)==False):
    print()
    user=input('User Email: ')
    pwd=stdiomask.getpass(prompt='Password: ', mask='*')
    print()

print('Authentication Successful!')

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


def setup_email(contacts_file, message_file, html_template, title):
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.starttls()
    server.login(user, pwd)
    create_email(contacts_file, message_file, html_template, server, title)


def create_email(contacts_file, message_file, html_template, server, subject):
    names, emails = read_contacts(contacts_file)
    
    message_template = read_template(message_file)
    
    html_email_template = read_template(html_template)

    if testing==0:
        for name, email in zip(names, emails):
            print('Sending to: '+name.title()+' at '+email)
            
            msg = EmailMessage()
            message = message_template.substitute(PERSON_NAME=name.title())
            html_email: str = html_email_template.substitute(MESSAGE=message)
            
            msg['To'] = email
            msg['From'] = user
            msg['Subject'] = subject

            msg.set_content(MIMEText(html_email, 'html'))
            server.send_message(msg)
            print('Success!')
            print()
            
            del msg
    else:
        print('Sending to: '+'Me'+' at '+user)
        msg = EmailMessage()
        message = message_template.substitute(PERSON_NAME='Me')
        html_email: str = html_email_template.substitute(MESSAGE=message)

        msg['To'] = user
        msg['From'] = user
        msg['Subject'] = subject

        msg.set_content(MIMEText(html_email, 'html'))
        server.send_message(msg)
        print('Success!')

        del msg


if __name__ == "__main__":
    
    subject = input('Subject: ')
    subject = subject if subject else "<no subject>"
    setup_email(contactsPath, messagePath, templatePath, subject)
    
