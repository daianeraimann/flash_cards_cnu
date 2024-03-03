# Use a imagem oficial do Python como imagem base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o código do aplicativo para dentro do contêiner
COPY . .

# Instala as dependências do aplicativo
RUN pip install --no-cache-dir flask

# Define a porta em que o aplicativo Flask estará ouvindo
EXPOSE 5000

# Comando para iniciar o aplicativo quando o contêiner for iniciado
CMD ["python", "main.py"]
