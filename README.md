# ML-Club-Emails
This is the program to automate sending the club's weekly email to all of its memebrs. You can test any local changes by sending emails to only yourself (and therefore not spam the rest of the club :-) ) by changing `testing` to `True`.

## How to use:
1. Download the newst version of the repo as a ZIP file and unpack it.
1. Open send_email.py in IDLE and change the contactsPath, messagePath, and templatePath to match the paths of the contacts.csv, message.html, and email_template.html respectively (though since the paths are relative, there shouldn't be any need to).
1. Edit message.html to say whatever you wish (remember that PERSON_NAME refers to, well, the person's (first) name).
1. Go to Command Prompt (or Terminal if you are on OSX or Linux) and run the .py program.
1. Follow the prompts to enter in your Bronx Science email, Bronx Science password and the subject of the email.

That's it!
