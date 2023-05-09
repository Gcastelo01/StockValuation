import re

import imapclient
import dotenv

from time import sleep
import modules.setter as sett
import modules.mailer as mail

REGEX_PATTERN = r"^[A-Za-z]{4}\d{1,2}$"

env_vals = dotenv.dotenv_values('.env')

IMAP_HOST = env_vals['IMAP_HOST']
IMAP_PORT = env_vals['IMAP_PORT']
IMAP_USER = env_vals['IMAP_USER']
IMAP_PSS = env_vals['IMAP_PASSWD']


with imapclient.IMAPClient(IMAP_HOST, IMAP_PORT) as client:
    client.login(IMAP_USER, IMAP_PSS)
    client.select_folder('INBOX')

    while True:
        try:
            messages = client.search(['UNSEEN'])
            
            if messages:
                for msg_id, data in client.fetch(messages, ['ENVELOPE']).items():
                    envelope = data[b'ENVELOPE']
                    to_up = str(envelope.subject).upper()
                    SENDER = mail.Mailer(to_up, envelope.sender)
                    
                    if re.match(REGEX_PATTERN, to_up):
                        SETTER = sett.Setter(to_up)
                        
                        SETTER.generate_analysis()
                        SENDER.send_mail()

                    else:
                        SENDER.send_error()

            sleep(10)

        except Exception:
            break
