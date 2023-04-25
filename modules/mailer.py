from os import system
from os.path import abspath, exists

from datetime import date, datetime
import json

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
            datapath = abspath('./assets')

            if self.__alert_content == 'Compra':
                subject = f'| ALERTA DE COMPRA PARA {self.__ticker}|'

            else:
                subject = f'| ALERTA DE VENDA PARA {self.__ticker}|'
            
            attachments = f'-a {datapath}/indicadores.jpg -a {datapath}/graham.jpg'
            
            system(f'echo " " | mutt -s {subject} {attachments} -- {self.__dest}')
            self.__save_alert()


    def send_mail(self) -> None:
        """
        @brief: Envia os resultados de uma requisição para o e-mail do destinatário. No e-mail, estará em anexo um relatório sobre a ação.
        """
        if self.__alert:
            self.__send_alert()
        else:
            datapath = abspath('./assets')
            subject = f"Informações sobre o papel {self.__ticker}"
            attachments = f"{datapath}/{self.__ticker}-analysis.pdf"

            system(f'echo " " | mutt -s "{subject}" -a {attachments} -- {self.__dest}')
