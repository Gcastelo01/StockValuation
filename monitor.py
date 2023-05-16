import re

import imapclient
import email
import dotenv

from time import sleep
from os import system
from datetime import datetime

import modules.setter as sett
import modules.mailer as mail

env_vals = dotenv.dotenv_values('.netconfig')

REGEX_PATTERN = r"^[A-Za-z]{4}\d{1,2}$"
REGEX_IMOBILIARIO = r"^[A-Za-z]{4}11$"

IMAP_HOST = env_vals['IMAP_HOST']
IMAP_USER = env_vals['IMAP_USER']
IMAP_PSS = env_vals['IMAP_PASSWD']

def now():
    return datetime.now()


with imapclient.IMAPClient(IMAP_HOST) as client:
    client.login(IMAP_USER, IMAP_PSS)

    print(f"| Iniciando monitor às {now()} |")
    print(f"Login com {IMAP_USER} realizado às {now()}")

    while True:
        
        client.select_folder('INBOX')
        messages = client.search([u'UNSEEN'])

        if messages:
            print(f"Novas mensagens encontradas!")

            for msg_id, data in client.fetch(messages, ['RFC822']).items():

                envelope = email.message_from_bytes(data[b'RFC822'])

                to_up = str(envelope.get("Subject"))
                mFrom = envelope.get("From").split(" ")[-1].replace("<", '').replace(">", "")

                print(f"{mFrom} solicitou informações do indicador {to_up} às {now}")

                SENDER = mail.Mailer(to_up, mFrom)

                if re.match(REGEX_PATTERN, to_up):
                    SENDER.confirm_recieve()
                    print(f"Gerando análise {now()}")
                    print(f"TICKER: {to_up}")

                    if not re.match(REGEX_IMOBILIARIO, to_up):
                        try:
                            system(f"node scripts/getData.js {to_up}")
                            SETTER = sett.Setter(to_up)
                            SETTER.generate_analysis()
                            SENDER.send_mail()
                            
                        except Exception:
                            SENDER.ticker_not_found()
                            
                    else:
                        SENDER.imob_not_found()

                    print(f"Email com análise enviado para {mFrom} às {now()}")

                else:
                    print("Ticker inválido")
                    SENDER.send_error()
                    print(f"Mensagem de erro enviada para {mFrom} às {now()}")

            client.set_flags(messages, ['\Seen'])
        sleep(5)
