#!/usr/bin/env bash

# Criando ambient virtual e instalando dependências do pip
echo "[+] Criando ambiente virtual Python3 para execução do script..."

python3 -m venv venv

if [ $? -ne 0 ]
then
    echo "[!] Erro criando VENV.  Deseja tentar instalar o gerenciador de venv python? [y/n]"
    read resp

    if [ $resp = 'y' ]
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
    echo "[!] Erro instalando dependências NPM. Talvez o node não esteja instalado."
    read -p "[?] Deseja instalar o NodeJS e o NPM?. [y/n]" resp

    if [ resp = 'y' ]
    then
        apt install nodejs
        
        if [ $? -ne 0 ]
        then
            echo "[!] Erro ao instalar NodeJS!"
            exit 1
        fi

        echo "[+] NodeJS instalado com sucesso!"

        apt install npm

        if [ $? -ne 0 ]
        then
            echo "[!] Erro ao instalar NPM!"
            exit 1
        fi
        echo "[+] NodeJS instalado com sucesso!"
        npm install
    else
        exit 1
    fi
fi

# Instalando QUARTO (framework necessário para compilar notebooks)
echo "[+] Instalando framework QUARTO"
curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb
dpkg -i quarto-linux-amd64.deb

if [ $? -ne 0]
then
    echo "[!] Erro na instalação do quarto! Acesse https://quarto.org/docs/get-started/ e instale manualmente."
    exit 1
fi

echo "[+] Framework QUARTO instalado com sucesso!"

echo "[+] Instalando TinyTex"
quarto install tinytex

if [ $? -ne 0]
then
    echo "[!] Erro na instalação do TinyTex!"
    exit 1
fi

# # Configurando incron
# apt update
# apt install incron -y
# echo $USER >> /etc/incron.allow

