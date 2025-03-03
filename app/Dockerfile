# Usa uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências
COPY ../requirements.txt .

# Instala as dependências
RUN pip install -r requirements.txt

# Copia o restante do código da aplicaçãopp .
COPY . .

# Expõe a porta em que a aplicação FastAPI roda
EXPOSE 8000

# Comando para rodar a aplicação
CMD uvicorn main:app --host 0.0.0.0 --port 8000     