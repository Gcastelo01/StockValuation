#!/bin/sh

# Criando ambient virtual e instalando dependências do pip
echo "[+] Criando ambiente virtual Python3 para execução do script..."

python3 -m venv venv

if [ $? -ne 0 ]
then
    echo "[!] Erro criando VENV.  Deseja tentar instalar o gerenciador de venv python? [y/n]"
    read resp

    if [ $resp in 'y' ]
    then
        apt install python3.10-venv -y
        python3 -m venv venv
    else
        exit 1
    fi
fi

source ./venv/bin/activate

if [ $? -ne 0 ]
then
    echo "[!] Erro ativando VENV."
    read $resp
    exit 1
fi

pip install -r requirements.txt

if [ $? -ne 0 ]
then
    echo "[!] Erro instalando dependências. Tente instalar manualmente via $ pip install -r requirements.txt"
    exit 1
fi

# Instalando dependências do Node.js
npm install

if [ $? -ne 0 ]
then
    echo "[!] Erro instalando dependências NPM. Tente instalar manualmente via $npm install"
    exit 1
fi

# # Configurando incron
# apt update
# apt install incron -y
# echo $USER >> /etc/incron.allow

