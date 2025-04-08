import smtplib
import json
import dotenv

from os import system
from os.path import abspath, exists

from datetime import date, datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders 
from email.mime.base import MIMEBase


class Mailer():
    """
    @brief: Classe responsável por lidar com o envio do resultado de uma análise via e-mail para um determinado remetente.

    @param ticker: Nome do papel cuja análise está sendo feita
    @param dest:  Destinatário que irá receber a análise
    @param alert: Se a análise a ser enviada é um alerta
    @param alert_content: O tipo do alerta (default = Compra)
    """
    def __init__(self, ticker, dest: str, alert=False, alert_content='Compra') -> None:
        self.__ticker = ticker
        self.__alert = alert
        self.__dest = dest
        self.__alert_content = alert_content
        self.__server_data = dotenv.dotenv_values('.netconfig')
        self.__DATAPATH = abspath('./data') + f'/{self.__ticker}-alert.json'

        
    def __save_alert(self) -> None:
        """
        @brief Armazena a data do último alerta para um determinado ticker. 
        """

        # Data do alerta
        today = date.today()
        today = today.strftime('%d/%m/%Y')
        
        # Criando JSON para salvar
        to_save = {
            'ticker' : f'{self.__ticker}', 
            'date' : today, 
            'tipo_alerta': self.__alert_content
        }

        jsonString = json.dumps(to_save)

        # Salvando dados no arquivo .json
        jsonFile = open(self.__DATAPATH, 'w')
        jsonFile.write(jsonString)
        jsonFile.close()
    

    def __get_last_alert(self) -> bool:
        """
        @brief: verifica se o último alerta enviado foi há mais de uma semana atrás.
        """
        if exists(self.__DATAPATH):
            # Lendo dados do alerta
            jsonFile = open(self.__DATAPATH, 'r').read()
            jsonObj = json.loads(jsonFile)
            
            # Comparando com data atual:
            today = datetime.today()
            dateAlert = datetime.strptime(jsonObj['date'], '%d/%m/%Y')

            # Tempo em semanas
            semanas = today - dateAlert
            semanas = semanas.days // 7

            if semanas > 1:
                return True
            
            else:
                return False

        else:
            return False


    def __send_alert(self) -> None:
        """
        @brief: Envia um alerta de compra ou venda, seguido do gráfico de preço da ação.
        """

        if self.__get_last_alert():
            msg = MIMEMultipart()

            msg['From'] = self.__server_data['IMAP_USER']
            msg['To'] = self.__dest

            datapath = abspath('./assets')

            if self.__alert_content == 'Compra':
                subject = f'| ALERTA DE COMPRA PARA {self.__ticker}|'

            else:
                subject = f'| ALERTA DE VENDA PARA {self.__ticker}|'
            
            msg['Subject'] = subject

            attachment1 = f'{datapath}/indicadores.jpg'
            with open(attachment1, 'rb') as img:
                im1 = img.read()
            
            attachment2 = f'{datapath}/graham.jpg'
            with open(attachment2, 'rb') as img:
                im2 = img.read()
            
            im1Mime = MIMEImage(im1)
            im1Mime.add_header('Content-Disposition', 'attachment', filename='indicadores.jpg')

            im2Mime = MIMEImage(im2)
            im2Mime.add_header('Content-Disposition', 'attachment', filename='graham.jpg')
            
            msg.attach(im1Mime)
            msg.attach(im2Mime)

            with smtplib.SMTP(self.__server_data['SMTP_HOST'], self.__server_data['SMTP_PORT']) as server:

                server.ehlo()

                server.starttls()

                server.login(self.__server_data['IMAP_USER'], self.__server_data['IMAP_PASSWD'])

                server.send_message(msg)

                server.quit()

            self.__save_alert()


    def send_mail(self) -> None:
        """
        @brief: Envia os resultados de uma requisição para o e-mail do destinatário. No e-mail, estará em anexo um relatório sobre a ação.
        """
        if self.__alert:
            self.__send_alert()

        else:
            subject = f"Informações sobre o papel {self.__ticker} \u2705"

            msg = MIMEMultipart()
            msg['From'] = self.__server_data['IMAP_USER']
            msg['To'] = self.__dest
            msg['Subject'] = subject

            attachments = f"{self.__ticker}-analysis.pdf"

            with open(attachments, 'rb') as f:
                pdf = f.read()

            pdf_mime = MIMEBase('application', 'octet-stream')
            pdf_mime.set_payload(pdf)
            encoders.encode_base64(pdf_mime)
            pdf_mime.add_header('Content-Disposition', 'attachment', filename='arquivo.pdf')

            msg.attach(pdf_mime)
            
            with smtplib.SMTP(self.__server_data['SMTP_HOST'], self.__server_data['SMTP_PORT']) as server:

                server.ehlo()

                server.starttls()

                server.login(self.__server_data['IMAP_USER'], self.__server_data['IMAP_PASSWD'])

                server.send_message(msg)

                server.quit()
                

    def send_error(self) -> None:
        """
        @brief: Envia uma mensagem de erro casa o ticker selecionado não seja um ticker válido da bolsa.
        """
        subject = f"Erro de Processamento! \u26A0\uFE0F \U0001f534"

        msg = MIMEMultipart()
        msg['From'] = self.__server_data['IMAP_USER']
        msg['To'] = self.__dest
        msg['Subject'] = subject

        msg.attach(MIMEText(f"O ticker {self.__ticker} não é um ticker válido."))
        
        with smtplib.SMTP(self.__server_data['SMTP_HOST'], self.__server_data['SMTP_PORT']) as server:

            server.ehlo()

            server.starttls()

            server.login(self.__server_data['IMAP_USER'], self.__server_data['IMAP_PASSWD'])

            server.send_message(msg)

            server.quit()

        print("Mensagem de erro enviada")


    def confirm_recieve(self) -> None:
        """
        @brief: Envia confirmação de recebimento de pedido para o destinatário
        """
        subject = "Requisição em processamento! \U0001f7e1"

        msg = MIMEMultipart()
        msg['From'] = self.__server_data['IMAP_USER']
        msg['To'] = self.__dest
        msg['Subject'] = subject

        msg.attach(MIMEText(f"A análise do Ticker {self.__ticker} já está em processamento!"))
        
        with smtplib.SMTP(self.__server_data['SMTP_HOST'], self.__server_data['SMTP_PORT']) as server:

            server.ehlo()

            server.starttls()

            server.login(self.__server_data['IMAP_USER'], self.__server_data['IMAP_PASSWD'])

            server.send_message(msg)

            server.quit()

        print("Mensagem de confirmação enviada")


    def ticker_not_found(self) -> None:
        """
        @brief: Envia mensagem de erro para o destinatário, caso o ticker tenha um formato válido, mas não seja encontrado na bolsa.
        """
        subject = f"Ticker {self.__ticker} inválido! \U0001f6a7"

        msg = MIMEMultipart()
        msg['From'] = self.__server_data['IMAP_USER']
        msg['To'] = self.__dest
        msg['Subject'] = subject

        msg.attach(MIMEText(f"O ticker {self.__ticker} não foi encontrado no Yahoo! finance. Verifique se é um ticker válido e tente novamente (O formato aceito é XXXXNN ou XXXXN, onde X são letras e N são números)."))
        
        with smtplib.SMTP(self.__server_data['SMTP_HOST'], self.__server_data['SMTP_PORT']) as server:

            server.ehlo()

            server.starttls()

            server.login(self.__server_data['IMAP_USER'], self.__server_data['IMAP_PASSWD'])

            server.send_message(msg)

            server.quit()

        print("Mensagem de aviso enviada")
        

    def imob_not_found(self) -> None:
        """
        @brief: Envia mensagem de erro para o destinatário, caso o ticker seja um FII.
        """
        subject = f"Ticker {self.__ticker} é FII! \U0001f6a7"

        msg = MIMEMultipart()
        msg['From'] = self.__server_data['IMAP_USER']
        msg['To'] = self.__dest
        msg['Subject'] = subject

        msg.attach(MIMEText(f"O ticker {self.__ticker} É um ticker de fundo imobiliário. No momento, o sistema ainda não faz a análise de FII's. Estamos trabalhando para implementar esta funcionalidade o mais rápido possível!"))
        
        with smtplib.SMTP(self.__server_data['SMTP_HOST'], self.__server_data['SMTP_PORT']) as server:

            server.ehlo()

            server.starttls()

            server.login(self.__server_data['IMAP_USER'], self.__server_data['IMAP_PASSWD'])

            server.send_message(msg)

            server.quit()

        print("Mensagem de aviso enviada")