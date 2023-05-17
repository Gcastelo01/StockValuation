#!/usr/bin/env bash

read -p "E-mail para o servidor: " emailServidor
echo "Um tutorial de como obter a senha para acesso do bot pode ser encontrado aqui: https://www.treinaweb.com.br/blog/enviando-email-com-python-e-smtp"
read -p "Digite a senha para o acesso: " senha

touch .netconfig

echo -e "IMAP_HOST='imap.gmail.com'\nSMTP_PORT=587\nIMAP_USER='$emailServidor'\nIMAP_PASSWD='$senha'
SMTP_HOST='smtp.gmail.com'" > .netconfig
