#!/usr/bin/env bash

# Testando existência de diretório temporário
if [ ! -d "$PWD/temp" ]; then
    mkdir $PWD/temp
fi

# Criando serviço de monitoramento
VENV_DIR="$PWD/venv/bin/python3"
SRC_DIR="$PWD/monitor.py"

SERVICE_DESC="[Unit]\nDescription=Monitoramento de E-mail\nAfter=network.target\n\n[Service]\nExecStart=$VENV_DIR $SRC_DIR \nWorkingDirectory=$PWD \nRestart=always\n\n[Install]\nWantedBy=multi-user.target"

touch ./assets/mailmonitor.service
echo -e $SERVICE_DESC > ./assets/mailmonitor.service

# cp ./assets/mailmonitor.service /etc/systemd/system/

# # Iniciando serviço
# systemctl daemon-reload
# systemctl start mailmonitor
# systemctl status mailmonitor
