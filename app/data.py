import imaplib
import email
from getpass import getpass

# Login to your email account
username = input('gmail: ')
password = getpass('password: ')
imap_host = 'imap.web.de'
imap_port = 993

mail = imaplib.IMAP4_SSL(imap_host, imap_port)
mail.login(username, password)
mail.select('inbox')

status, messages = mail.search(None, 'SUBJECT "WG"')

for message_id in messages[0].split():
    _, msg_data = mail.fetch(message_id, "(RFC822)")
    email_body = msg_data[0][1]
    mail_message = email.message_from_bytes(email_body)

    for part in mail_message.walk():
        if part.get_content_type() == 'text/plain':
            content = part.get_payload(decode=True)
            print(content.decode())

            with open(f'/home/leo/coding/python/bkm_ai/test_newsl/newsletter_{message_id}.txt', 'wb') as f:
                f.write(content)