#!/usr/bin/env bash

# Testando existência de diretório temporário
if [ ! -d "$PWD/temp" ]; then
    mkdir $PWD/temp
fi

if [ ! -d "$PWD/logs" ]; then
    mkdir $PWD/logs
fi

# Criando serviço de monitoramento
VENV_DIR="$PWD/venv/bin"
SRC_DIR="$PWD/monitor.py"

touch $PWD/logs/mailmonitor-service.log
touch $PWD/logs/mailmonitor-service-error.log

SERVICE_DESC="[Unit]\nDescription=Monitoramento de E-mail\nAfter=network.target\n\n[Service]\nExecStart=bash $PWD/scripts/service.sh\nWorkingDirectory=$PWD\nRestart=always\nStandardOutput=append:$PWD/logs/mailmonitor-service.log\nStandardError=append:$PWD/logs/mailmonitor-service-error.log\nUser=root\n\n[Install]\nWantedBy=multi-user.target"
CLEAN_DESC="[Unit]\nDescription=Limpeza de Cache de arquivos JSON gerados pelo mailmonitor.service\nAfter=network.target\n\n[Service]\nExecStart=bash $PWD/scripts/clean.sh\nWorkingDirectory=$PWD\nRestart=always\n\nUser=root\n\n[Install]\nWantedBy=multi-user.target\n\n[Timer]\nOnCalendar=*-*-* /1"

# Criando arquivos .service e incluindo diretrizes
touch ./temp/mailmonitor.service
touch ./temp/jsoncleaner.service
echo -e $SERVICE_DESC > ./temp/mailmonitor.service
echo -e $CLEAN_DESC > ./temp/jsoncelaner.service

cp ./temp/mailmonitor.service /etc/systemd/system/
cp ./temp/jsoncelaner.service /etc/systemd/system/

# Iniciando serviços
systemctl daemon-reload
systemctl start mailmonitor
systemctl start jsoncelaner
systemctl status mailmonitor

# Limpando diretório temporário
rm -rf ./temp