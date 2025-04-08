# StockValuation

## AVISO LEGAL :warning:

Os resultados expressos pelo sistema não configuram indicação de compra ou venda, servindo apenas a propósitos educacionais. O Criador deste sistema se exime de qualquer responsabilidade de perda financeira decorrente do uso deste sistema, e dos resultados por ele providos.

## Introdução ao sistema

O StockValuation é uma aplicação server-side para auxiliar o investidor em uma análise de indicadores fundamentalistas de ações da bolsa de valores. A aplicação funciona em cima do serviço de e-mails do gmail, portanto é necessário cadastrar um e-mail para que o sistema funciona corretamente. 

O sistema ainda está em desenvolvimento, e diversas funcionalidades que ainda não foram implementadas ainda irão aparecer, como:

* Análise e indicadores de FII´s
* Implementação de alertas de compra e venda baseado em preços
* Implementação de autenticação e cadastro de endereços válidos 

## Modo de uso:

Para gerar um relatório, basta enviar um e-mail para o endereço do servidor, com o ticker (ex.: CMIG4, PETR3...) no campo 'Assunto'. Após um tempo que varia entre 30 segundos e 2 minutos, a depender da conexão e capacidade de processamento, o servidor enviará um arquivo PDF para o e-mail solicitante, contendo diversos gráficos com as métricas dos indicadores fundamentalistas, além de uma avaliação de preço alvo da ação segundo o método de Graham

## Instalação
O sistema é um contêier docker, que pode ser criado através do comando
```shell
    sudo docker compose up -d --build mail-stock-valuator
```
No arquivo _.netconfig_, dentro da pasta mail-valuator, o usuário deverá preencher as seguintes variáveis de ambiente que serão utilizadas:
```properties
IMAP_HOST="imap.gmail.com"
IMAP_USER="<email_configurado>"
IMAP_PASSWD="<senha de aplicativo>"
SMTP_PORT=587
SMTP_HOST="smtp.gmail.com"
```
O serviço utilizado é o gmail, que permite criação de um e-mail gratuito, e disponibiliza uma senha de app para uso neste tipo de serviço. Um tutorial de como obter esta senha pode ser obtido [aqui](https://www.treinaweb.com.br/blog/enviando-email-com-python-e-smtp)

## Agradecimentos especiais

O sistema se vale de dados de dados retirados da API para python do Yahoo! Finance, além do webscrapper desenvolvido para NodeJS, que pode ser encontrado [neste link](https://github.com/lfreneda/statusinvestj). 

Um agradecimento especial aos criadores de ambos os serviços, que são fundamentais para o funcionamento deste sistema!
