#!/bin/sh

# Criando ambient virtual e instalando dependências do pip
echo "[+] Criando ambiente virtual Python3 para execução do script..."

python3 -m venv venv

if [$? -ne 0]
then
    echo "[!] Erro criando VENV. Verifique sua instalação de python e tente novamente"
    exit 1
fi

source ./venv/bin/activate

if [$? -ne 0]
then
    echo "[!] Erro ativando VENV. Abortando instalação."
    exit 1
fi

pip install -r requirements.txt

if [$? -ne 0]
then
    echo "[!] Erro instalando dependências. Tente instalar manualmente via $ pip install -r requirements.txt"
    exit 1
fi

# Instalando dependências do Node.js
npm install

if [$? -ne 0]
then
    echo "[!] Erro instalando dependências NPM. Tente instalar manualmente via $npm install"
    exit 1
fi

# # Configurando incron
# apt update
# apt install incron -y
# echo $USER >> /etc/incron.allow

