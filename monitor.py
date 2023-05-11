import re

import imapclient
import email
import dotenv

from time import sleep
from os import system

import modules.setter as sett
import modules.mailer as mail

env_vals = dotenv.dotenv_values('.netconfig')

REGEX_PATTERN = r"^[A-Za-z]{4}\d{1,2}$"

IMAP_HOST = env_vals['IMAP_HOST']
IMAP_USER = env_vals['IMAP_USER']
IMAP_PSS = env_vals['IMAP_PASSWD']

with imapclient.IMAPClient(IMAP_HOST) as client:
    client.login(IMAP_USER, IMAP_PSS)

    print("Acesso concluído")


    while True:
        
        client.select_folder('INBOX')

        messages = client.search([u'UNSEEN'])

        if messages:
            for msg_id, data in client.fetch(messages, ['RFC822']).items():

                envelope = email.message_from_bytes(data[b'RFC822'])

                to_up = str(envelope.get("Subject"))
                mFrom = envelope.get("From").split(" ")[-1].replace("<", '').replace(">", "")

                print(to_up)
                print(mFrom)

                SENDER = mail.Mailer(to_up,mFrom)

                if re.match(REGEX_PATTERN, to_up):
                    print(f"TICKER: {to_up}")

                    system(f"node scripts/getData.js {to_up}")
                    SETTER = sett.Setter(to_up)
                    SETTER.generate_analysis()
                    SENDER.send_mail()

                else:
                    print("Ticker inválido")
                    SENDER.send_error()
            
            client.set_flags(messages, ['\Seen'])
        sleep(5)
