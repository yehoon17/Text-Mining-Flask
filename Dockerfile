FROM python:3.10

WORKDIR /text-mining-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./website ./website

COPY main.py .

CMD ["python", "main.py"]