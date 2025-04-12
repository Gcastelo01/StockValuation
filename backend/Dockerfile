# Backend com Python + Node
FROM python:3.9-slim

# Instala Node.js
RUN apt-get update && apt-get install -y curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L -o ./temp/quarto-linux-amd64.deb https://quarto.org/download/latest/quarto-linux-amd64.deb \
    && dpkg -i ./temp/quarto-linux-amd64.deb

# Diretório do app
WORKDIR /app

RUN mkdir logs \
    && mkdir temp \
    && mkdir data

# Instala dependências Python
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia backend
COPY . .

# Copia frontend buildado
COPY --from=frontend-builder /app/frontend/build ./static

CMD ["python", "main.py"]