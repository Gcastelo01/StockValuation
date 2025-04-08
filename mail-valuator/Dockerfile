FROM python:3.12-slim

# Instala Node.js
RUN apt-get update && apt-get install -y curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

    
# Diretório do app
WORKDIR /app

RUN mkdir logs \
    && mkdir temp \
    && mkdir data

# Instala dependências NodeJs
COPY ./package.json .
RUN npm install


# Instala dependências Python
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Instalando QUARTO e dependências
RUN curl -L -o ./temp/quarto-linux-amd64.deb https://quarto.org/download/latest/quarto-linux-amd64.deb \
    && dpkg -i ./temp/quarto-linux-amd64.deb \
    && quarto install tinytex \
    && rm -rf temp


# Copia serviços
COPY . .


CMD ["python3", "monitor.py"]