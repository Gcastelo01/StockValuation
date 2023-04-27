#!/usr/bin/env bash

erro(){
    if [ $1 -ne 0 ]
    then
        echo "$2"
        exit 1
    fi
}

# Criando ambient virtual e instalando dependências do pip
if [ ! -d "./venv" ]
then
    echo "[+] Criando ambiente virtual Python3 para execução do script..."
    python3 -m venv venv

    if [ $? -ne 0 ]
    then
        echo "[!] Erro criando VENV.  Deseja tentar instalar o gerenciador de venv python? [y/n]"
        read resp

        if [ $resp = 'y' ]
        then
            apt install python3-venv -y
            python3 -m venv venv
        else
            exit 1
        fi
    fi
fi

echo "[+] Ativando VENV"

source ./venv/bin/activate  

erro $? "[!] Erro ativando VENV."

pip install -r requirements.txt

erro $? "[!] Erro instalando dependências. Tente instalar manualmente via $ pip install -r requirements.txt"

# Instalando dependências do Node.js
npm install

if [ $? -ne 0 ]
then
    echo "[!] Erro instalando dependências NPM. Talvez o node não esteja instalado."
    read -p "[?] Deseja instalar o NodeJS e o NPM?. [y/n]" resp

    if [ $resp = 'y' ]
    then
        apt install nodejs -y
        
        if [ $? -ne 0 ]
        then
            echo "[!] Erro ao instalar NodeJS!"
            exit 1
        fi

        echo "[+] NodeJS instalado com sucesso!"

        apt install npm -y

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

erro $? "[!] Erro na instalação do quarto! Acesse https://quarto.org/docs/get-started/ e instale manualmente."

echo "[+] Framework QUARTO instalado com sucesso!"

echo "[+] Instalando TinyTex"
quarto install tinytex

erro $? "[!] Erro na instalação do TinyTex!"

echo "[+] TinyTex instalado com sucesso!"

echo "[+] Instalando incron"

apt install incron -y

erro $? "[!] Erro na instalação do incron!"

echo "[+] Acrescentando $USER ao incrontab"

echo $USER >> /etc/incron.allow

erro $? "[!] Erro ao configurar arquivo incron.allow. Digite manualmente seu nome de usuário em /etc/incron.allow"

echo "[+] Usuário $USER adicionado ao incrontab"
echo "[-] Removendo arquivos temporários..."

rm -r quarto-linux-amd64.deb

echo "[+] Instalação concluída com sucesso!/"