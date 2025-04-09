FROM python:3.12-slim

# Instala Node.js e dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    libfontconfig1 \
    libfreetype6 \
    libxrender1 \
    libx11-dev \
    libxext6 \
    fontconfig \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Diretório do app
WORKDIR /app

# Copia arquivos de dependência primeiro (aproveita cache)
COPY ./requirements.txt .
COPY ./package*.json ./

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala dependências NodeJS
RUN npm install

RUN mkdir temp

# Instala Quarto
RUN curl -L -o ./temp/quarto-linux-amd64.deb https://quarto.org/download/latest/quarto-linux-amd64.deb \
    && dpkg -i ./temp/quarto-linux-amd64.deb \
    && quarto install tinytex \
    && rm -rf temp

# Copia o restante da aplicação
COPY . .

# Comando final
CMD ["python3", "monitor.py"]
