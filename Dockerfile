FROM python:3.11-slim-buster

WORKDIR /app

COPY . /app

RUN apt update -y && apt install awscli -y

RUN pip install -r requirements.txt
# RUN pip install --upgrade accelerate
# RUN pip uninstall -y transformers accelerate
# RUN pip install transformers accelerate

CMD ["python3", "app.py"]