#!/usr/bin/env bash

read -p "E-mail para o servidor: " emailServidor

read -p "Digite a senha numérica para o acesso automático" senha

touch .netconfig

echo -e "IMAP_HOST='imap.google.com'\nSMTP_PORT=587\nIMAP_USER='$emailServidor'\nIMAP_PASSWD='$senha'
SMTP_SERVER='smtp.gmail.com'" > .netconfig
