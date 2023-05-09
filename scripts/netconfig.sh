#!/usr/bin/env bash

read -p "E-mail para o servidor: " emailServidor

if [ ! (echo "$emailServidor" | grep -E "@gmail.com") ] 
then
    echo Endereço de e-mail inválido!
    exit 1
fi

read -p "Digite a senha numérica para o acesso automático" senha

touch .netconfig

echo -e "IMAP_HOST='imap.google.com'\nIMAP_PORT=993\nIMAP_USER='$emailServidor'\nIMAP_PASSWD='$senha'"
