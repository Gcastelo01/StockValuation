#!/usr/bin/env bash

# Testando existência de diretório temporário
if [ ! -d "$PWD/temp" ]; then
    mkdir $PWD/temp
fi

# Criando serviço de monitoramento
VENV_DIR="$PWD/venv/bin/"
SRC_DIR="$PWD/monitor.py"

touch $PWD/logs/mailmonitor-service.log
touch $PWD/logs/mailmonitor-service-error.log

SERVICE_DESC="[Unit]\nDescription=Monitoramento de E-mail\nAfter=network.target\n\n[Service]\nExecStart=/bin/bash -c 'source $VENV_DIR/activate && $VENV_DIR/python3 $SRC_DIR' \nWorkingDirectory=$PWD\nRestart=always\nStandardOutput=append:$PWD/logs/mailmonitor-service.log\nStandardError=append:$PWD/logs/mailmonitor-service-error.log\n[Install]\nWantedBy=multi-user.target"

touch ./assets/mailmonitor.service

echo -e $SERVICE_DESC > ./assets/mailmonitor.service

cp ./assets/mailmonitor.service /etc/systemd/system/

# Iniciando serviço
systemctl daemon-reload
systemctl start mailmonitor
systemctl status mailmonitor
