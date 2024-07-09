FROM python:3.11.4

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# RUN wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip \
#     && unzip /tmp/chromedriver.zip -d /usr/local/bin \
#     && chmod +x /usr/local/bin/chromedriver \
#     && rm /tmp/chromedriver.zip


COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501